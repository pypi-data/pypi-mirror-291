import os
import re
from doc_insights.logging_utils import log_message

def gather_all_filenames(directories, extensions):
    """
    Gathers all filenames with specified extensions from a list of directories.

    This function traverses through the provided directories and gathers all files
    that match the specified extensions. It also includes image files with common 
    image extensions.

    Args:
        directories (list of str): List of directories to search for files.
        extensions (list of str): List of file extensions to include in the search.

    Returns:
        set: A set of filenames that match the specified extensions.
    """
    filenames = set()
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions) or file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                    filenames.add(file)
    return filenames

def extract_links_from_app_dirs(app_dirs, link_patterns):
    """
    Extracts links from .c3doc.md files in application directories, including line numbers.

    This function scans all .c3doc.md files within the provided application directories
    and extracts document, type, and image links based on the provided regular expressions,
    while also tracking the line number of each link.

    Args:
        app_dirs (list of str): List of directories that contain application documentation files.
        link_patterns (dict): A dictionary containing compiled regular expressions for 
                              extracting document, type, and image links.

    Returns:
        dict: A dictionary containing lists of extracted links categorized as 'doc_links', 
              'type_links', and 'image_links', including the line number of each link.
    """
    links_data = {'doc_links': [], 'type_links': [], 'image_links': []}
    
    for directory in app_dirs:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".c3doc.md"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        for line_num, line in enumerate(f, 1):  # Keep track of line numbers
                            doc_links = link_patterns['doc'].findall(line)
                            type_links = link_patterns['type'].findall(line)
                            image_links = link_patterns['image'].findall(line)
                            
                            if doc_links:
                                links_data['doc_links'].append({
                                    'File': file,
                                    'Links': doc_links,
                                    'Line': line_num
                                })
                            if type_links:
                                type_links = [f"{link}.c3typ" if not link.endswith(".c3typ") else link for link in type_links]
                                links_data['type_links'].append({
                                    'File': file,
                                    'Links': type_links,
                                    'Line': line_num
                                })
                            if image_links:
                                links_data['image_links'].append({
                                    'File': file,
                                    'Links': image_links,
                                    'Line': line_num,
                                    'Path': root  # Store the root path for relative image validation
                                })
    return links_data


def validate_links(filenames, links_data, link_type, category_icon, exclude_types=[]):
    """
    Validates the existence of links by comparing them against known filenames,
    and captures line numbers and issue categories.

    Args:
        filenames (set): A set of filenames to validate against.
        links_data (dict): A dictionary containing lists of extracted links categorized 
                           by 'doc_links', 'type_links', and 'image_links'.
        link_type (str): The type of links to validate (e.g., 'doc_links', 'type_links').
        category_icon (str): An icon to represent the category of the issue.
        exclude_types (list of str, optional): A list of type names to exclude from validation.

    Returns:
        list of dict: A summary of broken links, with each entry containing the file name,
                      broken link, line number, and category icon.
    """
    broken_links_summary = []
    
    for data in links_data[link_type]:
        broken_links = []
        for link in data['Links']:
            # For Type validation, exclude certain Types
            if link_type == 'type_links':
                type_name = link.split('.')[0]  # Get the Type name before any dot
                if type_name in exclude_types:
                    continue
            if link not in filenames:
                broken_links.append({'Link': link, 'Line': data['Line'], 'Category': category_icon})
        
        if broken_links:
            broken_links_summary.append({
                'File Name': data['File'],
                'Broken Links': broken_links
            })
    
    return broken_links_summary


def validate_image_links(links_data, filenames, category_icon):
    """
    Validates the existence of image links in the documentation and captures line numbers and category icon.

    Args:
        links_data (dict): A dictionary containing lists of extracted links categorized 
                           by 'doc_links', 'type_links', and 'image_links'.
        filenames (set): A set of filenames to validate against.
        category_icon (str): An icon to represent the category of the issue.

    Returns:
        list of dict: A summary of broken image links, with each entry containing the file 
                      name, broken link, line number, and category icon.
    """
    broken_links_summary = []
    
    for data in links_data['image_links']:
        broken_links = []
        document_path = data['Path']
        for link in data['Links']:
            # Ignore parameters after @ symbol
            link_clean = re.sub(r'@.*', '', link)
            
            # Normalize the path by removing './' if present
            normalized_link = link_clean.lstrip('./')
            
            # Check if the path is an absolute path (e.g., starts with '/')
            if link.startswith('/'):
                # This is an absolute path and should be flagged as invalid
                broken_links.append({'Link': link, 'Line': data['Line'], 'Category': category_icon})
            elif normalized_link.startswith('img/'):
                # Check if the image exists in the `img` folder in the same directory as the document
                img_folder_path = os.path.join(document_path, 'img')
                image_path = os.path.join(img_folder_path, os.path.basename(normalized_link))
                if not os.path.isfile(image_path):
                    broken_links.append({'Link': link, 'Line': data['Line'], 'Category': category_icon})
            else:
                # If it doesn't start with "img/", flag it as broken
                broken_links.append({'Link': link, 'Line': data['Line'], 'Category': category_icon})
                    
        if broken_links:
            broken_links_summary.append({
                'File Name': data['File'],
                'Broken Links': broken_links
            })
    
    return broken_links_summary





def gather_all_filenames(directories, extensions):
    """
    Gathers all filenames with the specified extensions from the given directories.
    
    Args:
        directories (list of str): List of directories to search.
        extensions (list of str): List of file extensions to include.
    
    Returns:
        set: A set of filenames found in the directories.
    """
    filenames = set()
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions) or file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                    filenames.add(file)
    return filenames

