import os
import re
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from doc_insights.logging_utils import log_message
from IPython.display import display, HTML

def count_files_in_single_directory(directory, extensions, scan_cache, subdirs_to_ignore, log_file_path):
    """
    Counts files with specified extensions in a single directory.

    This function traverses through the given directory and counts files that match
    the specified extensions. It also handles subdirectories and aggregates metadata
    for .c3doc.md files.

    Args:
        directory (str): The directory path to search for files.
        extensions (list of str): List of file extensions to include in the count.
        scan_cache (dict): Cache to store scanned directories to avoid reprocessing.
        subdirs_to_ignore (list of str): List of subdirectory names to ignore during the scan.
        log_file_path (str): The path to the log file where messages should be written.

    Returns:
        tuple: A tuple containing:
            - defaultdict(int): A dictionary with the count of files per extension.
            - list of dict: A list of metadata dictionaries for .c3doc.md files.
    """
    # Initialize a dictionary to count files by their extension
    count = defaultdict(int)
    
    # Initialize a list to store metadata for .c3doc.md files
    file_metadata = []

    # Check if the directory has already been scanned
    if directory in scan_cache:
        return scan_cache[directory]

    try:
        # Open the directory for scanning
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file():  # Process files
                    for ext in extensions:
                        if entry.name.endswith(ext):  # Check if the file has a valid extension
                            count[ext] += 1  # Increment the count for the extension
                            if ext == ".c3doc.md":  # If the file is a .c3doc.md, extract its metadata
                                metadata = extract_metadata(entry.path, log_file_path)
                                if metadata:  # Only include if metadata exists
                                    file_metadata.append({
                                        'File Name': entry.name,
                                        'Title': metadata.get('Title', ''),
                                        'Abstract': metadata.get('Abstract', '')
                                    })
                elif entry.is_dir(follow_symlinks=False) and entry.name not in subdirs_to_ignore:
                    # Recursively scan subdirectories, unless they are in the ignore list
                    sub_count, sub_metadata = count_files_in_single_directory(
                        entry.path, extensions, scan_cache, subdirs_to_ignore, log_file_path
                    )
                    # Aggregate counts and metadata from subdirectories
                    for ext, ext_count in sub_count.items():
                        count[ext] += ext_count
                    file_metadata.extend(sub_metadata)
    except PermissionError:
        # Log an error if the directory cannot be accessed due to permissions
        log_message(f"Permission denied: {directory}", log_file_path)
    except Exception as e:
        # Log any other errors that occur during the scan
        log_message(f"Error accessing {directory}: {e}", log_file_path)
    
    # Cache the results to avoid reprocessing the same directory
    scan_cache[directory] = (count, file_metadata)
    
    return count, file_metadata


def extract_metadata(file_path, log_file_path):
    """
    Extracts metadata (Title, Abstract) from the top of a .c3doc.md file.

    This function reads a .c3doc.md file and extracts metadata information,
    specifically the Title and Abstract, which are located at the top of the file.

    Args:
        file_path (str): The path to the .c3doc.md file.
        log_file_path (str): The path to the log file where error messages should be written.

    Returns:
        dict: A dictionary containing the extracted metadata. Returns None if no metadata is found.
    """
    metadata = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if not line.strip():  # End of metadata section
                    break
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
                else:
                    break
    except Exception as e:
        log_message(f"Error reading metadata from {file_path}: {e}", log_file_path)
    return metadata if metadata else None

def shorten_path(path, levels=2):
    """
    Shortens the given path for easier reading in the output.

    This function shortens a file or directory path by keeping only the last
    few levels, making it easier to display in output logs or tables.

    Args:
        path (str): The full path to shorten.
        levels (int, optional): The number of path levels to retain. Defaults to 2.

    Returns:
        str: The shortened path.
    """
    return '/'.join(path.rstrip('/').split('/')[-levels:]) + '/'

