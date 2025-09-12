import os
from contextlib import contextmanager
from monitor import exceptions


# /////////////////////////////////////////////////////////////////////////////
@contextmanager
def directory(path):
    """Context manager to temporarily change the current working directory"""
    try:
        cwd = os.getcwd()
        os.chdir(path)
        yield
    finally:
        os.chdir(cwd)


# ///////////////////////////////////////////////////////////////////////////// 
def get_filepaths(dir):
    """Get a list of all file paths to files in a directory and its subdirectories"""
    if not directory_exists(dir):
        raise exceptions.DirectoryNotFoundError(dir)
    return flatten_list(files_in_dir_and_subdirs(dir))


# /////////////////////////////////////////////////////////////////////////////  
def directory_exists(dir):
    """Check if a directory exists""" 
    return True if os.path.isdir(dir) else False
        
        
# ///////////////////////////////////////////////////////////////////////////// 
def flatten_list(mixed_list):
    """Recursively flatten any sublists into a single list"""
    flat_list = []
    for item in mixed_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list


# /////////////////////////////////////////////////////////////////////////////  
def files_in_dir_and_subdirs(dir):
    """
    Recursively list the files in a directory and its subdirectories.
    Object returned is a nested list mirroring the directory structure.
    """ 
    with directory(dir):
        try:
            return list(map(
                lambda i: get_filepath(dir,i) 
                if os.path.isfile(get_filepath(dir,i)) 
                else files_in_dir_and_subdirs(get_filepath(dir,i)), 
                os.listdir(dir))
                )
        
        except Exception as err:
            raise exceptions.ListFilesError(err) 
    

# /////////////////////////////////////////////////////////////////////////////      
def get_filepath(dir, item):
    """Build a full file path to a file or sub-directory in a directory"""
    try:
        filepath = os.path.join(dir, item)
    
    except Exception as err:
        raise exceptions.FilePathCreationError(item, dir, err)   
        
    return filepath 


# /////////////////////////////////////////////////////////////////////////////   
def get_abs_path(file_path):
    """Get the absolute path of a file from its relative path"""    
    try:
        return os.path.abspath(file_path)

    except Exception as err:
        raise exceptions.AbsolutePathCreationError(file_path, err)  
