########## Importing Necessary Python Modules ##########
import sys
import os
import itertools
import pandas as pd
import sample.analyzer as anlz 

########## Check Validity of Call ##########
if (len(sys.argv) < 2):
    sys.exit("Syntax Error:\n\t$ python analyze.py [path/to/spreadsheet.py]")

########################
#   Helper functions   #
########################
def col_data(df, col_name):
    return df.iloc[:, df.columns.get_loc(col_name)]

#######################
#   Data formatting   #
#######################
xl = pd.ExcelFile(sys.argv[1])
outcome_variables = {"MAP": 7, "DBP": 8} # Outcome variables and their respective indices

col_names = ["SUBID", "Normalized Burst Amplitude",
             "DBP_CC1", "DBP_CC2", "DBP_CC3", "DBP_CC4", "DBP_CC5", "DBP_CC6", "DBP_CC7", "DBP_CC8", "DBP_CC9", "DBP_CC10", "DBP_CC11", "DBP_CC12", "DBP_Avg.",
             "MAP_C1", "MAP_CC2", "MAP_CC3", "MAP_CC4", "MAP_CC5", "MAP_CC6", "MAP_CC7", "MAP_CC8", "MAP_CC9", "MAP_CC10", "MAP_CC11", "MAP_CC12", "MAP_Avg.",
             "T1_DBP_CC1", "T1_DBP_CC2", "T1_DBP_CC3", "T1_DBP_CC4", "T1_DBP_CC5", "T1_DBP_CC6", "T1_DBP_CC7", "T1_DBP_CC8", "T1_DBP_CC9", "T1_DBP_CC10", "T1_DBP_CC11", "T1_DBP_CC12", "T1_DBP_Avg.",
             "T2_DBP_CC1", "T2_DBP_CC2", "T2_DBP_CC3", "T2_DBP_CC4", "T2_DBP_CC5", "T2_DBP_CC6", "T2_DBP_CC7", "T2_DBP_CC8", "T2_DBP_CC9", "T2_DBP_CC10", "T2_DBP_CC11", "T2_DBP_CC12", "T2_DBP_Avg.",
             "T3_DBP_CC1", "T3_DBP_CC2", "T3_DBP_CC3", "T3_DBP_CC4", "T3_DBP_CC5", "T3_DBP_CC6", "T3_DBP_CC7", "T3_DBP_CC8", "T3_DBP_CC9", "T3_DBP_CC10", "T3_DBP_CC11", "T3_DBP_CC12", "T3_DBP_Avg.",
             "T1_MAP_CC1", "T1_MAP_CC2", "T1_MAP_CC3", "T1_MAP_CC4", "T1_MAP_CC5", "T1_MAP_CC6", "T1_MAP_CC7", "T1_MAP_CC8", "T1_MAP_CC9", "T1_MAP_CC10", "T1_MAP_CC11", "T1_MAP_CC12", "T1_MAP_Avg.",
             "T2_MAP_CC1", "T2_MAP_CC2", "T2_MAP_CC3", "T2_MAP_CC4", "T2_MAP_CC5", "T2_MAP_CC6", "T2_MAP_CC7", "T2_MAP_CC8", "T2_MAP_CC9", "T2_MAP_CC10", "T2_MAP_CC11", "T2_MAP_CC12", "T2_MAP_Avg.",
             "T3_MAP_CC1", "T3_MAP_CC2", "T3_MAP_CC3", "T3_MAP_CC4", "T3_MAP_CC5", "T3_MAP_CC6", "T3_MAP_CC7", "T3_MAP_CC8", "T3_MAP_CC9", "T3_MAP_CC10", "T3_MAP_CC11", "T3_MAP_CC12", "T3_MAP_Avg.",
             "Q1_DBP_CC1", "Q1_DBP_CC2", "Q1_DBP_CC3", "Q1_DBP_CC4", "Q1_DBP_CC5", "Q1_DBP_CC6", "Q1_DBP_CC7", "Q1_DBP_CC8", "Q1_DBP_CC9", "Q1_DBP_CC10", "Q1_DBP_CC11", "Q1_DBP_CC12", "Q1_DBP_Avg.",
             "Q2_DBP_CC1", "Q2_DBP_CC2", "Q2_DBP_CC3", "Q2_DBP_CC4", "Q2_DBP_CC5", "Q2_DBP_CC6", "Q2_DBP_CC7", "Q2_DBP_CC8", "Q2_DBP_CC9", "Q2_DBP_CC10", "Q2_DBP_CC11", "Q2_DBP_CC12", "Q2_DBP_Avg.",
             "Q3_DBP_CC1", "Q3_DBP_CC2", "Q3_DBP_CC3", "Q3_DBP_CC4", "Q3_DBP_CC5", "Q3_DBP_CC6", "Q3_DBP_CC7", "Q3_DBP_CC8", "Q3_DBP_CC9", "Q3_DBP_CC10", "Q3_DBP_CC11", "Q3_DBP_CC12", "Q3_DBP_Avg.",
             "Q4_DBP_CC1", "Q4_DBP_CC2", "Q4_DBP_CC3", "Q4_DBP_CC4", "Q4_DBP_CC5", "Q4_DBP_CC6", "Q4_DBP_CC7", "Q4_DBP_CC8", "Q4_DBP_CC9", "Q4_DBP_CC10", "Q4_DBP_CC11", "Q4_DBP_CC12", "Q4_DBP_Avg.",
             "Q1_MAP_CC1", "Q1_MAP_CC2", "Q1_MAP_CC3", "Q1_MAP_CC4", "Q1_MAP_CC5", "Q1_MAP_CC6", "Q1_MAP_CC7", "Q1_MAP_CC8", "Q1_MAP_CC9", "Q1_MAP_CC10", "Q1_MAP_CC11", "Q1_MAP_CC12", "Q1_MAP_Avg.",
             "Q2_MAP_CC1", "Q2_MAP_CC2", "Q2_MAP_CC3", "Q2_MAP_CC4", "Q2_MAP_CC5", "Q2_MAP_CC6", "Q2_MAP_CC7", "Q2_MAP_CC8", "Q2_MAP_CC9", "Q2_MAP_CC10", "Q2_MAP_CC11", "Q2_MAP_CC12", "Q2_MAP_Avg.",
             "Q3_MAP_CC1", "Q3_MAP_CC2", "Q3_MAP_CC3", "Q3_MAP_CC4", "Q3_MAP_CC5", "Q3_MAP_CC6", "Q3_MAP_CC7", "Q3_MAP_CC8", "Q3_MAP_CC9", "Q3_MAP_CC10", "Q3_MAP_CC11", "Q3_MAP_CC12", "Q3_MAP_Avg.",
             "Q4_MAP_CC1", "Q4_MAP_CC2", "Q4_MAP_CC3", "Q4_MAP_CC4", "Q4_MAP_CC5", "Q4_MAP_CC6", "Q4_MAP_CC7", "Q4_MAP_CC8", "Q4_MAP_CC9", "Q4_MAP_CC10", "Q4_MAP_CC11", "Q4_MAP_CC12", "Q4_MAP_Avg.",
             "DBP_Non_Bursts_CC1", "DBP_Non_Bursts_CC2", "DBP_Non_Bursts_CC3", "DBP_Non_Bursts_CC4", "DBP_Non_Bursts_CC5", "DBP_Non_Bursts_CC6", "DBP_Non_Bursts_CC7", "DBP_Non_Bursts_CC8", "DBP_Non_Bursts_CC9", "DBP_Non_Bursts_CC10", "DBP_Non_Bursts_CC11", "DBP_Non_Bursts_CC12", "DBP_Non_Bursts_Avg.",
             "MAP_Non_Bursts_CC1", "MAP_Non_Bursts_CC2", "MAP_Non_Bursts_CC3", "MAP_Non_Bursts_CC4", "MAP_Non_Bursts_CC5", "MAP_Non_Bursts_CC6", "MAP_Non_Bursts_CC7", "MAP_Non_Bursts_CC8", "MAP_Non_Bursts_CC9", "MAP_Non_Bursts_CC10", "MAP_Non_Bursts_CC11", "MAP_Non_Bursts_CC12", "MAP_Non_Bursts_Avg.",
             ]


