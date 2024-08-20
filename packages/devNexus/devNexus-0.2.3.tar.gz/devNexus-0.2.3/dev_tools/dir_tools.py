import os
import shutil
from datetime import datetime


def get_directory_size(directory_path):
    """
    Calculate the total size of a directory.

    :param directory_path: Path to the directory.
    :return: Total size of the directory in bytes.
    """
    total_size = 0
    for dir_path, dir_names, filenames in os.walk(directory_path):
        for f in filenames:
            fp = os.path.join(dir_path, f)
            total_size += os.path.getsize(fp)
    return total_size


def search_files_by_extension(directory_path, extension):
    """
    Search for files with a specific extension in a directory.

    :param directory_path: Path to the directory.
    :param extension: File extension to search for.
    :return: List of file paths with the specified extension.
    """
    return [os.path.join(root, file)
            for root, dirs, files in os.walk(directory_path)
            for file in files if file.endswith(f".{extension}")]


def list_all_files(directory_path):
    """
    List all files in a directory and its subdirectories.

    :param directory_path: Path to the directory.
    :return: List of all file paths.
    """
    return [os.path.join(root, file)
            for root, dirs, files in os.walk(directory_path)
            for file in files]


def extract_folder_path_from_filepath(filepath):
    """
    Extract the folder path from a given file path.

    :param filepath: The input file path.
    :return: Folder path.
    """
    return os.path.dirname(filepath)


def create_new_directory(parent_dir, directory):
    """
    Create a new directory if it doesn't exist.

    :param parent_dir: The parent directory.
    :param directory: The name of the new directory.
    :return: The path of the created directory.
    """
    path = os.path.join(parent_dir, directory)
    os.makedirs(path, exist_ok=True)
    return path


def list_subdirectories(rootdir):
    """
    Return a list of all the subdirectories in the root directory.

    :param rootdir: Root directory to start the search.
    :return: List of subdirectories.
    """
    try:
        return [os.path.join(root, name) for root, dirs, _ in os.walk(rootdir) for name in dirs]
    except FileNotFoundError:
        print(f"Directory '{rootdir}' does not exist")
        return []


def delete_directory(directory_path):
    """
    Delete a directory at the specified path.

    :param directory_path: Path to the directory to be deleted.
    """
    try:
        shutil.rmtree(directory_path)
        print(f"Directory '{directory_path}' deleted.")
    except FileNotFoundError:
        print(f"Directory '{directory_path}' not found.")
    except PermissionError:
        print(f"Permission denied to delete '{directory_path}'.")


def join_os_path_parts(part1, part2):
    """
    Create an OS path string by joining two strings using the OS separator.

    :param part1: The first part of the path.
    :param part2: The second part of the path.
    :return: The OS path string.
    """
    return os.path.join(part1, part2)


def check_if_folder_exists(path):
    """
    Check if a folder exists at the specified path.

    :param path: The path to check for the folder.
    :return: True if the folder exists, False otherwise.
    """
    return os.path.isdir(path)


def replace_text_in_file(file_path, old_text, new_text):
    """
    Replace all occurrences of a text in a file.

    :param file_path: Path to the file.
    :param old_text: Text to be replaced.
    :param new_text: Text to replace with.
    """
    try:
        with open(file_path, 'r') as file:
            file_data = file.read()
        new_data = file_data.replace(old_text, new_text)
        with open(file_path, 'w') as file:
            file.write(new_data)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")


def list_files_with_size(directory_path):
    """
    List files in a directory with their sizes.

    :param directory_path: Path to the directory.
    :return: List of tuples containing file names and their sizes.
    """
    try:
        return [(file, os.path.getsize(os.path.join(directory_path, file)))
                for file in os.listdir(directory_path)
                if os.path.isfile(os.path.join(directory_path, file))]
    except FileNotFoundError:
        print(f"Directory '{directory_path}' not found.")
        return []


def list_recently_modified_files(directory_path, days):
    """
    List files modified within the last 'days' days.

    :param directory_path: Path to the directory.
    :param days: Number of days to look back.
    :return: List of recently modified files.
    """
    current_time = datetime.now().timestamp()
    cutoff_time = current_time - (days * 86400)
    try:
        return [file for file in os.listdir(directory_path)
                if os.path.isfile(os.path.join(directory_path, file)) and
                os.path.getmtime(os.path.join(directory_path, file)) > cutoff_time]
    except FileNotFoundError:
        print(f"Directory '{directory_path}' not found.")
        return []



def file_exists_in_folder(folder_path, file_name, search_subfolders=False):
    """
    Check if a file exists in a given folder.

    :param folder_path: The path to the folder to search in.
    :param file_name: The name of the file to search for.
    :param search_subfolders: Whether to search in subfolders. Default is False.
    :return: True if the file exists in the folder (and optionally in subfolders), otherwise False.
    """
    # Ensure the folder path exists and is a directory
    if not os.path.isdir(folder_path):
        raise ValueError(f"The provided folder path '{folder_path}' is not a valid directory.")

    # Check in the main folder
    if not search_subfolders:
        return file_name in os.listdir(folder_path)

    # Check in subfolders
    for root, dirs, files in os.walk(folder_path):
        if file_name in files:
            return True

    return False






def rename_folder(current_folder_path, new_folder_name):
    """
    Rename a folder to a new name.

    :param current_folder_path: The full path to the folder to be renamed.
    :param new_folder_name: The new name for the folder.
    """
    # Ensure the current folder path exists and is a directory
    if not os.path.isdir(current_folder_path):
        raise ValueError(f"The provided folder path '{current_folder_path}' is not a valid directory.")

    # Get the parent directory of the folder to be renamed
    parent_directory = os.path.dirname(current_folder_path)

    # Construct the new folder path
    new_folder_path = os.path.join(parent_directory, new_folder_name)

    # Rename the folder
    os.rename(current_folder_path, new_folder_path)

    print(f"Renamed folder from '{current_folder_path}' to '{new_folder_path}'")



