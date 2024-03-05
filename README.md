# Python Spontaneous NVTD Analysis
An open-source program to analyze spontaneous sympathetic neurohemodynamic transduction using python based on this [paper](https://pubmed.ncbi.nlm.nih.gov/33596745/).

Analysis is done using the methods in the paper's [analysis spreadsheet](https://doi.org/10.6084/m9.figshare.13692139).

## Setup
Make sure the required python packages are installed:

    $ python -m pip install pandas, openpyxl

### Copy your data pad into an excel sheet
1. Open your .adicht file in LabChart
2. Open the datapad by clicking 'Data Pad View' in the Data Pad section of the taskbar
3. Highlight the data using <Ctrl+a> or <⌘+a>
4. Copy and paste the data into an empty excel spreadsheet and save the file
   
## Running the analysis
Running the analysis requires the path to the data pad spreadsheet:

    $ python run.py /path/to/spreadsheet.xlsx

## Notes
This analysis does some things differently than in the paper, the differences are highlighted below.

- The sheet titled '**Overall_NVTD**' in the paper's analysis spreadsheet skips a cardiac cycle between CC5 and CC6 under '**TRACKING ABSOLUTE VALUES**'. This is accounted for in this program.