import pyperclip


def get_multiline_clipboard_content_as_list():
    """
    Return an array from multiline text in the clipboard, cleaning leading and trailing whitespaces.

    :return: Array of cleaned lines.
    """
    text = paste_from_clipboard()
    return [line.strip() for line in text.split("\n") if line.strip()]


def copy_to_clipboard(text):
    """
    Copy the given text to the system clipboard.

    :param text: Text to be copied.
    """
    pyperclip.copy(text)


def paste_from_clipboard():
    """
    Paste text from the system clipboard.

    :return: Text from the clipboard.
    """
    return pyperclip.paste()


def clear_clipboard():
    """
    Clear the system clipboard.
    """
    pyperclip.copy('')
