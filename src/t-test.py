from scipy import stats
import pandas as pd

runtime_df = pd.read_excel('metrics\\runtime.xlsx')

interval_runtimes = runtime_df['Intervals'].tolist()
pentagon_runtimes = runtime_df['Pentagon'].tolist()

result = stats.ttest_ind(interval_runtimes, pentagon_runtimes)
print("result:", result)
