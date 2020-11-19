import os
import sys
import shutil
from zipfile import ZipFile
from PIL import Image
import platform
import warnings
import hashlib
#PLATFORM
OS_TYPE = platform.platform()
if not OS_TYPE.startswith("Windows"):
    import pyheif


#SETTINGS
pdf_export = True
MAX_PATH = 260

#FILE LOCATIONS
zip_in_loc = os.path.join(".", "place_zip_here")
zip_out_loc = os.path.join(".", "unzipped_files")
file_destination = os.path.join(".", "your_sorted_files")
pdf_destination = os.path.join(".", "your_pdf_files")
log_destination = os.path.join(".", "your_log_file")
md5_destination = os.path.join(".", "your_md5_file")

#ERROR FLAGS
jpg_to_pdf_err = False

def is_jpg(filename):
    try:
        i=Image.open(filename)
        return i.format =='JPEG'
    except IOError:
        return False

def make_folders(folders):
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

def unpack_zip(zip_in_loc, zip_out_loc):
    all_files = os.listdir(zip_in_loc)
    #For Mac-users (.DS_Store hidden file is created)
    for i in all_files:
        if i.startswith(".DS"):
            all_files.remove(i)
    if len(all_files) < 1:
        print("No files in folder:", zip_in_loc)
        sys.exit()
    elif len(all_files) > 1:
        print("Only one file is allowed. Found multiple files in folder:", zip_in_loc)
        sys.exit()
    file_name, file_extension = os.path.splitext(all_files[0])
    if not file_extension == ".zip":
        print(file_name + file_extension, "is not a zip file. Only zip files are allowed.")
        sys.exit()
    print("Extracting zip file...")
    full_path = os.path.join(zip_in_loc, all_files[0])
    # Windows MAX_PATH may be limited to 260 in registry
    if OS_TYPE.startswith("Windows"):
        warnings.warn("HEIC to jpg conversion will not work on Windows")
        len_path_zip = len(os.getcwd() + full_path[1:])
        if len_path_zip > (MAX_PATH - len(all_files[0])):
            warnings.warn("You are approaching Windows MAX_PATH which is limited to 260 characters. If unzipping fails, run this script from de Desktop.")
    with ZipFile(full_path, 'r') as zipObj:
        zipObj.extractall(zip_out_loc)
    print("Zip file extracted")


def read_files(source, destination):
    all_files = os.listdir(source)
    students = []
    for i in all_files:
        #For Mac-users (__MACOSX folder is created)
        if i.startswith("__MAC"):
            continue
        whole_path = os.path.join(source, i)
        student = i.split("_")[1]
        out_path = os.path.join(destination, student)
        if not os.path.exists(out_path):
            os.mkdir(out_path)
        out_path_file = os.path.join(out_path, i)
        if not student in students:
            print("Sorting files to", student)
            students.append(student)
        shutil.copyfile(whole_path, out_path_file)


def export_to_pdf(jpg_destination, pdf_destination):
    global jpg_to_pdf_err
    first_image_obj = None
    jpg_ext = ".jpg .JPG .jpeg .JPEG".split()
    print("Exporting to pdf...")
    all_folders = os.listdir(jpg_destination)
    for subfolder in all_folders:
        whole_path = os.path.join(jpg_destination, subfolder)
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
                    print("file", file_path, "is not a valid jpg file")
                    jpg_to_pdf_err = True
                    continue
        if first_image_obj:
            first_image_obj.save(pdf_filename, "PDF", resolution=100.0, save_all=True, append_images=image_list)


def write_log(zip_out_loc, log_destination):
    full_path = os.path.join(log_destination, "log_file.txt")
    pic_to_skip = ".jpg .jpeg .JPG .JPEG".split()
    others_to_skip = [".txt"]
    with open(full_path, "w") as f:
        f.write("Files with other extension then jpg or txt\n")
        f.write("or files with .jpg extension but fail jpg integrity test:\n\n")
        all_files = os.listdir(zip_out_loc)
        for i in all_files:
            file_name, file_extension = os.path.splitext(i)
            if not file_extension in pic_to_skip and file_extension not in others_to_skip:
                f.write(i + "\n")
            elif not is_jpg(os.path.join(zip_out_loc, i)) and file_extension not in others_to_skip:
                print(i)
                f.write(i + "\n")

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def write_md5_checksum(zip_out_loc, log_destination):
    full_path = os.path.join(log_destination, "file_hashes.csv")
    with open(full_path, "w") as csv:
        csv.write("Filepath; MD5 checksum\n\n")
        all_files = os.listdir(zip_out_loc)
        for i in all_files:
            file_path = os.path.join(zip_out_loc, i)
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
    folders = [zip_out_loc, file_destination, log_destination, md5_destination]
    if pdf_export:
        folders.append(pdf_destination,)
    make_folders(folders)
    unpack_zip(zip_in_loc, zip_out_loc)
    read_files(zip_out_loc, file_destination)
    if OS_TYPE.startswith("Linux") or OS_TYPE.startswith("Darwin") or OS_TYPE.startswith("macOS"):
        export_heic_to_jpg(file_destination)
    if pdf_export:
        export_to_pdf(file_destination, pdf_destination)
    write_log(zip_out_loc, log_destination)
    write_md5_checksum(zip_out_loc, md5_destination)
    print("Files are sorted to", file_destination)
    if pdf_export:
        print("PDF file is saved to", pdf_destination)
    print("Log file saved to", log_destination)
    print("MD5 checksum saved to", md5_destination)
    if jpg_to_pdf_err:
        print("Corrupt jpg encountered. See log file for details")
    print("Done")

if __name__ == "__main__":
    main()