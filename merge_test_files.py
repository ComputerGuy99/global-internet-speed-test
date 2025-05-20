import pandas as pd
from datetime import datetime

file_a_path = "UPDATED_global_internet_speed_test_output_1746689101.842129_Manually_Cleaned.csv" #file from initial run of map_speed_test_results_enhanced.py
file_b_path = "UPDATED_TEST_global_internet_speed_test_output_1747601245.872089.csv" #file from second run of map_speed_test_results_enhanced.py using skipped servers list

file_a_data = pd.read_csv(str("./script_outputs/")+file_a_path)
file_a_df = pd.DataFrame(file_a_data)
file_a_df.info()

file_b_data = pd.read_csv(str("./script_outputs/")+file_b_path)
file_b_df = pd.DataFrame(file_b_data)
file_b_df.info()

merged_df = pd.concat([file_a_df, file_b_df])

# simply removing rows for which a speed test was not run. (i.e. id exists but no server id)
merged_df = merged_df.dropna(subset=['server id'])

merged_df.to_csv('merged_output_files_'+file_a_path+'_AND_'+file_b_path+'_ON_'+str(datetime.timestamp(datetime.now()))+'.csv', index=True)
