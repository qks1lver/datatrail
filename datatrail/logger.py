#!/usr/bin/env python3

"""
Copyright 2018 Jiun Yang Yen

MIT License

"""

# Imports
from __future__ import print_function
import os
import shutil
from datetime import datetime

# Global variables
_dtrail_log = ''
_header = 'datatrail: '
_dtrail = '.dtrail'
_verbose = False

# Functions
def init(force=False):

    """
    Initialize a Datatrail log (.dtrail) for a project. Usually do this in the parent directory of the project. Only
    need to do this once for a project.

    :param force: Boolean, (optional) whether to force create a new .dtrail log eventhough there's one in a parent directory
    :return: Boolean, initialized successfully (True), otherwise False
    """

    global _dtrail_log

    if _check_log() and not force:
        print(_header + 'Found .dtrail log in directory or parent directory. Use force=True to create a new one. Current log at %s' % _dtrail_log)
        return(False)

    _dtrail_log = os.path.abspath(_dtrail)

    with open(_dtrail_log, 'w+') as f:
        timestamp = datetime.now().isoformat()
        _ = f.write('%s\n\tInitialized at %s\n\n'%(timestamp, _dtrail_log))
        print(_header + 'Initialized .dtrail log: %s' % _dtrail_log)

    return(True)

def set_verbose(verbose=True):

    """
    Whether to let Datatrail talk a lot.

    :param verbose: Boolean, (optional) to verbose (True), not to verbose (False)
    :return: None
    """

    global _verbose

    _verbose = verbose

    return

def load(p_log=''):

    """
    Manually load a .dtrail log file. Usually don't need to run this since the most closely associated .dtrail log will
    be automatically identified.

    :param p_log: String, (optional) path of a .dtrail log
    :return: Boolean, loaded successfully (True), otherwise False
    """

    global _dtrail_log

    status = False

    if p_log:
        if os.path.isfile(p_log):
            _dtrail_log = p_log
            if _verbose:
                print(_header + 'Loaded log: %s' % _dtrail_log)
        elif _verbose:
            print(_header + 'Not a file: %s' % p_log)
    else:
        p_log = _search_dtrail()
        if p_log:
            _dtrail_log = p_log
            status = True
            if _verbose:
                print(_header + 'Loaded log: %s' % p_log)
        elif _verbose:
            print(_header + 'Cannot locate .dtrail log. Consider initializing with logger.init()')

    return(status)

def show_log_path():

    """
    Display where the currently loaded .dtrail log is at.

    :return: String, path of the currently loaded .dtrail log. Empty ('') if none loaded.
    """

    if _check_log():
        print(_header + 'Current log at %s' % _dtrail_log)
        return(_dtrail_log)

    return('')

def run(func, *args, func_name='', **kwargs):

    """
    This runs and log the given function into .dtrail log.

    :param func: The function to run.
    :param args: Positional arguments for the function to run.
    :param func_name: String, (optional) the name of the function to use for logging (not recommend using)
    :param kwargs: keyword arguments for the function to run.
    :return: Output of the function ran or -1 if .dtrail log is missing
    """

    if not _check_log():
        return(-1)

    if not func_name:
        func_name = func.__name__

    output = func(*args, **kwargs)
    if isinstance(output, (list, tuple)):
        output_list = list(output)
    else:
        output_list = [output]

    with open(_dtrail_log, 'a') as f:
        f.write('%s\n\t%s(' % (datetime.now().isoformat(), func_name))
        for x in args:
            if type(x) == str:
                _ = f.write("'%s',"%x)
            else:
                _ = f.write('%s,'%x)
        for x in kwargs:
            if type(kwargs[x]) == str:
                _ = f.write("%s='%s',"%(x,kwargs[x]))
            else:
                _ = f.write('%s=%s,'%(x,kwargs[x]))
        f.write(')\n')
        for x in list(output_list):
            _ = f.write('\t@RETURN=%s\n'%x)
        f.write('\n')

    if _verbose:
        print(_header + 'Logged.')

    return(output)

def make(p_file, overwrite=False):

    """
    To make a file.

    :param p_file: String, path or name of the file to make.
    :param overwrite: Boolean, (optional) overwrite an existing file (True), otherwise False
    :return: int, if missing .dtrail log (-1), if file already exist and not overwriting (0), if sucessfully made (1)
    """

    if not _check_log():
        return(-1)

    p_file = os.path.abspath(p_file)

    if os.path.isfile(p_file):
        if not overwrite:
            print(_header + 'File name already exists, use overwrite=True to replace. File at %s' % p_file)
            return(0)
        else:
            _ = run(_make_file, p_file, func_name='make', overwrite=overwrite)
    else:
        _ = run(_make_file, p_file, func_name='make')

    return(1)

def remove(p_file):

    """
    To remove a file.

    :param p_file: String, path or name of the file to remove.
    :return: int, if missing .dtrail log (-1), if file does not exist (0), if sucessfully removed (1).
    """

    if not _check_log():
        return(-1)

    if not os.path.isfile(p_file):
        print(_header + 'File does not exist: %s' % p_file)
        return(0)

    _ = run(os.remove, p_file)

    return(1)

