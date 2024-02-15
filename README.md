An open-source program to analyze spontaneous sympathetic neurohemodynamic transduction using python. [Link to paper.](https://pubmed.ncbi.nlm.nih.gov/33596745/)

Automates transduction analysis based off of the paper's [spreadsheet](https://doi.org/10.6084/m9.figshare.13692139), using sheet 'Overall_NVTD'.

### Setup
Make sure required python packages are installed

    python -m pip install scipy, numpy, matplotlib

#### Export LabChart File as .mat
1. Open your .adicht file in LabChart
2. Click File > Export in the top left
3. Export as .mat
   
### Running the analysis
    $ python analyze.py /path/to/matlab_file.mat "Outcome Variable Name"

    Output:
    Max average absolute change: ###.##
    Max absolute percent change: ###%