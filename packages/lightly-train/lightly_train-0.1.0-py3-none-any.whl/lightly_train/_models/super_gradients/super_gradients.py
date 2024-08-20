from __future__ import annotations

from abc import ABC, abstractmethod

from torch.nn import Module

from lightly_train._models.feature_extractor import FeatureExtractor


class SuperGradientsFeatureExtractor(ABC, FeatureExtractor):
    @classmethod
    @abstractmethod
    def is_supported_model_cls(cls, model_cls: type[Module]) -> bool: ...

    @classmethod
    @abstractmethod
    def supported_model_classes(cls) -> tuple[type[Module], ...]: ...
