# Read lxb files into Pandas

Read the contents of a Luminex FCS file (file extension 'lxb') and generate a DataFrame of bead fluorescence. The `lxb_parser.py` file contains the function `parse_lxb` which takes a single argument - a string corresponding to the path where your *.lxb files are stored.

The function returns a `Pandas DataFrame` of the containing data. The target directory should be representative of a single Luminex plate and contain *.lxb files for each well. The function concatenates this data into a single `DataFrame` with well's identified by the "Well ID". 

Use the function as an import like so:

```
from lxb_parser import parse_lxb
luminex_df = parse_lxb("/path/to/data")
```

Or, run from command line like so:

```
python lxb_parser.py /path/to/lxb/files /path/to/save.csv
```

If the filepath for saving the DataFrame as a CSV is not provided, it will default to saving the data as "luminex_data.csv" in the current directory.
