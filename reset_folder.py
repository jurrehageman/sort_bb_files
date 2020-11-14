import shutil
import os

zip_out_loc = os.path.join(".", "unzipped_files")
jpg_destination = os.path.join(".", "your_sorted_files")
pdf_destination = os.path.join(".", "your_pdf_files")
log_destination = os.path.join(".", "your_log_file")
md5_destination = os.path.join(".", "your_md5_file")


def remove_folders(folders):
    for folder in folders:
        try:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(folder, "deleted")
        except OSError as e:
            print("Error: %s : %s" % (log_destination, e.strerror))
    print("Unsorted files cleaned")


def main():
    print("Cleaning files")
    remove_folders([zip_out_loc, jpg_destination, pdf_destination, log_destination, md5_destination])
    print("Files cleaned")


if __name__ == "__main__":
    main()