def rename(p_src, p_dest, overwrite=False):

    """
    To rename a file.
    Use .move() to move since that one lets you pass in a directory path.

    :param p_src: String, path or name of the source file.
    :param p_dest: String, the new name.
    :param overwrite: Boolean, (optional) to overwrite an existing file (True), otherwise False.
    :return: int, if missing .dtrail log (-1), if source file does not exist (-2), if new name already exist but not overwrite (0), if successfully renamed (1)
    """

    if not _check_log():
        return(-1)

    p_src = os.path.abspath(p_src)
    p_dest = os.path.abspath(p_dest)

    if not os.path.isfile(p_src):
        print(_header + 'Source file does not exist: %s' % p_src)
        return(-2)

    if os.path.isfile(p_dest):
        if not overwrite:
            print(_header + 'A file with this name already exists, use overwrite=True to replace. File at %s' % p_dest)
            return(0)
        else:
            _ = run(_rename_file, p_src, p_dest, func_name='rename', overwrite=overwrite)
    else:
        _ = run(_rename_file, p_src, p_dest, func_name='rename')

    return(1)

def copy(p_src, dest='.', overwrite=False):

    """
    To copy a file.

    :param p_src: String, path or name of the source file.
    :param dest: String, path of the destination folder (or new path for the file if name must be specific).
    :param overwrite: Boolean, (optional) to overwrite an existing file (True), otherwise False.
    :return: int or String, if missing .dtrail log (-1), if source file does not exist (-2), if desination directory does not exist (0), if successfully copied (path of copied file)
    """

    if not _check_log():
        return(-1)

    if not os.path.isfile(p_src):
        print(_header + 'Source file does not exist: %s' % p_src)
        return(-2)
    p_src = os.path.abspath(p_src)

    if os.path.isdir(dest):
        if dest.endswith('/'):
            dest += '/'
        fname = os.path.basename(p_src)
        p_dest = os.path.abspath(dest) + '/' + _insert_fname(fname)

    elif not dest.endswith('/') and os.path.isdir(os.path.dirname(os.path.abspath(dest))):
        p_dest = os.path.abspath(dest)
        while os.path.isfile(p_dest) and not overwrite:
            fname = os.path.basename(p_dest)
            p_dir = os.path.dirname(p_dest)
            p_dest = p_dir + '/' + _insert_fname(fname)

    else:
        print(_header + 'Destination folder does not exist: %s' % dest)
        return(0)

    if overwrite:
        _ = run(_copy_file, p_src, p_dest, func_name='copy', overwrite=overwrite)
    else:
        _ = run(_copy_file, p_src, p_dest, func_name='copy')

    return(p_dest)

def move(p_src, dest, overwrite=False):

    """
    To move.
    Use .rename() to rename since that is faster.

    :param p_src: String, path or name of the source file.
    :param dest: String, path of the destination folder (or new path for the file if name must be specific).
    :param overwrite: Boolean, (optional) to overwrite an existing file (True), otherwise False.
    :return: int or String, if missing .dtrail log (-1), if source file does not exist (-2), if source and destination are the same (-3), if filename already exist and not overwriting (-4), if desination directory does not exist (0), if successfully moved (new path of file)
    """

    if not _check_log():
        return(-1)

    if not os.path.isfile(p_src):
        print(_header + 'Source file does not exist: %s' % p_src)
        return(-2)
    p_src = os.path.abspath(p_src)

    if os.path.isdir(dest):
        if dest.endswith('/'):
            dest += '/'
        p_dest = os.path.abspath(dest) + '/' + os.path.basename(p_src)

    elif not dest.endswith('/') and os.path.isdir(os.path.dirname(os.path.abspath(dest))):
        p_dest = os.path.abspath(dest)
        if p_dest == p_src:
            print(_header + 'Souce and destination are the same')
            return(-3)

        if os.path.isfile(p_dest) and not overwrite:
            print(_header + 'A file with the same name already exist, use overwrite=True to overwrite. File at %s' % p_dest)
            return(-4)

    else:
        print(_header + 'Destination folder does not exist: %s' % dest)
        return(0)

    if overwrite:
        _ = run(_move_file, p_src, p_dest, func_name='move', overwrite=overwrite)
    else:
        _ = run(_move_file, p_src, p_dest, func_name='move')

    return(p_dest)

def _check_log():

    if os.path.isfile(_dtrail_log):
        return(True)
    elif load():
        return(True)

    print(_header + 'Cannot locate .dtrail log. Consider initializing with logger.init()')

    return(False)

def _search_dtrail():

    p_log = ''

    if os.path.isfile(_dtrail):
        p_log = os.path.abspath(_dtrail)
    else:
        parts = os.path.realpath('.').split('/')[:-1]
        while parts:
            p_tmp = '/'.join(parts) + '/' + _dtrail
            if os.path.isfile(p_tmp):
                p_log = p_tmp
                break
            else:
                _ = parts.pop()

    return(p_log)

def _make_file(p_file, overwrite=False):

    with open(p_file, 'w+') as f:
        _ = f.write('')

    if overwrite and _verbose:
        print(_header + 'Overwrite %s' % p_file)

    return(p_file)

def _rename_file(p_src, p_dest, overwrite=False):

    os.rename(p_src, p_dest)

    if overwrite and _verbose:
        print(_header + 'Overwrite %s' % p_dest)

    return(p_dest)

def _copy_file(p_src, p_dest, overwrite=False):

    shutil.copyfile(p_src, p_dest)

    if overwrite and _verbose:
        print(_header + 'Overwrite %s' % p_dest)

    return(p_dest)

def _move_file(p_src, p_dest, overwrite=False):

    shutil.move(p_src, p_dest)

    if overwrite and _verbose:
        print(_header + 'Overwrite %s' % p_dest)

    return (p_dest)

def _insert_fname(fname, insertion='copy', addtime=True):

    tmp = fname.split('.')

    timestamp = ''
    if addtime:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    if len(tmp) > 1:
        fname = '.'.join(tmp[:-1]) + '-%s%s.' % (insertion, timestamp) + tmp[-1]
    else:
        fname = tmp[0] + '-%s%s' % (insertion, timestamp)

    return(fname)
