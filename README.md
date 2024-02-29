# Python NVTD Analysis
An open-source program to analyze spontaneous sympathetic neurohemodynamic transduction using python. [Link to paper.](https://pubmed.ncbi.nlm.nih.gov/33596745/)

Automates transduction analysis based off of the paper's [spreadsheet](https://doi.org/10.6084/m9.figshare.13692139), using sheet 'Overall_NVTD'.

## Setup
Make sure required python packages are installed

    python -m pip install pandas, openpyxl

### Copy your data pad into an excel sheet
1. Open your .adicht file in LabChart
2. Open the datapad by clicking 'Data Pad View' in the Data Pad section of the taskbar
3. Highlight the data using <Ctrl+a> or <⌘+a>
4. Copy and paste the data into an empty excel spreadsheet and save the file
   
## Running the analysis
Running the analysis requires two arguments, the path to the data pad spreadsheet and whether you want to use mean arterial pressure (MAP) or mean diastolic pressure (MDP).

For using MAP:

    $ python datapad_analysis.py /path/to/spreadsheet.xlsx MAP

For using MDP:

    $ python datapad_analysis.py /path/to/spreadshit.xlsx MDP


The output will look like the following:

    Max average absolute change: ###.##
    Max absolute percent change: ###%

## Differences of Analysis
This analysis does some things differently than in the paper, the differences are highlighted below.

- 