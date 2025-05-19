from datetime import datetime
import subprocess
import pandas as pd
from pandas import *
import time
import argparse

def run_speed_test(server_id):
    command = "speedtest --server-id="+str(server_id)+" --selection-details --format=csv"
    print('Running command:'+command)
    process = subprocess.run(command, shell=True, capture_output=True) 
    print('server_id:'+str(server_id))
    print(str(process.stdout))
    print(str(process.stderr))
    if process.stdout and "Limit reached" not in str(process.stderr) and "Configuration" not in str(process.stderr):
        output_file.write(str(process.stdout)+',"'+str(datetime.now())+'","'+str("-")+'"\n')
    print("")
    return process


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', '-i', type=str, default='speedtest_servers_second_run.csv', help='Input file with speed test server data (default is speedtest_servers_second_run.csv)')
    parser.add_argument('--server-id-column', '-c', type=str, default='id', help='Column name for server ID in input file (default is id)')
    parser.add_argument('--start-row', '-s', type=int, default=0, help='Input file row number to start at (default is 0)')
    args = parser.parse_args()

    # speed_test_server_data = read_csv("ookla_speed_test_servers.csv")
    speed_test_server_data = read_csv(str(args.input_file))
    print("Read input file with ookla test server data: "+str(args.input_file))
    # df = pd.DataFrame(speed_test_server_data)
    # df.info()

    server_ids = speed_test_server_data[str(args.server_id_column)].to_list()

    server_ids_row_to_start = args.start_row
    # server_ids_row_to_start = input("Enter the row number to start at (default is 0): ")
    try:
        server_ids_row_to_start = int(server_ids_row_to_start)
    except ValueError:
        server_ids_row_to_start = 0

    output_file_header = '"server name","server id","idle latency","idle jitter","packet loss","download","upload","download bytes","upload bytes","share url","download server count","download latency","download latency jitter","download latency low","download latency high","upload latency","upload latency jitter","upload latency low","upload latency high","idle latency low","idle latency high","start time","source"\n'
    output_file = open('TEST_global_internet_speed_test_output_'+str(datetime.timestamp(datetime.now()))+'.csv', 'w+')
    print(output_file_header)
    output_file.write(output_file_header)

    for i in range(server_ids_row_to_start, len(server_ids)):
        server_id = server_ids[i]
        process = run_speed_test(server_id)
        while "Limit reached" in str(process.stderr):
            time.sleep(3610)
            process = run_speed_test(server_id)

        time.sleep(3)
    output_file.close()


#Nice To Have Improvements:
# 1. Add a command line argument to specify the output file name and/or row of file to start at.
# 2. Record all output to a log file.
# 3. Add test start time and source IP address to the output file.
# 4. Add a command line argument to specify when the script should start running. 
#    This can be used to schedule a second instance of the script to run on a second machine to overcome API rate limits.
#  Note: API allows 30 tests per hour. Rate limit does not appear to be based on IP address.
#        30 tests take roughly 15-17 minutes to run.
# SOLUTION: To solve most problems above run script as follows:
# sleep 10 && python3 global_internet_speed_test_enhanced.py -s 2 &>> console_output.log
# sleep 10 && python3 global_internet_speed_test_enhanced.py -s 2 2>&1 | tee -a console_output.log
# redirecting stdout and stderr to a log file did not work as expected.
# 5. Improve Error handling. TimeoutException should be handled and retried.
