from __future__ import annotations

import inspect

from torch.nn import Module

from lightly_train._models.feature_extractor import FeatureExtractor
from lightly_train._models.package import Package
from lightly_train._models.timm.timm import TIMMFeatureExtractor


class TIMMPackage(Package):
    name = "timm"

    @classmethod
    def list_model_names(cls) -> list[str]:
        try:
            import timm
        except ImportError:
            return []
        return [f"{cls.name}/{model_name}" for model_name in timm.list_models()]

    @classmethod
    def is_supported_model(cls, model: Module) -> bool:
        # Get the class hierarchy (MRO: Method Resolution Order) and check if
        # any of the (super)classes are from the timm package.
        class_hierarchy = inspect.getmro(model.__class__)
        return any(_cls.__module__.startswith(cls.name) for _cls in class_hierarchy)

    @classmethod
    def get_model(cls, model_name: str) -> Module:
        try:
            import timm
        except ImportError:
            raise ValueError(
                f"Cannot create model '{model_name}' because timm is not installed."
            )
        return timm.create_model(model_name, pretrained=False)

    @classmethod
    def get_feature_extractor_cls(cls, model: Module) -> type[FeatureExtractor]:
        return TIMMFeatureExtractor


# Create singleton instance of the package. The singleton should be used whenever
# possible.
TIMM_PACKAGE = TIMMPackage()
