# Python Spontaneous NVTD Analysis
An open-source program to analyze spontaneous sympathetic neurohemodynamic transduction using python based on this [paper](https://pubmed.ncbi.nlm.nih.gov/33596745/).

Analysis is done using the methods in the paper's [analysis spreadsheet](https://doi.org/10.6084/m9.figshare.13692139).

## Setup
### Participant data formatting
1. Open your .adicht file in LabChart
2. Open the datapad by clicking 'Data Pad View' in the Data Pad section of the taskbar
3. Highlight the data using <Ctrl+a> or <⌘+a>
4. Copy and paste the data into an empty excel spreadsheet and save the file
5. Repeat for each participant in a separate sheet within the file, naming each sheet with the participant ID (example below)
![alt text](https://github.com/anseljohn/Python_MSNA_Analysis/blob/master/img/sheet_naming.png?raw=true)

### Install required python packages
 Make sure the required python packages are installed:

    $ python -m pip install pandas, openpyxl, xlsxwriter

### (Optional) Set up the output excel spreadsheet
TODO: Add screenshot of Miguel's output spreadsheet format + instructions

## Running the analysis
Running the analysis requires the path to the data pad spreadsheet:

    $ python run.py /path/to/spreadsheet.xlsx

## Notes
This analysis does some things differently than in the paper, the differences are highlighted below.

- The sheet titled '**Overall_NVTD**' in the paper's analysis spreadsheet skips a cardiac cycle between CC5 and CC6 under '**TRACKING ABSOLUTE VALUES**'. This is accounted for in this program.