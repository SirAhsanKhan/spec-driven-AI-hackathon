import os
import glob
from typing import List, Dict
from pathlib import Path
from utils.logging import get_logger

logger = get_logger(__name__)

def read_markdown_files_from_directory(directory_path: str) -> List[Dict[str, str]]:
    """
    Read all markdown files from a given directory and return as a list of dictionaries
    """
    markdown_files = []
    
    # Find all markdown files in the directory and subdirectories
    md_files = glob.glob(os.path.join(directory_path, "**/*.md"), recursive=True)
    mdx_files = glob.glob(os.path.join(directory_path, "**/*.mdx"), recursive=True)
    
    all_files = md_files + mdx_files
    
    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Extract file name without extension for use as title/identifier
                file_name = Path(file_path).stem
                relative_path = os.path.relpath(file_path, directory_path)
                
                markdown_files.append({
                    "title": file_name,
                    "content": content,
                    "source_path": relative_path,
                    "full_path": file_path
                })
                
                logger.info(f"Successfully read markdown file: {relative_path}")
                
        except Exception as e:
            logger.error(f"Error reading markdown file {file_path}: {str(e)}")
    
    return markdown_files

def read_specific_markdown_file(file_path: str) -> str:
    """
    Read a specific markdown file and return its content
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            logger.info(f"Successfully read specific markdown file: {file_path}")
            return content
    except Exception as e:
        logger.error(f"Error reading specific markdown file {file_path}: {str(e)}")
        return None