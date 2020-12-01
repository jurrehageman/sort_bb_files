#!/usr/bin/env python3
import os
import sys
import shutil
from zipfile import ZipFile
from PIL import Image
import platform
import warnings
import hashlib
import argparse
import random
#PLATFORM
OS_TYPE = platform.platform()
if not OS_TYPE.startswith("Windows"):
    import pyheif

#SETTINGS
MAX_PATH = 260


def get_comm_args():
    """
    Reads command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Sort files downloaded from Blackboard")
    parser.add_argument("zip_file",
                        help="the path to the Zip File downloaded from Blackboard")
    parser.add_argument("output_folder",
                        help="the path to the Folder with the output")
    parser.add_argument('-p', '--pdf', action='store_true',
                        help="exports to pdf")
    parser.add_argument('-c', '--checksum', action='store_true',
                        help="generates md5 checksums")
    parser.add_argument('-r', '--randomize', action='store_true',
                        help="adds random numbers to student numbers to randomize folder/file sequence")
    args = parser.parse_args()
    return args


def is_jpg(filename):
    try:
        i=Image.open(filename)
        return i.format =='JPEG'
    except IOError:
        return False


def make_folder(out_folder):
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)


def windows_warnings():
    warnings.warn("HEIC to jpg conversion will not work on Windows")
    len_path_zip = len(os.getcwd())
    if len_path_zip > (MAX_PATH - 150):
        warnings.warn("You are approaching MAX_PATH. If unzipping fails, run this script from de Desktop.")


def unpack_zip(zip_in_loc, out_folder):
    file_name, file_extension = os.path.splitext(zip_in_loc)
    if not file_extension == ".zip":
        print(file_name + file_extension, "is not a zip file. Only zip files are allowed.")
        sys.exit()
    print("Extracting zip file...")
    unzipped_files = os.path.join(out_folder, "unzipped_files")
    make_folder(unzipped_files)
    with ZipFile(zip_in_loc, 'r') as zipObj:
        zipObj.extractall(unzipped_files)
    print("Zip file extracted")


def sort_files(out_folder, randomize):
    source = os.path.join(out_folder, "unzipped_files")
    all_files = os.listdir(source)
    destination = os.path.join(out_folder, "sorted_files")
    students = []
    for i in all_files:
        salt = ""
        #For Mac-users (__MACOSX folder is created)
        if i.startswith("__MAC"):
            continue
        student = i.split("_")[1]
        if not student in students:
            if randomize:
                salt = str(random.randint(100, 999)) + "_"
            out_path = os.path.join(destination, salt + student)
            print("Sorting to", salt + student)
            make_folder(out_path)
            whole_path = os.path.join(source, i)
            out_path_file = os.path.join(out_path, i)
            shutil.copyfile(whole_path, out_path_file)
            students.append(student)
        else:
            whole_path = os.path.join(source, i)
            out_path_file = os.path.join(out_path, i)
            shutil.copyfile(whole_path, out_path_file)


def export_to_pdf(out_folder):
    pdf_destination = os.path.join(out_folder, "pdf_files")
    sorted_files = os.path.join(out_folder, "sorted_files")
    make_folder(pdf_destination)
    first_image_obj = None
    jpg_ext = ".jpg .JPG .jpeg .JPEG".split()
    print("Exporting to pdf...")
    all_folders = os.listdir(sorted_files)
    for subfolder in all_folders:
        whole_path = os.path.join(sorted_files, subfolder)
        all_files = os.listdir(whole_path)
        first_image_obj = None
        image_list = []
        pdf_filename = os.path.join(pdf_destination, subfolder + ".pdf")
        print("Now processing", pdf_filename)
        jpg_counter = 0
        for i in all_files:
            file_path = os.path.join(whole_path, i)
            file_name, file_extension = os.path.splitext(i)
            if file_extension in jpg_ext:
                if is_jpg(file_path):
                    if jpg_counter == 0:
                        first_image_obj = Image.open(file_path)
                    else:
                        image_obj = Image.open(file_path)
                        image_list.append(image_obj)
                    jpg_counter += 1
                else:
                    print("Warning: file", file_path, "is not a valid jpg file")
                    continue
        if first_image_obj:
            first_image_obj.save(pdf_filename, "PDF", resolution=100.0, save_all=True, append_images=image_list)


def write_log(out_folder):
    print("writing log...")
    log_path = os.path.join(out_folder, "log")
    make_folder(log_path)
    log_file = os.path.join(log_path, "log_file.txt")
    zip_location = os.path.join(out_folder, "unzipped_files")
    pic_to_skip = ".jpg .jpeg .JPG .JPEG".split()
    others_to_skip = [".txt"]
    with open(log_file, "w") as f:
        f.write("Files with other extension then jpg or txt\n")
        f.write("or files with .jpg extension but fail jpg integrity test:\n\n")
        all_files = os.listdir(zip_location)
        for i in all_files:
            file_name, file_extension = os.path.splitext(i)
            if not file_extension in pic_to_skip and file_extension not in others_to_skip:
                f.write(i + "\n")
            elif not is_jpg(os.path.join(zip_location, i)) and file_extension not in others_to_skip:
                print(i)
                f.write(i + "\n")


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def write_md5_checksum(out_folder):
    print("Creating md5 hashes...")
    md5_file = os.path.join(out_folder, "log", "file_hashes.csv")
    unzipped_files = os.path.join(out_folder, "unzipped_files")
    with open(md5_file, "w") as csv:
        csv.write("Filepath; MD5 checksum\n\n")
        all_files = os.listdir(unzipped_files)
        for i in all_files:
            file_path = os.path.join(unzipped_files, i)
            file_hash = md5(file_path)
            csv.write("{};{}\n".format(i, file_hash))  # Get the hexadecimal digest of the hash


def export_heic_to_jpg(file_destination):
    heic_ext = [".HEIC", ".heic"]
    all_folders = os.listdir(file_destination)
    for subfolder in all_folders:
        whole_path = os.path.join(file_destination, subfolder)
        all_files = os.listdir(whole_path)
        for i in all_files:
            file_path = os.path.join(whole_path, i)
            file_name, file_extension = os.path.splitext(i)
            if file_extension in heic_ext:
                print("Exporting {} to jpg".format(file_path))
                new_name = file_name + "_EXPORTED_BY_SCRIPT"
                heif_file = pyheif.read(file_path)
                image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw", heif_file.mode, heif_file.stride)
                out_path_new = os.path.join(whole_path, new_name)
                image.save(out_path_new + ".jpg", "JPEG")


def main():
    if OS_TYPE.startswith("Windows"):
        windows_warnings()
    args = get_comm_args()
    zip_file = args.zip_file
    out_folder = args.output_folder
    unpack_zip(zip_file, out_folder)
    sort_files(out_folder, args.randomize)
    if not OS_TYPE.startswith("Windows"):
        export_heic_to_jpg(os.path.join(out_folder, "sorted_files"))
    if args.pdf:
        export_to_pdf(out_folder)
    write_log(out_folder)
    if args.checksum:
        write_md5_checksum(out_folder)
    print("Done")

if __name__ == "__main__":
    main()