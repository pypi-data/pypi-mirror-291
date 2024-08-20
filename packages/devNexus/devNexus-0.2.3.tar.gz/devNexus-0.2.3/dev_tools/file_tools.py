import os
import shutil

from dir_tools import list_subdirectories


def count_word_in_file(file_path, word):
    """
    Count occurrences of a word in a file.

    :param file_path: Path to the file.
    :param word: Word to count.
    :return: Number of occurrences.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read().count(word)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return 0


def delete_file(file_path):
    """
    Delete a file at the specified path.

    :param file_path: Path to the file to be deleted.
    """
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except PermissionError:
        print(f"Permission denied to delete '{file_path}'.")


def format_filename_to_title_case(filename):
    """
    Replace _, ., and - in a file name with space and transform it to title case.

    :param filename: The input filename.
    :return: Title-cased filename.
    """
    name, ext = os.path.splitext(filename)
    clean_name = name.replace('_', ' ').replace('.', ' ').replace('-', ' ').title()
    return f'{clean_name}{ext}'


def extract_filename_from_path(path, include_extension=True):
    """
    Return the filename from a given path.

    :param path: The input file path.
    :param include_extension: True to return the file name with extension.
    :return: The file name or file name with extension.
    """
    return os.path.basename(path) if include_extension else os.path.splitext(os.path.basename(path))[0]


def normalize_all_filenames_in_folder(folder_path):
    """
    Normalize all the filenames in a folder.

    :param folder_path: Path to folder containing the files.
    :return: A list of dictionaries containing before and after names.
    """
    modifications = []
    try:
        filenames = os.listdir(folder_path)
    except FileNotFoundError:
        print(f"Folder '{folder_path}' does not exist")
        return modifications

    for file in filenames:
        old_name = os.path.join(folder_path, file)
        new_name = os.path.join(folder_path, format_filename_to_title_case(file))
        try:
            os.rename(old_name, new_name)
        except FileExistsError:
            print(f"Cannot rename '{old_name}' to '{new_name}': file with the same name already exists")
            continue
        modifications.append({'before': old_name, 'after': new_name})
    return modifications


def prepend_line_to_file_start(file_path, line):
    """
    Insert given line as a new line at the beginning of a file.

    :param file_path: Path to the file.
    :param line: Line to be added.
    """
    dummy_file = file_path + '.bak'
    try:
        with open(file_path, 'r') as read_file, open(dummy_file, 'w') as write_file:
            write_file.write(line + '\n')
            shutil.copyfileobj(read_file, write_file)
        os.replace(dummy_file, file_path)
    except FileNotFoundError:
        print(f"File '{file_path}' does not exist")


def prepend_lines_from_file_to_file_start(file_path, source_file, check_line):
    """
    Insert given lines from a source file at the beginning of a target file.

    :param file_path: Path to the target file.
    :param source_file: Path to the source file.
    :param check_line: Line to check for existing content.
    :raises FileNotFoundError: If the target or source file does not exist.
    :raises PermissionError: If there are permission issues with reading or writing files.
    :raises IOError: For any other IO-related errors.
    :raises Exception: For general errors such as existing content.
    """
    dummy_file = file_path + '.bak'

    try:
        with open(file_path, 'r') as read_file, open(dummy_file, 'w') as write_file:
            if read_file.readline().strip() == check_line:
                raise ValueError('Content already exists in the target file.')

            with open(source_file, 'r') as source:
                write_file.writelines(source.readlines())

            read_file.seek(0)
            shutil.copyfileobj(read_file, write_file)

        os.replace(dummy_file, file_path)

    except FileNotFoundError as e:
        print(f"File error: {e}")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except IOError as e:
        print(f"IO error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Clean up dummy file if it exists
        if os.path.exists(dummy_file):
            os.remove(dummy_file)


def prepend_lines_to_all_files_with_extension(folder_path, source_file, extension, check_line):
    """
    Insert text from a source file to all files in a folder with a specific extension.

    :param folder_path: Path to the folder.
    :param source_file: Path to the source file.
    :param extension: File extension to match.
    :param check_line: Line to check for existing content.
    """
    for file in folder_path:
        if file.endswith(f".{extension}"):
            file_path = os.path.join(folder_path, file)
            try:
                prepend_lines_from_file_to_file_start(file_path, source_file, check_line)
            except Exception as e:
                print(e)
                continue


def prepend_lines_to_all_files_in_subdirectories(folder_path, source_file, extension, check_line):
    """
    Insert text from a source file to all files in all subfolders with a specific extension.

    :param folder_path: Path to the root folder.
    :param source_file: Path to the source file.
    :param extension: File extension to match.
    :param check_line: Line to check for existing content.
    """
    prepend_lines_to_all_files_with_extension(folder_path, source_file, extension, check_line)
    for subfolder in list_subdirectories(folder_path):
        prepend_lines_to_all_files_with_extension(subfolder, source_file, extension, check_line)


def move_file_to_destination(src_path, dest_path):
    """
    Move a file from one location to another.
    """
    shutil.move(src_path, dest_path)
    print(f"File '{os.path.basename(src_path)}' moved to '{dest_path}'.")


def copy_file_to_destination(src_path, dest_path):
    """
    Copy a file from one location to another.
    """
    shutil.copy2(src_path, dest_path)
    print(f"File '{os.path.basename(src_path)}' copied to '{dest_path}'.")


def replace_text_in_file(file_path, old_text, new_text):
    """
    Replace all occurrences of a text in a file.
    """
    try:
        with open(file_path, 'r') as file:
            file_data = file.read()
        new_data = file_data.replace(old_text, new_text)
        with open(file_path, 'w') as file:
            file.write(new_data)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")


def join_os_path_parts(part1, part2):
    """
    Create an OS path string by joining two strings using the OS separator.
    """
    return os.path.join(part1, part2)


def replace_path_separator(path):
    """
    Replace '/' with '\\' in a string.
    """
    return path.replace('/', '\\')
