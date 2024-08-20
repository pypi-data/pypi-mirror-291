from __future__ import annotations

from abc import ABC, abstractmethod

from torch.nn import Module

from lightly_train._models.feature_extractor import FeatureExtractor


class Package(ABC):
    """Interface for a package that provides models and feature extractors that are
    compatible with lightly_train.

    Every package must implement this interface.
    """

    name: str  # The name of the package.

    @classmethod
    @abstractmethod
    def list_model_names(cls) -> list[str]:
        """List all supported models by this package."""
        ...

    @classmethod
    @abstractmethod
    def is_supported_model(cls, model: Module) -> bool:
        """Check if the model is supported by this package."""
        ...

    @classmethod
    @abstractmethod
    def get_model(cls, model_name: str) -> Module:
        """Get the model by name.

        Assumes that the model is supported by the package.
        """
        ...

    @classmethod
    @abstractmethod
    def get_feature_extractor_cls(cls, model: Module) -> type[FeatureExtractor]:
        """Get the feature extractor class for the model from this package.

        Assumes that the model is supported by the package.
        """
        ...
