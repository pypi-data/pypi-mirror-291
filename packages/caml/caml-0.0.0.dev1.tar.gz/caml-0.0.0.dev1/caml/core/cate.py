from __future__ import annotations

import copy
import logging

import ibis
import numpy as np
import pandas
import polars
import pyspark
import ray
from econml._cate_estimator import BaseCateEstimator
from econml._ortho_learner import _OrthoLearner
from econml.dml import DML, CausalForestDML, LinearDML, NonParamDML
from econml.dr import DRLearner
from econml.metalearners import DomainAdaptationLearner, SLearner, TLearner, XLearner
from econml.score import EnsembleCateEstimator, RScorer
from econml.validate.drtester import DRTester
from ibis.common.exceptions import IbisTypeError
from ibis.expr.types.relations import Table
from joblib import Parallel, delayed
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import PolynomialFeatures
from typeguard import typechecked

from ._base import CamlBase

logger = logging.getLogger(__name__)


class CamlCATE(CamlBase):
    """
    The CamlCATE class represents an opinionated implementation of Causal Machine Learning techniques for estimating
    highly accurate conditional average treatment effects (CATEs) and constucting CATE ensemble models.

    This class... TODO

    Parameters
    ----------
    df:
        The input DataFrame representing the data for the EchoCATE instance.
    Y:
        The str representing the column name for the outcome variable.
    T:
        The str representing the column name(s) for the treatment variable(s).
    X:
        The str (if unity) or list of feature names representing the heterogeneity feature set. Defaults to None.
    W:
        The str (if unity) or list of feature names representing the confounder feature set. Defaults to None.
    uuid:
        The str representing the column name for the universal identifier code (eg, ehhn). Defaults to None, which implies index for joins.
    discrete_treatment:
        A boolean indicating whether the treatment is discrete or continuous. Defaults to True.

    Attributes
    ----------
    df : pandas.DataFrame | polars.DataFrame | pyspark.sql.DataFrame | Table
        The input DataFrame representing the data for the EchoCATE instance.=
    Y: str
        The str representing the column name for the outcome variable.
    T: str
        The str representing the column name(s) for the treatment variable(s).
    X: list[str] | str | None
        The str (if unity) or list/tuple of feature names representing the heterogeneity feature set.
    W: list[str] | str | None
        The str (if unity) or list/tuple of feature names representing the confounder feature set. Only used for fitting nuisance functions.
    uuid: str
        The str representing the column name for the universal identifier code (eg, ehhn)
    discrete_treatment: bool
        A boolean indicating whether the treatment is discrete or continuous.
    _ibis_connection: ibis.client.Client
        The Ibis client object representing the backend connection to Ibis.
    _ibis_df: Table
        The Ibis table expression representing the DataFrame connected to Ibis.
    _table_name: str
        The name of the temporary table/view created for the DataFrame in Ibis.
    _Y: Table
        The outcome variable data as ibis table.
    _T: Table
        The treatment variable data as ibis table.
    _X: Table
        The feature set data as ibis table.
    _estimator: CausalForestDML
        The fitted EconML estimator object.
    """

    __slots__ = [
        "_spark",
        "_ibis_connection",
        "_ibis_df",
        "_table_name",
        "_Y",
        "_T",
        "_X",
        "_estimator",
        "_model_Y_X_W",
        "_model_T_X_W",
        "_model_Y_X_W_T",
        "_cate_models",
        "_validation_estimator",
        "_rscorer",
        "_data_splits",
        "_nuisances_fitted",
        "_validator_results",
        "_final_estimator",
    ]

    @typechecked
    def __init__(
        self,
        df: pandas.DataFrame | polars.DataFrame | pyspark.sql.DataFrame | Table,
        Y: str,
        T: str,
        X: str | list[str],
        W: str | list[str] = [],
        *,
        uuid: str | None = None,
        discrete_treatment: bool = True,
        discrete_outcome: bool = False,
    ):
        self.df = df
        self.uuid = uuid
        self.Y = Y
        self.T = T
        self.X = X
        self.W = W
        self.discrete_treatment = discrete_treatment
        self.discrete_outcome = discrete_outcome
        self._spark = None

        self._ibis_connector()

        if self.uuid is None:
            self._ibis_df = self._ibis_df.mutate(
                uuid=ibis.row_number().over(ibis.window())
            )
            self.uuid = "uuid"

        self._Y = self._ibis_df.select(self.Y)
        self._T = self._ibis_df.select(self.T)
        self._X = self._ibis_df.select(self.X)
        self._W = self._ibis_df.select(self.W) if self.W else None
        self._X_W = self._ibis_df.select(self.X + self.W)
        self._X_W_T = self._ibis_df.select(self.X + self.W + [self.T])

        self._nuisances_fitted = False
        self._validation_estimator = None
        self._final_estimator = None

    @typechecked
    def auto_nuisance_functions(
        self,
        *,
        flaml_Y_kwargs: dict | None = None,
        flaml_T_kwargs: dict | None = None,
        use_ray: bool = False,
        use_spark: bool = False,
    ):
        """
        TODO
        """

        self._model_Y_X_W = self._run_auto_nuisance_functions(
            outcome=self._Y,
            features=self._X_W,
            discrete_outcome=self.discrete_outcome,
            flaml_kwargs=flaml_Y_kwargs,
            use_ray=use_ray,
            use_spark=use_spark,
        )
        self._model_Y_X_W_T = self._run_auto_nuisance_functions(
            outcome=self._Y,
            features=self._X_W_T,
            discrete_outcome=self.discrete_outcome,
            flaml_kwargs=flaml_Y_kwargs,
            use_ray=use_ray,
            use_spark=use_spark,
        )
        self._model_T_X_W = self._run_auto_nuisance_functions(
            outcome=self._T,
            features=self._X_W,
            discrete_outcome=self.discrete_treatment,
            flaml_kwargs=flaml_T_kwargs,
            use_ray=use_ray,
            use_spark=use_spark,
        )

        self._nuisances_fitted = True

    @typechecked
    def fit_validator(
        self,
        *,
        subset_cate_models: list[str] = [
            "LinearDML",
            "NonParamDML",
            "DML-Lasso3d",
            "CausalForestDML",
            "XLearner",
            "DomainAdaptationLearner",
            "SLearner",
            "TLearner",
            "DRLearner",
        ],
        rscorer_kwargs: dict = {},
        use_ray: bool = False,
        ray_remote_func_options_kwargs: dict = {},
    ):
        """
        Fits the econometric model to learn the CATE function.

        Sets the _Y, _T, and _X internal attributes to the data of the outcome, treatment, and feature set,
        respectively. Additionally, sets the _estimator internal attribute to the fitted EconML estimator object.

        Parameters
        ----------
        estimator:
            The estimator to use for fitting the CATE function. Defaults to 'CausalForestDML'. Currently,
            only this option is available.
        automl_Y_kwargs:
            The settings to use for the AutoML model for the outcome. Defaults to None.
        automl_T_kwargs:
            The settings to use for the AutoML model for the treatment. Defaults to None.
        **kwargs:
            Additional keyword arguments to pass to the EconML estimator.

        Returns
        -------
        econml.dml.causal_forest.CausalForestDML:
            The fitted EconML CausalForestDML estimator object if `return_estimator` is True.
        """

        assert self._nuisances_fitted, "find_nuissance_functions() method must be called first to find optimal nussiance functions for estimating CATE models."

        self._split_data(validation_size=0.2, test_size=0.2)
        self._get_cate_models(subset_cate_models=subset_cate_models)
        (
            self._validation_estimator,
            self._rscorer
        ) = self._fit_and_ensemble_cate_models(
            rscorer_settings=rscorer_kwargs,
            use_ray=use_ray,
            ray_remote_func_options_kwargs=ray_remote_func_options_kwargs,
        )

    @typechecked
    def validate(
        self,
        *,
        estimator: BaseCateEstimator | EnsembleCateEstimator | None = None,
        print_full_report: bool = True,
    ):
        """
        Validates the CATE model.

        Returns
        -------
            None
        """

        if estimator is None:
            estimator = self._validation_estimator

        validator = DRTester(
            model_regression=self._model_Y_X_W_T,
            model_propensity=self._model_T_X_W,
            cate=estimator,
        )

        X_test, T_test, Y_test = (
            self._data_splits["X_test"],
            self._data_splits["T_test"],
            self._data_splits["Y_test"],
        )

        X_train, T_train, Y_train = (
            self._data_splits["X_train"],
            self._data_splits["T_train"],
            self._data_splits["Y_train"],
        )

        validator.fit_nuisance(
            X_test, T_test.astype(int), Y_test, X_train, T_train.astype(int), Y_train
        )

        res = validator.evaluate_all(X_test, X_train)

        # Check for insignificant results & warn user
        summary = res.summary()
        if np.array(summary[[c for c in summary.columns if "pval" in c]] > 0.1).any():
            logger.warn(
                "Some of the validation results suggest that the model has not found statistically significant heterogeneity. Please closely look at the validation results and consider retraining with new configurations."
            )
        else:
            logger.info(
                "All validation results suggest that the model has found statistically significant heterogeneity."
            )

        if print_full_report:
            print(summary.to_string())
            for i in res.blp.treatments:
                if i > 0:
                    res.plot_cal(i)
                    res.plot_qini(i)
                    res.plot_toc(i)

        self._validator_results = res

        return res

    @typechecked
    def fit_final(self):
        """
        Fits the final estimator on the entire dataset.
        """

        assert (
            self._validation_estimator
        ), "The best estimator must be fitted first before fitting the final estimator."

        self._final_estimator = copy.deepcopy(self._validation_estimator)

        if isinstance(self._final_estimator, EnsembleCateEstimator):
            for estimator in self._final_estimator._cate_models:
                estimator.fit(
                    Y=self._Y.execute().to_numpy().ravel(),
                    T=self._T.execute().to_numpy().ravel(),
                    X=self._X.execute().to_numpy(),
                )
        else:
            self._final_estimator.fit(
                Y=self._Y.execute().to_numpy().ravel(),
                T=self._T.execute().to_numpy().ravel(),
                X=self._X.execute().to_numpy(),
            )

    @typechecked
    def predict(
        self,
        *,
        out_of_sample_df: pandas.DataFrame
        | polars.DataFrame
        | pyspark.sql.DataFrame
        | Table
        | None = None,
        out_of_sample_uuid: str | None = None,
        return_predictions: bool = False,
        join_predictions: bool = False,
    ):
        """
        Predicts the CATE given feature set.

        Returns
        -------
        tuple:
            A tuple containing the predicted CATE, standard errors, lower bound, and upper bound if `return_predictions` is True.
        """

        assert (
            return_predictions or join_predictions
        ), "Either return_predictions or join_predictions must be set to True."

        assert self._final_estimator, "The final estimator must be fitted first before making predictions. Please run the fit() method with final_estimator=True."

        if out_of_sample_df is None:
            X = self._X.execute().to_numpy()
            uuids = self._ibis_df[self.uuid].execute().to_numpy()
            uuid_col = self.uuid
        else:
            input_df = self._create_internal_ibis_table(df=out_of_sample_df)
            if join_predictions:
                if out_of_sample_uuid is None:
                    try:
                        uuids = input_df[self.uuid].execute().to_numpy()
                        uuid_col = self.uuid
                    except IbisTypeError:
                        raise ValueError(
                            "The `uuid` column must be provided in the out-of-sample DataFrame to join predictions and the `out_of_sample_uuid` argument must be set to the string name of the column."
                        )
                else:
                    uuids = input_df[out_of_sample_uuid].execute().to_numpy()
                    uuid_col = out_of_sample_uuid
            X = input_df.select(self.X).execute().to_numpy()

        cate_predictions = self._validation_estimator.effect(X)

        if join_predictions:
            data_dict = {
                uuid_col: uuids,
                "cate_predictions": cate_predictions,
            }
            results_df = self._create_internal_ibis_table(data_dict=data_dict)
            if out_of_sample_df is None:
                self._ibis_df = self._ibis_df.join(
                    results_df, predicates=uuid_col, how="inner"
                )
            else:
                final_df = input_df.join(results_df, predicates=uuid_col, how="inner")
                return self._return_ibis_dataframe_to_original_backend(
                    ibis_df=final_df, backend=input_df._find_backend().name
                )

        if return_predictions:
            return cate_predictions

    @typechecked
    def rank_order(
        self,
        *,
        out_of_sample_df: pandas.DataFrame
        | polars.DataFrame
        | pyspark.sql.DataFrame
        | Table
        | None = None,
        return_rank_order: bool = False,
        join_rank_order: bool = False,
    ):
        """
        Ranks households based on the those with the highest estimated CATE.

        Returns
        -------
            None
        """

        assert (
            return_rank_order or join_rank_order
        ), "Either return_rank_order or join_rank_order must be set to True."
        assert (
            self._ibis_connection.name != "polars"
        ), "Rank ordering is not supported for polars DataFrames."

        if out_of_sample_df is None:
            assert (
                "cate_predictions" in self._ibis_df.columns
            ), "CATE predictions must be present in the DataFrame to rank order. Please call the predict() method first with join_predictions=True."

            window = ibis.window(order_by=ibis.desc(self._ibis_df["cate_predictions"]))
            self._ibis_df = self._ibis_df.mutate(
                cate_ranking=ibis.row_number().over(window)
            )

            if return_rank_order:
                return self._ibis_df.select("cate_ranking").execute().to_numpy()

            elif join_rank_order:
                self._ibis_df = self._ibis_df.order_by("cate_ranking")

        else:
            input_df = self._create_internal_ibis_table(df=out_of_sample_df)
            assert (
                "cate_predictions" in input_df.columns
            ), "CATE predictions must be present in the DataFrame to rank order. Please call the predict() method first with join_predictions=True, passing the out_of_sample_dataframe."

            window = ibis.window(order_by=ibis.desc(input_df["cate_predictions"]))
            final_df = input_df.mutate(cate_ranking=ibis.row_number().over(window))

            if return_rank_order:
                return final_df.select("cate_ranking").execute().to_numpy()
            elif join_rank_order:
                return self._return_ibis_dataframe_to_original_backend(
                    ibis_df=final_df.order_by("cate_ranking"),
                    backend=input_df._find_backend().name,
                )

    @typechecked
    def summarize(
        self,
        *,
        out_of_sample_df: pandas.DataFrame
        | polars.DataFrame
        | pyspark.sql.DataFrame
        | Table
        | None = None,
    ):
        """
        Provides population summary of treatment effects, including Average Treatment Effects (ATEs)
        and Conditional Average Treatement Effects (CATEs).

        """

        if out_of_sample_df is None:
            df = self._ibis_df
        else:
            df = self._create_internal_ibis_table(df=out_of_sample_df)

        assert (
            "cate_predictions" in df.columns
        ), "CATE predictions must be present in the DataFrame to summarize. Please call the predict() method first with join_predictions=True."

        column = df["cate_predictions"]

        cate_summary_statistics = df.aggregate(
            [
                column.mean().name("cate_mean"),
                column.sum().name("cate_sum"),
                column.std().name("cate_std"),
                column.min().name("cate_min"),
                column.max().name("cate_max"),
                column.count().name("count"),
            ]
        )

        return self._return_ibis_dataframe_to_original_backend(
            ibis_df=cate_summary_statistics
        )

    @typechecked
    def _get_cate_models(self, *, subset_cate_models: list[str]):
        """
        Create model grid for CATE models to be fitted and ensembled.
        """

        mod_Y_X = self._model_Y_X_W
        mod_T_X = self._model_T_X_W
        mod_Y_X_T = self._model_Y_X_W_T

        self._cate_models = [
            (
                "LinearDML",
                LinearDML(
                    model_y=mod_Y_X,
                    model_t=mod_T_X,
                    discrete_treatment=self.discrete_treatment,
                    discrete_outcome=self.discrete_outcome,
                    cv=3,
                ),
            ),
            (
                "NonParamDML",
                NonParamDML(
                    model_y=mod_Y_X,
                    model_t=mod_T_X,
                    model_final=mod_Y_X_T,
                    discrete_treatment=self.discrete_treatment,
                    discrete_outcome=self.discrete_outcome,
                    cv=3,
                ),
            ),
            (
                "DML-Lasso3d",
                DML(
                    model_y=mod_Y_X,
                    model_t=mod_T_X,
                    model_final=LassoCV(),
                    discrete_treatment=self.discrete_treatment,
                    discrete_outcome=self.discrete_outcome,
                    featurizer=PolynomialFeatures(degree=3),
                    cv=3,
                ),
            ),
            (
                "CausalForestDML",
                CausalForestDML(
                    model_y=mod_Y_X,
                    model_t=mod_T_X,
                    discrete_treatment=self.discrete_treatment,
                    discrete_outcome=self.discrete_outcome,
                    cv=3,
                ),
            ),
        ]
        if self.discrete_treatment:
            self._cate_models.append(
                (
                    "XLearner",
                    XLearner(
                        models=mod_Y_X_T,
                        cate_models=mod_Y_X_T,
                        propensity_model=mod_T_X,
                    ),
                )
            )
            self._cate_models.append(
                (
                    "DomainAdaptationLearner",
                    DomainAdaptationLearner(
                        models=mod_Y_X, final_models=mod_Y_X_T, propensity_model=mod_T_X
                    ),
                )
            )
            self._cate_models.append(("SLearner", SLearner(overall_model=mod_Y_X_T)))
            self._cate_models.append(("TLearner", TLearner(models=mod_Y_X_T)))
            self._cate_models.append(
                (
                    "DRLearner",
                    DRLearner(
                        model_propensity=mod_T_X,
                        model_regression=mod_Y_X_T,
                        model_final=mod_Y_X_T,
                        cv=3,
                    ),
                )
            )

        self._cate_models = [m for m in self._cate_models if m[0] in subset_cate_models]

    @typechecked
    def _fit_and_ensemble_cate_models(
        self,
        *,
        rscorer_settings: dict,
        use_ray: bool,
        ray_remote_func_options_kwargs: dict,
    ):
        """
        Fits the CATE models and ensembles them.

        Returns
        -------
        """

        Y_train, T_train, X_train = (
            self._data_splits["Y_train"],
            self._data_splits["T_train"],
            self._data_splits["X_train"],
        )

        Y_val, T_val, X_val = (
            self._data_splits["Y_val"],
            self._data_splits["T_val"],
            self._data_splits["X_val"],
        )

        def fit_model(name, model, use_ray, ray_remote_func_options_kwargs):
            if isinstance(model, _OrthoLearner):
                model.use_ray = use_ray
                model.ray_remote_func_options_kwargs = ray_remote_func_options_kwargs
            if name == "CausalForestDML":
                return name, model.tune(Y=Y_train, T=T_train, X=X_train).fit(
                    Y=Y_train, T=T_train, X=X_train
                )
            return name, model.fit(Y=Y_train, T=T_train, X=X_train)

        if use_ray:
            ray.init(ignore_reinit_error=True)

            fit_model = ray.remote(fit_model).options(**ray_remote_func_options_kwargs)
            futures = [
                fit_model.remote(
                    name,
                    model,
                    use_ray=True,
                    ray_remote_func_options_kwargs=ray_remote_func_options_kwargs,
                )
                for name, model in self._cate_models
            ]
            models = ray.get(futures)
        else:
            models = Parallel(n_jobs=-1)(
                delayed(fit_model)(name, model) for name, model in self._cate_models
            )

        base_rscorer_settings = {
            "cv": 3,
            "mc_iters": 3,
            "mc_agg": "median",
        }

        if rscorer_settings is not None:
            base_rscorer_settings.update(rscorer_settings)

        rscorer = RScorer(
            model_y=self._model_Y_X_W,
            model_t=self._model_T_X_W,
            discrete_treatment=self.discrete_treatment,
            **base_rscorer_settings,
        )

        rscorer.fit(Y_val, T_val, X_val)

        ensemble_estimator, ensemble_score, estimator_scores = rscorer.ensemble(
            [mdl for _, mdl in models], return_scores=True
        )

        logger.info(f"Ensemble Estimator RScore: {ensemble_score}")
        logger.info(
            f"Inidividual Estimator RScores: {dict(zip([n[0] for n in models],estimator_scores))}"
        )

        # Choose best estimator
        def get_validation_estimator(
            ensemble_estimator, ensemble_score, estimator_scores
        ):
            if np.max(estimator_scores) >= ensemble_score:
                logger.info(
                    "The best estimator is greater than the ensemble estimator. Returning that individual estimator."
                )
                best_estimator = ensemble_estimator._cate_models[
                    np.argmax(estimator_scores)
                ]
            else:
                logger.info(
                    "The ensemble estimator is the best estimator, filtering models with weights less than 0.01."
                )
                estimator_weight_map = dict(
                    zip(ensemble_estimator._cate_models, ensemble_estimator._weights)
                )
                ensemble_estimator._cate_models = [
                    k for k, v in estimator_weight_map.items() if v > 0.01
                ]
                ensemble_estimator._weights = np.array(
                    [v for _, v in estimator_weight_map.items() if v > 0.01]
                )
                best_estimator = ensemble_estimator

            return best_estimator

        best_estimator = get_validation_estimator(
            ensemble_estimator, ensemble_score, estimator_scores
        )

        return best_estimator, rscorer
