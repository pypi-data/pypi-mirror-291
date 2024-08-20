from dataclasses import dataclass

from lightly_train._configs.config import Config


@dataclass
class MethodArgs(Config):
    """Arguments for a method.

    This does not include optimizer or scheduler arguments.
    """

    pass
