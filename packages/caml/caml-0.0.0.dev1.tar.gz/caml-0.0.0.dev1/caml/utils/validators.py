# from typing import Any
# from functools import wraps
# import logging

# logger = logging.getLogger(__name__)

# class TypeValidator:
#     def __init__(self, name: str, expected_type: Any | list[Any], strict: bool = False):
#         self.name = name
#         self.private_name = f"_{name}_stored"
#         self.expected_type = expected_type
#         self.strict = strict

#     def __get__(self, instance, owner):
#         return getattr(instance, self.private_name)

#     def __set__(self, instance, value):

#         expected_type = self.expected_type if isinstance(self.expected_type, list) else [self.expected_type]
#         for t in expected_type:
#             if t is None and self.strict:
#                 raise ValueError("Value must not be None.")
#             if not self.strict and value is None:
#                 setattr(instance, self.private_name, None)
#                 return
#             if isinstance(value, t):
#                 setattr(instance, self.private_name, value)
#                 return
#         raise ValueError(f"Value must be of type(s) {expected_type}.")

#     def __delete__(self, instance):
#         raise AttributeError(f"Cannot delete attribute {self.name}.")

# def enforce_types(**expected_types_kwargs):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(self, *args, **kwargs):
#             # Check keyword arguments
#             for key, expected_type in expected_types_kwargs.items():
#                 if key in kwargs:
#                     value = kwargs[key]
#                     if isinstance(expected_type, (list, tuple)):
#                         if None in expected_type:
#                             if value is None:
#                                 pass
#                             else:
#                                 expected_type.remove(None)
#                                 if not any(isinstance(value, t) for t in expected_type):
#                                     raise ValueError(f"Keyword argument '{key}' must be one of the types {expected_type}, but got {type(value).__name__}.")
#                     else:
#                         if not isinstance(value, expected_type):
#                             raise ValueError(f"Keyword argument '{key}' must be of type {expected_type.__name__}, but got {type(value).__name__}.")

#             return func(self, *args, **kwargs)
#         return wrapper
#     return decorator
