import pandas as pd

car = pd.read_csv('kaggle_datasets/car_prices.csv')
msrp = pd.read_csv('MSRP.csv')

msrp.info()

car['MSRP'] = pd.NA

#import pandas as pd

# Sample DataFrames
# df1 = pd.DataFrame({'col1': ['A', 'B', 'C', 'D'],
#                     'col2': ['X', 'Y', 'Z', 'W'],
#                     'col3': [1, 2, 3, 4]})
#
# df2 = pd.DataFrame({'col1': ['A', 'B', 'C', 'E'],
#                     'col2': ['X', 'Y', 'Z', 'V'],
#                     'col3': [1, 2, 3, 5],
#                     'value': [100, 200, 300, 400]})
#
# # Create a new column 'new_col' in df1, initialized with NaN
# df1['new_col'] = pd.NA
#
# # Iterate through df1 and check for matching rows in df2
# for index1, row1 in df1.iterrows():
#     for index2, row2 in df2.iterrows():
#         if (row1['col1'] == row2['col1']) and \
#            (row1['col2'] == row2['col2']) and \
#            (row1['col3'] == row2['col3']):
#             df1.loc[index1, 'new_col'] = row2['value']
#             break  # Exit inner loop once a match is found
#
# print(df1)