import os
import re
from doc_insights.file_processing import process_directories, output_file_counts
from doc_insights.link_validation import gather_all_filenames, extract_links_from_app_dirs, validate_links, validate_image_links
from doc_insights.logging_utils import log_message

# Keys for different types of links in the links_data
doc_link_key = 'doc_links'
type_link_key = 'type_links'
image_link_key = 'image_links'

# Link patterns for extracting links from the .c3doc.md files
link_patterns = {
    'doc': re.compile(r'\[.*?\]\((.*?\.c3doc\.md)\)'),
    'type': re.compile(r'\{@link ([\w.]+)'),
    'image': re.compile(r'!\[.*?\]\((.*?)\)')
}

# User input: keys for application and dependency directories
app_dir_key = "Application"
dep_dir_key = "Dependency"

# Determine the optimal number of threads
max_workers = min(32, os.cpu_count() + 4)

def run_validation(
    dependency_dirs, app_dirs, file_exts_to_include, exclude_types, 
    subdirs_to_ignore, should_print_counts, should_print_broken_links, should_print_documents, 
    should_save_to_csv, csv_file_path, doc_file_ext, type_file_ext, log_file_path
):
    # Icons for different categories
    doc_icon = "📄"  # Document-related issue
    type_icon = "🔗"  # Missing Type issue
    image_icon = "🖼️"  # Image-related issue

    # Step 1: Gather all filenames from dependency_dirs
    all_filenames = gather_all_filenames(dependency_dirs, [doc_file_ext, type_file_ext])

    # Step 2: Extract links from `.c3doc.md` files in app_dirs
    links_data = extract_links_from_app_dirs(app_dirs, link_patterns)

    # Step 3: Validate document links
    broken_doc_links_summary = validate_links(all_filenames, links_data, doc_link_key, doc_icon, exclude_types)

    # Step 4: Validate type links
    broken_type_links_summary = validate_links(all_filenames, links_data, type_link_key, type_icon, exclude_types)

    # Step 5: Validate image links
    broken_image_links_summary = validate_image_links(links_data, all_filenames, image_icon)

    # Process directories and output results
    all_counts, all_metadata = process_directories(
        dependency_dirs, file_exts_to_include, app_dirs, max_workers, 
        subdirs_to_ignore, log_file_path, app_dir_key, dep_dir_key
    )
    
    output_file_counts(
        all_counts, 
        file_exts_to_include, 
        all_metadata, 
        broken_doc_links_summary + broken_type_links_summary + broken_image_links_summary, 
        should_print_counts, 
        should_print_broken_links, 
        should_print_documents, 
        save_to_csv=should_save_to_csv, 
        csv_path=csv_file_path,
        log_file_path=log_file_path
    )
