from abc import ABC, abstractmethod
from typing import List

from kpcommons.chunker.Chunk import Chunk


class BaseChunker(ABC):

    @abstractmethod
    def chunk(self, text: str) -> List[Chunk]:
        pass
