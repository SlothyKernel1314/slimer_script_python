# !/usr/bin/python
# -*- coding: utf-8 -*-

from utilities import *
from constants import *


def upload_slimer_script_log(backup_file):
    # opens the file for reading only in binary format in order to upload
    file = open(backup_file.name, "rb")

    upload_file_to_server_ftp(file, file.name)

    file.close()


def slimer_script():
    computer_name = get_computer_name()

    logging.info(f"COMPUTER NAME : {computer_name}")

    logging.info("SLIMER SCRIPT is currently running. This can take up a few minutes...")

    timestamped_directory = create_timestamped_directory(SLIMER_SCRIPT_ROOT_LOGS_PATH)

    for path in DIRECTORIES_TO_BE_SCANNED_FOR_BACKUP.values():

        formatted_path = format_path(path)

        backup_file = open(create_timestamped_and_named_file_name(APPLICATION_NAME + formatted_path
                                                                  + SLIMER_SCRIPT_BACKUP_FILE_END_NAME),
                           "w", encoding="utf-8")
        backup_file.write(f"COMPUTER NAME : {computer_name}")
        logging.info(f"Counting the number of files in the folder {path} ...")
        files_count_in_path = count_files_in_a_directory(path)
        logging.info(f"Number of files in the folder {path} : {files_count_in_path}")
        logging.info(f"Backup of data (name, size and last modification date) of the files in the folder {path} ...")
        backup_file.write(f"\n\nList of directories, subdirectories and descendants of the folder {path} \n")
        parse_directories(path, backup_file)
        backup_file.write("\n\n################################################################################ \n")
        backup_file.write(f"\nList of files in the folder {path} \n")
        parse_all_folders_and_files(path, backup_file, files_count_in_path)
        backup_file.write("\n\n################################################################################ \n")
        logging.info(f"The backup of the data of the files in the directory {path} has been completed")
        backup_file.close()

    logging.info("All paths have been scanned. All backup files are saved")

    # logging.info('get all files in order to zip theses files')
    # file_paths_to_zip = get_all_file_paths(SLIMER_SCRIPT_ROOT_LOGS_PATH + "/" + timestamped_directory)
    #
    # zip_file = zip_files(file_paths_to_zip, SLIMER_SCRIPT_ROOT_LOGS_PATH + "/" + timestamped_directory,
    #                      computer_name + "_backup")
    #
    # # opens the zip file for reading only in binary format in order to upload
    # opened_zip_file = open(zip_file.filename, "rb")
    #
    # upload_file_to_server_ftp(opened_zip_file, zip_file.filename)
    #
    # opened_zip_file.close()
    #
    # logging.info('deleting local zip file...')
    # os.remove(zip_file.filename)
    #
    # logging.info('delete local zip file done')

