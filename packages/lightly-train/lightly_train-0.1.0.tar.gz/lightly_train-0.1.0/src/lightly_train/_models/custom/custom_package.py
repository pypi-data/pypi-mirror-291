from __future__ import annotations

from torch.nn import Module

from lightly_train._models.custom.custom import CustomFeatureExtractor
from lightly_train._models.feature_extractor import FeatureExtractor
from lightly_train._models.package import Package


class CustomPackage(Package):
    name = "custom"

    @classmethod
    def list_model_names(cls) -> list[str]:
        return []

    @classmethod
    def is_supported_model(cls, model: Module) -> bool:
        return (
            hasattr(model, "num_features")
            and hasattr(model, "forward_features")
            and hasattr(model, "forward_pool")
        )

    @classmethod
    def get_model(cls, model_name: str) -> Module:
        raise NotImplementedError()

    @classmethod
    def get_feature_extractor_cls(cls, model: Module) -> type[FeatureExtractor]:
        return CustomFeatureExtractor


# Create singleton instance of the package. The singleton should be used whenever
# possible.
CUSTOM_PACKAGE = CustomPackage()
