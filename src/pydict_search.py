# Python3 code to demonstrate working of
# Keys with specific suffix in Dictionary
# Using dictionary comprehension + endswith()
  
# Initialize dictionary
import pandas as pd
from os.path import join, dirname

df = pd.read_csv(join(dirname(__file__), '../data/jisx0402.csv'), index_col='city', usecols=['city','pref'])

# test_dict = {'all' : 4, 'geeks' : 5, 'are' : 8, 'freaks' : 10}
test_dict = dict(zip(df.index, df['pref']))

# printing original dictionary
# print("The original dictionary : " + str(test_dict))
  
# Initialize suffix
test_suf = '中央区'
  
# Using dictionary

# Keys with specific preffix in Dictionary
# res = {key:val for key, val in test_dict.items() if key.startswith(test_suf)}

# Keys with specific suffix in Dictionary
# res = {key:val for key, val in test_dict.items() if key.endswith(test_suf)}

# Keys with specific constraints in Dictionary
import re
res = {key:val for key, val in test_dict.items() if re.search(test_suf, key)}

  
# printing result 
print("Filtered dictionary keys are : " + str(res))
