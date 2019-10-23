#!/usr/bin/python3


from os import path
from pathlib import Path as PyPath

from requests import get, exceptions


def prepare_file_path(filename, extension, dirpath=''):
    '''
    Inputs:

    filename -- string, file name

    extension
    -- string, file extension
    -- use empty string if extension is included
       in the file name, otherwise must start with a dot

    dirpath
    -- string, directory path
    -- points to the directory where the script is located
       if empty string is given (default) or the given
       directory does not exist (invalid path)
    -- use string with a single dot or getcwd function from os library
       to point to the current working directory


    Returns a string representing an absolute path to the file.
    '''

    extension_requirements = (
        extension.startswith('.'),
        not extension.endswith('.'),
        ' ' not in extension
    )

    if all(extension_requirements):
        filename += extension.lower()

    filepath = dirpath if path.isdir(dirpath) else path.dirname(__file__)
    filepath = path.abspath(filepath)
    filepath = path.join(filepath, filename)

    return filepath


def download_file(url, binf, filepath='', username='', password=''):
    '''
    Inputs:

    url -- string, link to a file

    binf
    -- boolean, file type indicator
    -- binary file is expected if True (default), text file if False

    filepath
    -- string, download locaion
    -- path to a file or directory
    -- if an empty string is given (default), file name will be infered from
       the URL and saved the file to the directory where the script is located

    username, password
    -- strings, authentication information (credentials)
    -- when authentication is not required, use empty strings (default)


    Returns a string with an absolute path if the file was correctly
    downloaded and saved or the file already exists, empty string otherwise.
    '''

    if path.isdir(filepath) or filepath == '':
        # Extract file name from url
        filename = url[url.rindex('/') + 1:]
        filepath = prepare_file_path(filename, '', filepath)

    if path.isfile(filepath):
        print('\nFile is already saved:', filepath, end='\n\n')
        return filepath

    authinf = (username, password) if username and password else None

    try:

        response = get(url, stream=binf, timeout=3, auth=authinf)

        response.raise_for_status()

        if binf:
            with open(filepath, mode='wb') as f:
                f.write(response.content)

        else:
            with open(filepath, mode='wt', encoding=response.encoding) as f:
                f.write(response.text)

    except exceptions.Timeout:
        print('Cannot get:', url)
        print('Connection timeout', end='\n\n')

    except (exceptions.ConnectionError, exceptions.HTTPError) as err:
        print(err, end='\n\n')

    except (IOError, OSError) as err:
        print('Cannot save:', filepath)
        print(err.strerror if err.strerror else err, end='\n\n')

    else:
        response.close()

        print('\nSuccessfully get:', url)
        print('-- Status code:', response.status_code)
        print('-- Encoding:', response.encoding if not binf else '---')

        print('\nFile saved:', filepath, end='\n\n')

        return filepath

    return ''


def clean_dir(dir_path=''):
    '''
    Input:

    dir_path
    -- string, path to a directory
    -- points to the directory where the script is located
       if empty string is given (default)
    -- use string with a single dot or getcwd function from os library
       to point to the current working directory


    Delete all files from the given directory that are not python scripts.

    This function does not return any value.
    '''

    if not dir_path:
        dir_path = path.dirname(__file__)

    dir_path = path.abspath(dir_path)

    try:

        if not path.isdir(dir_path):
            raise IOError('Directory does not exist: {}'.format(dir_path))

        files_to_remove = [
            item for item in PyPath(dir_path).iterdir()
            if item.is_file() and item.suffix != '.py'
        ]

        if not files_to_remove:
            print('No files to remove in {}'.format(dir_path))
            return

        message = '\n'.join((
            '{:n} file(s) will be deleted'.format(len(files_to_remove)),
            'from {}'.format(dir_path),
            '\n'.join('- {}'.format(f.name) for f in files_to_remove)
        ))

        print(message)

        permission = input('Do you want to continue (y/n)? ')
        permission = permission.strip().lower()

        if permission in ('y', 'yes'):
            for f in files_to_remove:
                f.unlink()

    except (IOError, OSError) as err:
        print(err.strerror if err.strerror else err)


if __name__ == '__main__':
    clean_dir()
