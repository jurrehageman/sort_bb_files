import os
import sys
import shutil
from zipfile import ZipFile
from PIL import Image
import platform
import warnings

#FILE LOCATIONS
zip_in_loc = os.path.join(".", "place_zip_here")
zip_out_loc = os.path.join(".", "unzipped_files")
file_destination = os.path.join(".", "your_sorted_files")
pdf_destination = os.path.join(".", "your_pdf_files")
log_destination = os.path.join(".", "your_log_file")

#PLATFORM
OS_TYPE = platform.platform()
MAX_PATH = 260

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
    jpg_ext = ".jpg .JPG .jpeg .JPEG".split()
    print("Exporting to pdf...")
    all_folders = os.listdir(jpg_destination)
    for subfolder in all_folders:
        whole_path = os.path.join(jpg_destination, subfolder)
        all_files = os.listdir(whole_path)
        image_list = []
        pdf_filename = os.path.join(pdf_destination, subfolder + ".pdf")
        print("Now processing", pdf_filename)
        jpg_counter = 0
        for i in all_files:
            file_path = os.path.join(whole_path, i)
            file_name, file_extension = os.path.splitext(i)
            if file_extension in jpg_ext:
                if jpg_counter == 0:
                    first_image_obj = Image.open(file_path)
                else:
                    image_obj = Image.open(file_path)
                    image_list.append(image_obj)
                jpg_counter += 1
        first_image_obj.save(pdf_filename, "PDF", resolution=100.0, save_all=True, append_images=image_list)


def write_log(zip_out_loc, log_destination):
    full_path = os.path.join(log_destination, "log_file.txt")
    ext_to_skip = ".jpg .jpeg .JPG .JPEG .txt".split()
    with open(full_path, "w") as f:
        f.write("Files with other extension then " + ",".join(ext_to_skip) + ":\n\n")
        all_files = os.listdir(zip_out_loc)
        for i in all_files:
            file_name, file_extension = os.path.splitext(i)
            if not file_extension in ext_to_skip:
                f.write(i + "\n")

def main():
    make_folders([zip_out_loc, file_destination, pdf_destination, log_destination])
    unpack_zip(zip_in_loc, zip_out_loc)
    read_files(zip_out_loc, file_destination)
    export_to_pdf(file_destination, pdf_destination)
    write_log(zip_out_loc, log_destination)
    print("Files are sorted to", file_destination)
    print("PDF file is saved to", pdf_destination)
    print("Log file saved to", log_destination)
    print("Done")

if __name__ == "__main__":
    main()