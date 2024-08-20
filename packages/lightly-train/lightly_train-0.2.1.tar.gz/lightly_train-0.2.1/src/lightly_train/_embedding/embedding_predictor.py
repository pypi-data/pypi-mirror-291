from __future__ import annotations

from pytorch_lightning import LightningModule
from torch import Tensor
from torch.nn import Flatten

from lightly_train._models.embedding_model import EmbeddingModel
from lightly_train.types import SingleViewBatch


class EmbeddingPredictor(LightningModule):
    """PyTorch Lightning module for "predicting" embeddings.

    This module uses the `predict_step` to extract embeddings from the given
    embedding model.

    Args:
        embedding_model: The embedding model.
    """

    def __init__(self, embedding_model: EmbeddingModel):
        super().__init__()
        self.embedding_model = embedding_model
        self.flatten = Flatten(start_dim=1)

    def forward(self, x: Tensor) -> Tensor:
        x = self.embedding_model(x)
        x = self.flatten(x)
        return x

    def predict_step(
        self, batch: SingleViewBatch, batch_idx: int
    ) -> tuple[Tensor, list[str]]:
        x = batch[0]
        filenames = batch[-1]
        embeddings = self(x)
        return embeddings, filenames
