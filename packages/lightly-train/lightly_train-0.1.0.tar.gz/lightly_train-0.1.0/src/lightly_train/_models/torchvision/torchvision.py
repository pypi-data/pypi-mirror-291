from __future__ import annotations

from torch.nn import Module

from lightly_train._models.feature_extractor import FeatureExtractor


class TorchvisionFeatureExtractor(FeatureExtractor):
    _torchvision_models: list[type[Module]]
    # Regex pattern for matching model names.
    _torchvision_model_name_pattern: str
