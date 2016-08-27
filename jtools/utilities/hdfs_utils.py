"""
Module to handle various common HDFS IO functions
"""
import subprocess

hadoop_cli_ = 'hadoop'
hdfs_scheme_ = 'hdfs://'


def stream_from_hdfs(path_to_hdfs_file):
    """
    :param path_to_hdfs_file: Path to an existing file on HDFS to stream (NOTE: hadoop must be in the PATH)
    :return: A file-like object to read from
    """
    # use -text instead of -cat to automatically handle compressed files
    return subprocess.Popen([hadoop_cli_, 'fs', '-text', path_to_hdfs_file], stdout=subprocess.PIPE).stdout


def put_file_to_hdfs(path_to_local_file, path_to_hdfs_directory):
    """
    :param path_to_local_file: Path to an existing local file
    :param path_to_hdfs_directory: Existing HDFS directory to put the local file to
    """
    subprocess.check_call([hadoop_cli_, 'fs', '-put', path_to_local_file, path_to_hdfs_directory])


def move_file_to_hdfs(path_to_local_file, path_to_hdfs_directory):
    """
    :param path_to_local_file: Path to an existing local file that is deleted after it's put to HDFS
    :param path_to_hdfs_directory: Existing HDFS directory to put the local file to
    """
    subprocess.check_call([hadoop_cli_, 'fs', '-moveFromLocal', path_to_local_file, path_to_hdfs_directory])


def hdfs_mkdir(new_hdfs_directory):
    """
    :param new_hdfs_directory: The new HDFS directory to create
    """
    subprocess.check_call([hadoop_cli_, 'fs', '-mkdir', '-p', new_hdfs_directory])


def open_for_read(file_path):
    """
    :param file_path: Can be a HDFS URL to a file, or a path to a local file
    :return: A file-like object to read from
    """
    if file_path.startswith(hdfs_scheme_):
        return stream_from_hdfs(file_path[len(hdfs_scheme_):])
    else:
        return open(file_path)