def process_directories(directories, extensions, app_dirs, max_workers, subdirs_to_ignore, log_file_path, app_dir_key, dep_dir_key):
    """
    Processes a list of directories and counts files by extension.

    This function concurrently processes multiple directories, counting files
    that match the specified extensions. It also categorizes directories as
    application or dependency and aggregates metadata for .c3doc.md files.

    Args:
        directories (list of str): List of directories to process.
        extensions (list of str): List of file extensions to include in the count.
        app_dirs (list of str): List of application directories.
        max_workers (int): The maximum number of threads to use for concurrent processing.
        subdirs_to_ignore (list of str): List of subdirectory names to ignore during the scan.
        log_file_path (str): The path to the log file where messages should be written.
        app_dir_key (str): The key to categorize application directories.
        dep_dir_key (str): The key to categorize dependency directories.

    Returns:
        tuple: A tuple containing:
            - list of dict: A list of dictionaries summarizing the file counts per directory.
            - list of dict: A list of metadata dictionaries for .c3doc.md files.
    """
    start_time = time.time()
    all_counts = []
    all_metadata = []
    completed_dirs = 0
    total_dirs = len(directories)
    scan_cache = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(count_files_in_single_directory, directory, extensions, scan_cache, subdirs_to_ignore, log_file_path): directory 
                   for directory in directories}

        for future in as_completed(futures):
            directory = futures[future]
            result, metadata = future.result()

            directory_short = shorten_path(directory)
            is_app_dir = app_dir_key if directory in app_dirs else dep_dir_key
            directory_result = {'Directory': directory_short, 'Type': is_app_dir}
            for ext, count in result.items():
                directory_result[ext] = count

            all_counts.append(directory_result)
            all_metadata.extend(metadata)
            completed_dirs += 1
            log_message(f"Processed {completed_dirs}/{total_dirs} directories...", log_file_path)

    log_message(f"\nTotal time taken: {time.time() - start_time:.4f} seconds", log_file_path)
    return all_counts, all_metadata

def output_file_counts(all_counts, extensions, metadata, broken_links_summary, should_print_counts, should_print_broken_links, should_print_documents, save_to_csv=False, csv_path=None, log_file_path="scan_log.txt"):
    """
    Outputs file counts, metadata, and broken links summary, with configurable print options.

    Args:
        all_counts (list of dict): A list of dictionaries summarizing the file counts per directory.
        extensions (list of str): List of file extensions included in the count.
        metadata (list of dict): A list of metadata dictionaries for .c3doc.md files.
        broken_links_summary (list of dict): A list of dictionaries summarizing any broken links found.
        should_print_counts (bool): Whether to print the file counts to the console.
        should_print_broken_links (bool): Whether to print the broken links table to the console.
        should_print_documents (bool): Whether to print the document metadata table to the console.
        save_to_csv (bool, optional): Whether to save the results to a CSV file. Defaults to False.
        csv_path (str, optional): The path to the CSV file where results should be saved. Required if `save_to_csv` is True.
        log_file_path (str, optional): The path to the log file where messages should be written. Defaults to "scan_log.txt".

    Returns:
        None
    """
    df_counts = pd.DataFrame(all_counts).fillna(0)
    df_counts[extensions] = df_counts[extensions].astype(int)
    df_counts = df_counts[['Directory', 'Type'] + extensions]
    
    df_counts.sort_values(by=['Type', 'Directory'], ascending=[True, False], inplace=True)
    
    if should_print_counts:
        print("\nFile counts by extension across all directories:")
        display(df_counts.style.set_table_attributes('style="width:100%"'))

    # Check if metadata is not empty before processing it
    if metadata:
        df_metadata = pd.DataFrame(metadata)
        if should_print_documents:
            print("\nMetadata for .c3doc.md files:")
            display(df_metadata.style.set_table_attributes('style="width:100%"'))
        
        if save_to_csv and csv_path:
            metadata_csv_path = csv_path.replace('.csv', '_metadata.csv')
            df_metadata.to_csv(metadata_csv_path, index=False)

    # Process and display broken links
    if broken_links_summary:
        expanded_broken_links = []
        for item in broken_links_summary:
            file_name = item['File Name']
            for link_data in item['Broken Links']:
                expanded_broken_links.append({
                    'File Name': file_name,
                    'Broken Link': link_data['Link'],
                    'Line Number': link_data['Line'],
                    'Category': link_data['Category']
                })

        df_broken_links = pd.DataFrame(expanded_broken_links)
        if should_print_broken_links:
            print("\nBroken Links Summary:")
            display(df_broken_links.style.set_table_attributes('style="width:100%"'))

        if save_to_csv and csv_path:
            broken_links_csv_path = csv_path.replace('.csv', '_broken_links.csv')
            df_broken_links.to_csv(broken_links_csv_path, index=False)

    if save_to_csv and csv_path:
        df_counts.to_csv(csv_path, index=False)
        log_message(f"Results saved to {csv_path} and associated files", log_file_path)