cumulative_data = []
for participant in xl.sheet_names:
    # Allocate 125 columns of data for the participant
    participant_data = [0]*125

    # Get the participant's sheet
    df = xl.parse(participant)

    # Formatting - getting rid of header
    df.drop([0, 1], inplace=True)
    df.dropna(how="all", inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Additional formatting in case of trailing empty rows
    for index, row in df.iterrows():
        if not isinstance(row["Integrated MSNA"], float):
            df.drop([index], inplace=True)

    ############################################################
    #   Getting required arguments for analyses calculations   #
    ############################################################
    comnums = col_data(df, "Integrated MSNA.1") # The burst comment numbers
    burst_sizes = col_data(df, "Integrated MSNA") # The burst size or "Integrated MSNA max-min"
    data_len = len(comnums) # The default length of data
    burst_checks = []
    normalized_burst_amplitude_percent = [] # Normalize burst sizes

    # Determining bursts from burst comment numbers
    burst_cnt = 0
    for i in range(data_len):
        if (i == 0 and comnums[i] != comnums[i+1]) or comnums[i] != comnums[i-1]:
            burst_checks.append(True)
            burst_cnt += 1
        else:
            burst_checks.append(False)

    # Normalizing burst sizes
    largest_burst = burst_sizes.max() # Grabbing the largest burst
    avg_norm_burst_amp = 0
    burstcnt = 0
    for i in range(data_len):
        if burst_checks[i]:
            avg_norm_burst_amp += burst_sizes[i] / largest_burst * 100
            burstcnt += 1
    avg_norm_burst_amp /= burstcnt

    # Analyzing for DBP and MAP
    dbp_data = col_data(df, "Diastolic")
    map_data = col_data(df, "Mean Arterial BP")
    analyzer = anlz.Analyzer(data_len, burst_checks)
    dbp = analyzer.overall_calculations(dbp_data)
    map = analyzer.overall_calculations(map_data)
    tdbp = analyzer.xtiles(dbp_data, dbp_data, anlz.DivisionMethod.TERTILES)
    tmap = analyzer.xtiles(map_data, dbp_data, anlz.DivisionMethod.TERTILES)
    burst_amplitude_quartiles_dbp = analyzer.xtiles(dbp_data, burst_sizes, anlz.DivisionMethod.QUARTILES)
    burst_amplitude_quartiles_map = analyzer.xtiles(map_data, burst_sizes, anlz.DivisionMethod.QUARTILES)

    #TODO: Write burst amplitude quartiles (using normalized burst amplitude percent)

    dbp_non = analyzer.overall_calculations(dbp_data, for_bursts=False)
    map_non = analyzer.overall_calculations(map_data, for_bursts=False)

    cumulative_data.append(list(itertools.chain([participant],
                                                [avg_norm_burst_amp],
                                                dbp, 
                                                map,
                                                list(itertools.chain(*tdbp)),
                                                list(itertools.chain(*tmap)),
                                                list(itertools.chain(*burst_amplitude_quartiles_dbp)),
                                                list(itertools.chain(*burst_amplitude_quartiles_map)),
                                                dbp_non,
                                                map_non)))
    
if not os.path.exists("./out"):
    os.makedirs("./out")

cum_df = pd.DataFrame(cumulative_data)
cum_df.to_excel("./out/NVTD_Cumulative_Output.xlsx", header=col_names, index=False)
