# !/usr/bin/python
# -*- coding: utf-8 -*-

import ftplib
import logging
import os
import socket
import time
from ftplib import FTP
from constants import *
from credentials import *


def create_directory(path):
    logging.info('creating the folder ' + path + "...")
    if not os.path.isdir(path):
        os.makedirs(path)
        logging.info("the folder " + path + " was successfully created")
    else:
        logging.info("the folder " + path + " already exists, it's ok")
    # Designation of the working directory as current directory
    os.chdir(path)


def create_timestamped_and_named_file_name(file_name):
    computer_name = socket.gethostname()
    timestamp = time.strftime("%Y%m%d") + "_" + time.strftime("%H%M%S")
    format_file_name = f"{timestamp}_{computer_name}_{file_name}"
    return format_file_name


def count_files_in_a_directory(path):
    files_count = 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRECTORIES]
        files_count += len(files)
    return files_count


def parse_directories(path, backup_file):
    number_of_directories = 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRECTORIES]
        backup_file.write("\n" + root)
        number_of_directories += 1
    backup_file.write("\n\nNumber of folders in the directory " + path + " : " + str(number_of_directories - 1))


def print_current_state_of_parsing_files(current_count_in_path, total_files_count_in_path, path):
    percentage = None
    if total_files_count_in_path != 0:
        try:
            percentage = round((current_count_in_path / total_files_count_in_path) * 100, 2)
        except ZeroDivisionError as e:
            logging.error("Error: " + str(e))
        finally:
            print(f"files processed in {path} : {current_count_in_path} of {total_files_count_in_path} ({percentage}%)")


def parse_all_folders_and_files(path, backup_file, files_count_in_path):
    current_count_parsing_files = 0
    last_time_current_state_of_parsing_files_printed = time.time()
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRECTORIES]
        backup_file.write("\n" + root)
        for file in files:
            try:
                path_name = os.path.join(root, file)
                size = os.path.getsize(os.path.join(root, path_name))
                timestamp = os.path.getmtime(os.path.join(root, path_name))
                # timestamp conversion in the form of : DD/MM/YY HH:MM:SS
                time_format_temp = time.gmtime(timestamp)
                time_format = time.strftime("%x %X", time_format_temp)
                backup_file.write("\n" + "--- " + path_name + " *** " + time_format + " *** " + str(size) + " Ko")
                current_count_parsing_files += 1
            except Exception as e:
                print("Error: " + str(e))
            finally:
                current_time = time.time()
                if current_time > last_time_current_state_of_parsing_files_printed + 1:
                    print_current_state_of_parsing_files(current_count_parsing_files, files_count_in_path, path)
                    last_time_current_state_of_parsing_files_printed = current_time
    print_current_state_of_parsing_files(current_count_parsing_files, files_count_in_path, path)
    backup_file.write("\n\nNumber of files in the directory " + path + " : " + str(files_count_in_path))


def get_the_latest_file_in_a_folder(path):
    list_of_files = os.listdir(path)  # get a list of all file names in a folder
    # get a list of absolute paths for previously recovered files
    paths = [os.path.join(path, basename) for basename in list_of_files]
    # return the latest (most recent modified metadata) file
    return max(paths, key=os.path.getctime)


def upload_file_to_server_ftp(file, filename):
    ftp = FTP(SEEDBOX_DOMAIN_NAME)  # connect to host, default port
    try:
        logging.info("trying to connect the ftp server...")
        ftp.login(user=SEEDBOX_USER_NAME, passwd=SEEDBOX_PASSWD)  # login with credentials
        logging.info('ftp connection succeed !')
        try:
            # TODO : se placer dans le bon repertoire (ok) du serveur et
            #  creer un dossier *nom application* s'il n'existe pas
            ftp.cwd(SEEDBOX_ROOT_SLIMER_SCRIPT_PATH)  # Set the current directory on the server
            logging.info('sending ' + filename + ' file to the ftp server...')
            ftp.storbinary('STOR ' + filename + '', file)  # uploading file to the server
            logging.info(filename + ' uploaded successfully!')
        except ftplib.all_errors:
            logging.error('unable to make directories')
    except ftplib.all_errors:
        logging.error('unable to connect to ftp server')
    ftp.quit()


def upload_file_to_server_ftp_without_logging_messages(file, filename, subdirectory):
    ftp = FTP(SEEDBOX_DOMAIN_NAME)  # connect to host, default port
    try:
        print("trying to connect the ftp server...")
        ftp.login(user=SEEDBOX_USER_NAME, passwd=SEEDBOX_PASSWD)  # login with credentials
        print('ftp connection succeed !')
        try:
            # TODO : se placer dans le bon repertoire (ok) du serveur et
            #  creer un dossier *nom application* s'il n'existe pas
            ftp.cwd(SEEDBOX_ROOT_SLIMER_SCRIPT_PATH + "/" + subdirectory)  # Set the current directory on the server
            print('sending ' + filename + ' file to the ftp server... (' + subdirectory + ' file)')
            ftp.storbinary('STOR ' + filename + '', file)  # uploading file to the server
            print(filename + ' uploaded successfully!')
        except ftplib.all_errors:
            print('unable to make directories')
    except ftplib.all_errors:
        print('unable to connect to ftp server')
    ftp.quit()


def get_computer_name():
    computer_name = socket.gethostname()
    return computer_name
