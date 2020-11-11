import pandas as pd
import numpy as np

def determine_min_height(data):
    return max(5000, data.power_total.max()/2)

# import the data
data = pd.read_csv("aefa29b4-cf46-46c5-8202-ce9e83408f32.csv", index_col= 'command_execution_date', parse_dates=True)

# resample the original data to 1 timestamp per minute, interplote the missing data using the average of the neighbors
data = data.resample('T').mean()
data = data.interpolate(method='time')

# calculate number of large spikes
min_height = determine_min_height(data)

data['baking'] = data.power_total > min_height
data['baking_last'] = data['baking'].shift(-1)
data['baking_next'] = data['baking'].shift(1)
data['baking_adjustment'] = data['baking_last']*data['baking_next'] # if both the last and next are True, baking_adjust is True
data['baking'] = data['baking'] + data['baking_adjustment']
data['baking'] = data['baking']>0

data['baking_status_change'] = data['baking']!=data['baking'].shift()
data.loc[data.index==0,'baking_status_change']=False

data['baking_count'] = data['baking_status_change'].cumsum()
data['baking_count'] = ((data['baking_count']+1)/2)*data['baking']
data['baking_cum'] = data['baking'].cumsum()*data['baking']

base = data.groupby(['baking_count'])['baking_cum'].min()
data['base'] = data['baking_count'].apply(lambda x: base[x])
data['baking_cum'] = (data['baking_cum'] - data['base']+1)*data['baking']
duration = data.groupby(['baking_count'])['baking_cum'].max()
data['duration'] = data['baking_count'].apply(lambda x: duration[x])

min_width = 12
data['duration'] = data['duration'].apply(lambda x: 0 if x < min_width else x)
data['baking'] = data['duration'] > 0
data['baking_status_change'] = data['baking_status_change'] & data['baking']
data['spike_count'] = data['baking_status_change'].cumsum()
data['spike_count'] = data['spike_count']*data['baking']

num_spikes = data['spike_count'].max()

# calculate number of baking cycle
baking_cycle = duration/min_width
baking_cycle = baking_cycle.astype(int)

num_baking_cycle = baking_cycle.sum()

# print outcome
print('Minimum power_total used', min_height, 'watts')
print('Minimum baking cycle used',min_width,'minutes')
print('Number of spikes found', num_spikes)
print('Number of baking cycles found', num_baking_cycle)