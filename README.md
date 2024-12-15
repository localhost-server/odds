# Instructions

## Setup

### R

Install the `reticulate` package:

```r
install.packages("reticulate")
```

### Python

- Download and install [Python 3.11.1](https://www.python.org/downloads/);
- Double click on the `Update Shell Profile.command` file on the Finder window that popped up. 

You should see the following in your terminal (which you can close):

```
This script will update your shell profile when the 'bin' directory
of python is not early enough of the PATH of your shell.
These changes will be effective only in shell windows that you open
after running this script.
All right, you're a python lover already
logout
Saving session...
...copying shared history...
...saving history...truncating history files...
...completed.
Deleting expired sessions...633 completed.

[Process completed]
```

Create and activate a new python virtual environment to install package dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies with:

```bash
python3 -m pip install -r requirements.txt
playwright install
```

## Usage

Run the `master.R` script from within Rstudio. 

You should see a `odds-data-table.html` saved in the `data/` folder.
