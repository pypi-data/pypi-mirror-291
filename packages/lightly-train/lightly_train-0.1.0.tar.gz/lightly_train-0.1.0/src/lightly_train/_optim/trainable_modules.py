from dataclasses import dataclass
from typing import Iterable

from torch.nn import Module


@dataclass
class TrainableModules:
    modules: Iterable[Module]
    modules_no_weight_decay: Iterable[Module] = ()
