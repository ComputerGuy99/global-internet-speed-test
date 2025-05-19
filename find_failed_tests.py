from datetime import datetime
import subprocess
import pandas as pd
from pandas import *
import time
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--server-list', '-s', type=str, default='speedtest_servers_second_run.csv', help='Input file with speed test server data (default is speedtest_servers_second_run.csv)')
    parser.add_argument('--server-list-id-col', '-slc', type=str, default='id', help='Column name for server ID in test server data file (default is id)')
    parser.add_argument('--test-results-file', '-r', type=str, default='global_internet_speed_test_output_1746689101.842129_Manually_Cleaned.csv', help='Input file with speed test results (default is global_internet_speed_test_output_1746689101.842129_Manually_Cleaned.csv)')
    parser.add_argument('--test-results-id-col', '-trc', type=str, default='server id', help='Column name for server ID in test results file (default is server id)')
    args = parser.parse_args()

    speed_test_server_data = read_csv(str(args.server_list))
    print("Read input file with ookla test server data: "+str(args.server_list))
    test_servers_df = pd.DataFrame(speed_test_server_data)
    test_servers_df.info()

    speed_test_results_data = read_csv("./script_outputs/"+str(args.test_results_file))
    print("Read input file with ookla speed test results data: ./script_outputs/"+str(args.test_results_file))
    test_results_df = pd.DataFrame(speed_test_results_data)
    test_results_df.info()

    # server_ids = speed_test_server_data[str(args.server_id_column)].to_list()

    # Find IDs in test_servers_df but not in test_results_df
    missing_in_test_results_df = test_servers_df[~test_servers_df[str(args.server_list_id_col)].isin(test_results_df[str(args.test_results_id_col)])]

    # Find IDs in test_results_df but not in test_servers_df
    missing_in_test_servers_df = test_results_df[~test_results_df[str(args.test_results_id_col)].isin(test_servers_df[str(args.server_list_id_col)])]

    print("IDs in test_servers_df but not in test_results_df:")
    print(missing_in_test_results_df)
    print("\nIDs in test_results_df but not in test_servers_df:")
    print(missing_in_test_servers_df)

    # Build csv with missing server IDs
    missing_in_test_results_df.to_csv("./script_outputs/skipped_servers_"+str(args.test_results_file), index=True)

    # Compute download and upload speeds in mbps
    test_results_df['download_speed_mbps'] = (test_results_df['download'] / 1000000) * 8
    test_results_df['upload_speed_mbps'] = (test_results_df['upload'] / 1000000) * 8

    # Build test results csv with server details
    updated_results_df = pd.merge(test_servers_df, test_results_df, left_on=str(args.server_list_id_col), right_on=str(args.test_results_id_col), how='left')
    updated_results_df.to_csv("./script_outputs/UPDATED_"+str(args.test_results_file), index=True)