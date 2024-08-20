import abc
import logging

import ibis
import pandas
import polars
import pyspark
from flaml import AutoML
from pyspark.sql import SparkSession
from sklearn.model_selection import train_test_split
from typeguard import typechecked

from ..utils import generate_random_string

logger = logging.getLogger(__name__)


class CamlBase(metaclass=abc.ABCMeta):
    """
    Base ABC class for core classes.
    """

    @property
    def dataframe(self):
        return self._return_ibis_dataframe_to_original_backend(ibis_df=self._ibis_df)

    @property
    def validation_estimator(self):
        if self._validation_estimator is not None:
            logger.info("The validation estimator has been fit and will be returned.")
            return self._validation_estimator
        else:
            raise ValueError(
                "No validation estimator has been fit yet. Please run fit_validator() method first."
            )

    @property
    def final_estimator(self):
        if self._final_estimator is not None:
            logger.info(
                "The final estimator has been fit on the entire dataset and will be returned."
            )
            return self._final_estimator
        else:
            raise ValueError(
                "No final estimator has been fit yet. Please run fit_final() method first."
            )

    @abc.abstractmethod
    def fit_validator(self):
        pass

    @abc.abstractmethod
    def validate(self):
        pass
    
    @abc.abstractmethod
    def fit_final(self):
        pass

    @abc.abstractmethod
    def predict(self):
        pass

    @abc.abstractmethod
    def rank_order(self):
        pass

    @abc.abstractmethod
    def summarize(self):
        pass

    @typechecked
    def _split_data(
        self, *, validation_size: float | None = None, test_size: float = 0.2
    ):
        """
        Splits the data into training, validation, and test sets.

        """
        X = self._X.execute().to_numpy()
        Y = self._Y.execute().to_numpy().ravel()
        T = self._T.execute().to_numpy().ravel()

        X_train, X_test, T_train, T_test, Y_train, Y_test = train_test_split(
            X, T, Y, test_size=test_size
        )

        self._data_splits = {
            "X_train": X_train,
            "X_test": X_test,
            "T_train": T_train,
            "T_test": T_test,
            "Y_train": Y_train,
            "Y_test": Y_test,
        }

        if validation_size:
            X_train, X_val, T_train, T_val, Y_train, Y_val = train_test_split(
                X_train, T_train, Y_train, test_size=validation_size
            )

            self._data_splits["X_val"] = X_val
            self._data_splits["T_val"] = T_val
            self._data_splits["Y_val"] = Y_val
            self._data_splits["X_train"] = X_train
            self._data_splits["T_train"] = T_train
            self._data_splits["Y_train"] = Y_train

    @typechecked
    def _run_auto_nuisance_functions(
        self,
        *,
        outcome: ibis.expr.types.Table,
        features: ibis.expr.types.Table,
        discrete_outcome: bool,
        flaml_kwargs: dict | None,
        use_ray: bool,
        use_spark: bool,
    ):
        """
        Automatically selects the best nuisance models for the outcome and treatment.

        """

        automl = AutoML()

        base_settings = {
            "n_jobs": -1,
            "log_file_name": "",
            "seed": 123,
            "time_budget": 300,
            "early_stop": "True",
            "eval_method": "cv",
            "n_splits": 3,
            "starting_points": "static",
            "estimator_list": ["lgbm", "rf", "xgboost", "extra_tree", "xgb_limitdepth"],
        }

        _flaml_kwargs = base_settings.copy()

        if discrete_outcome:
            _flaml_kwargs["task"] = "classification"
            _flaml_kwargs["metric"] = "log_loss"
        else:
            _flaml_kwargs["task"] = "regression"
            _flaml_kwargs["metric"] = "mse"

        if self._spark or use_spark:
            _flaml_kwargs["use_spark"] = True
            _flaml_kwargs["n_concurrent_trials"] = 4
        elif use_ray:
            _flaml_kwargs["use_ray"] = True
            _flaml_kwargs["n_concurrent_trials"] = 4

        if flaml_kwargs is not None:
            _flaml_kwargs.update(flaml_kwargs)

        # Fit the AutoML models
        outcome_array = outcome.execute().to_numpy().ravel()
        features_matrix = features.execute().to_numpy()

        automl.fit(features_matrix, outcome_array, **_flaml_kwargs)

        model = automl.model.estimator

        return model

    @typechecked
    def _ibis_connector(
        self,
        custom_table_name: str | None = None,
    ):
        """
        Connects the DataFrame to the Ibis backend based on the type of DataFrame.

        If the DataFrame is a pyspark.sql.DataFrame, it creates a temporary view and connects to Ibis using the PySpark session.
        If the DataFrame is a pandas.DataFrame, it connects to Ibis using the pandas DataFrame.
        If the DataFrame is a polars.DataFrame, it connects to Ibis using the polars DataFrame.
        If the DataFrame is an ibis.expr.types.Table, it creates a new table (copy of df) on Ibis using the current Ibis connection.

        This method sets the '_table_name`, '_ibis_df` and `_ibis_connection` internal attributes of the class when nonbase_df is None.

        Parameters
        ----------
        custom_table_name:
            The custom table name to use for the DataFrame in Ibis, by default None

        Returns
        -------
        str | None
            The table name of the DataFrame in Ibis if nonbase_df is not None, else None
        ibis.expr.types.Table | None
            The Ibis table expression of the DataFrame if nonbase_df is not None, else None
        ibis.client.Client | None
            The Ibis client object if nonbase_df is not None, else None
        """
        if custom_table_name is None:
            table_name = generate_random_string(10)
        else:
            table_name = custom_table_name

        if isinstance(self.df, pyspark.sql.DataFrame):
            self._spark = SparkSession.builder.getOrCreate()
            self.df.createOrReplaceTempView(table_name)
            ibis_connection = ibis.pyspark.connect(session=self._spark)
            ibis_df = ibis_connection.table(table_name)
        elif isinstance(self.df, pandas.DataFrame):
            ibis_connection = ibis.pandas.connect({table_name: self.df})
            ibis_df = ibis_connection.table(table_name)
        elif isinstance(self.df, polars.DataFrame):
            ibis_connection = ibis.polars.connect({table_name: self.df})
            ibis_df = ibis_connection.table(table_name)
        elif isinstance(self.df, ibis.expr.types.Table):
            ibis_connection = self.df._find_backend()
            if isinstance(ibis_connection, ibis.backends.pyspark.Backend):
                obj = self.df
            else:
                obj = self.df.execute()
            ibis_df = ibis_connection.create_view(name=table_name, obj=obj)

        self._table_name = table_name
        self._ibis_df = ibis_df
        self._ibis_connection = ibis_connection

    @typechecked
    def _create_internal_ibis_table(
        self,
        data_dict: dict | None = None,
        df: ibis.expr.types.Table
        | pyspark.sql.DataFrame
        | pandas.DataFrame
        | polars.DataFrame
        | None = None,
    ):
        """
        Create an internal Ibis DataFrame based on the provided data dictionary.

        Args:
            data_dict (dict): A dictionary containing the data for the DataFrame.

        Returns:
            ibis_results_df: The created Ibis DataFrame.
        """

        table_name = generate_random_string(10)

        backend = self._ibis_connection.name

        if backend == "pandas":
            if data_dict:
                df = pandas.DataFrame(data_dict)
            ibis_df = self._ibis_connection.create_table(name=table_name, obj=df)

        elif backend == "polars":
            if data_dict:
                df = polars.from_dict(data_dict)
            ibis_df = self._ibis_connection.create_table(name=table_name, obj=df)
        elif backend == "pyspark":
            if data_dict:
                df = self._spark.createDataFrame(pandas.DataFrame(data_dict))

            df.createOrReplaceTempView(table_name)
            ibis_df = self._ibis_connection.table(table_name)

        return ibis_df

    @typechecked
    @staticmethod
    def _return_ibis_dataframe_to_original_backend(
        *, ibis_df: ibis.expr.types.Table, backend: str | None = None
    ):
        """
        Return the Ibis DataFrame to the original backend.

        Args:
            ibis_df: The Ibis DataFrame to return to the original backend.

        Returns:
            df: The DataFrame in the original backend.
        """

        if backend is None:
            backend = ibis_df._find_backend().name

        if backend == "pandas":
            df = ibis_df.to_pandas()
        elif backend == "polars":
            df = ibis_df.to_polars()
        elif backend == "pyspark":
            spark = SparkSession.builder.getOrCreate()
            df = spark.sql(ibis_df.compile())

        return df
