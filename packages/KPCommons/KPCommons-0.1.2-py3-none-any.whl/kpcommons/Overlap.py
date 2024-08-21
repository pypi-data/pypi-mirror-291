from dataclasses import dataclass


@dataclass
class Overlap:
    """
    An overlap with a start and end position, a length, and overlap ratios.
    The length can be negative if there is no overlap.
    """

    start: int
    end: int
    length: int
    ratio_1: float
    ratio_2: float
