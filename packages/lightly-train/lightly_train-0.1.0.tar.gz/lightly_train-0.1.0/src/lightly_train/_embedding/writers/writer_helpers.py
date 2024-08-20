from pathlib import Path

from lightly_train._embedding.embedding_format import EmbeddingFormat
from lightly_train._embedding.writers.csv_writer import CSVWriter
from lightly_train._embedding.writers.embedding_writer import EmbeddingWriter
from lightly_train._embedding.writers.torch_writer import TorchWriter


def get_writer(format: EmbeddingFormat, filepath: Path) -> EmbeddingWriter:
    if CSVWriter.is_supported_format(format):
        return CSVWriter(filepath=filepath, format=format)
    elif TorchWriter.is_supported_format(format):
        return TorchWriter(filepath=filepath)
    else:
        raise ValueError(f"Unsupported embedding format: '{format}'")
