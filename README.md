# Sort BB files

- Sorts files downloaded from a BB test in folders.
- Converts heic files in jpg files.
- Generates bundled pdf document for all jpg pictures per student.

## Getting Started

These instructions will show some examples to run the scripts

### Prerequisites

`Pillow` and `pyheif` needs to be installed on your system


### Installing

Use pip to install `Pillow`.

```
pip3 install pillow
```

Use pip to install `pyheif`

```
pip3 install pyheif
```

## Running the sort2folder.py module:

This module will sort files in folders and will generate bundled pdf files.

Mac/Linux:
First make the file executable:

```
chmod u+x sort2folder.py
```
Then run the script
Example Mac/Linux:
```
./sort2folder.py -pcr test.zip outdirname
```
On windows:
```
python sort2folder.py -pcr test.zip outdirname
```
Warning: The pyheif module will not work on Windows so we do not recommend to use Windows. 

### Arguments:

Required arguments:
- `zip_file`: path to the zip file
- `output_folder`: path to the output folder

Optional arguments:
- `--pdf or -p`: bundles all jpg files per student to pdf 
- `--checksum or -c`: creates csv file with md5 checksums for all files. Use Excel conditional formatting to find duplicates.
- `--randomize or -r`: adds random numbers to student numbers to randomize folder/file sequence.
- `--help or -h`: shows help on arguments.


## Authors

Jurre Hageman & Mark Sibbald

## License

This project is licensed under the GNU General Public License (GPL)