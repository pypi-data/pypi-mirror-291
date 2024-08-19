from pathlib import Path
from os.path import join
import re
from kpcommons.DateProvider import DateProvider
from kpcommons.NowDateProvider import NowDateProvider
from kpcommons.Overlap import Overlap


def get_namespace(tag: str) -> str:
    """
    Gets the namespace from a root tag of a xml file.
    :param tag: The tag
    :return: The namespace
    """
    m = re.match(r'{.*}', tag)
    return m.group(0) if m else ''


def create_dated_folder(folder_path: str, date_provider:DateProvider = NowDateProvider(),
                        name_format:str = '%Y_%m_%d_%H_%M_%S') -> None:
    """
    Creates a subfolder with a date as the name.
    :param folder_path: The path of the folder in which to create the new folder
    :param date_provider: A :class:`DateProvider`. By default, this is a :class:`NowDateProvider`
    :param name_format: Format to use to for the name of the folder
    """
    date = date_provider.get_date()
    date_time_string = date.strftime(name_format)
    folder_path = join(folder_path, date_time_string)
    Path(folder_path).mkdir(parents=True, exist_ok=True)

def calculate_overlap(start_1: int, end_1: int, start_2: int, end_2: int) -> Overlap:
    """
    Calculates the overlap between two ranges.
    :param start_1: Start of the first range
    :param end_1: End of the first range
    :param start_2: Start of the second range
    :param end_2: End of the second range
    :return: An :class:`Overlap`
    """
    __check_values(start_1, end_1, start_2, end_2)

    overlap_start = max(start_1, start_2)
    overlap_end = min(end_1, end_2)
    overlap_length = overlap_end - overlap_start

    overlap_ratio_1 = 0
    overlap_ratio_2 = 0

    if overlap_length > 0:
        overlap_ratio_1 = overlap_length / (end_1 - start_1)
        overlap_ratio_2 = overlap_length / (end_2 - start_2)

    return Overlap(overlap_start, overlap_end, overlap_length, overlap_ratio_1, overlap_ratio_2)


def __check_values(start_1: int, end_1: int, start_2: int, end_2: int):

    if start_1 == end_1 or start_2 == end_2:
        raise ValueError(f'Start and end are the same')

    if start_1 > end_1:
        raise ValueError(f'Start value ({start_1}) is greater end value ({end_1})')

    if start_2 > end_2:
        raise ValueError(f'Start value ({start_2}) is greater end value ({end_2})')
