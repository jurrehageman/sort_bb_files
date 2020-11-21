# Sort BB files

- Sorts files downloaded from a BB test in folders.
- Converts heic files to jpg files.
- Generates a bundled pdf document for all jpg pictures for each student.

## Getting Started

These instructions will show some examples to run the script.

### Prerequisites

`pillow` and `pyheif` need to be installed on your system.


### Installing

Use pip to install `pillow`.

```
pip3 install pillow
```

Use pip to install `pyheif`

```
pip3 install pyheif
```

## Running the sort2folder.py module:

This module will sort files in folders, convert HEIC files to jpg files and will generate bundled pdf files. 

> Important note:
> The pyheif module does not work in Windows.
> This script will run on Winsows but HEIC files will not be converted to jpg!
> We recommend to use Mac/Linux.

Mac/Linux:
First make the file executable:

```
chmod u+x sort2folder.py
```
Then run the script.  
Example Mac/Linux:
```
./sort2folder.py -pcr test.zip outdirname
```
On windows:
```
python sort2folder.py -pcr test.zip outdirname
``` 

### Arguments:

Required arguments:
- `zip_file`: path to the zip file
- `output_folder`: path to the output folder

Optional arguments:
- `--pdf or -p`: bundles all jpg files per student to pdf 
- `--checksum or -c`: creates csv file with md5 checksums for all files. Use Excel conditional formatting to find duplicates.
- `--randomize or -r`: adds a random prefix to student numbers to randomize folder/file sequence.
- `--help or -h`: shows help on running the script.


## Authors

Jurre Hageman & Mark Sibbald

## License

This project is licensed under the GNU General Public License (GPL).