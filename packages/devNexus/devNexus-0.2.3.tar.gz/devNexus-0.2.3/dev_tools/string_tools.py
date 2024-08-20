from datetime import date


def replace_path_separator(path):
    """
    Replace '/' with '\\' in a string.

    :param path: The input path.
    :return: Path with replaced separators.
    """
    return path.replace('/', '\\')


def get_date_as_string(date_to_convert):
    return date_to_convert.strftime("%d-%m-%Y")


def get_today_as_string():
    return get_date_as_string(date.today())


def extract_text_between_substrings(s, start, end):
    """
    Extract text between two substrings.

    :param s: Input string.
    :param start: Starting substring.
    :param end: Ending substring.
    :return: Extracted text.
    """
    return s[s.find(start) + len(start):s.rfind(end)].strip()


def extract_text_after_delimiter(s, delimiter):
    """
    Extract text after a specified delimiter.

    :param s: Input string.
    :param delimiter: Delimiter to search for.
    :return: Text after the delimiter.
    """
    return s.partition(delimiter)[2].strip()


def extract_text_around_keyword(s, keyword, extract_before=True):
    """
    Extract text around a keyword.

    :param s: Input string.
    :param keyword: Keyword to search for.
    :param extract_before: True to extract text before the keyword, False to extract text after the keyword.
    :return: Extracted text.
    """
    before, _, after = s.partition(keyword)
    return before if extract_before else after
