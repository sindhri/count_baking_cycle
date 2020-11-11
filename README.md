# Use power and energy to count the number of baking cycles

## files
<table>
    <tr>
        <th>File Name</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>main.py</td>
        <td>run the calculation on the csv file</td>
    </tr>
    <tr>
        <td>baking_cycle_by_steps.ipynb</td>
        <td>Step by step calculation with visualizations</td>
    </tr>
</table>

## Dataset
* Use the time series power and energy data to count baking cycle
* The time series has a frequency of one data per ~1 minute
* Column power_total showes power at each time point in watts
* Column energy_total showes accumulative energy at each time point in kWh
* The data includes 13 full-day records from 10/1 to 10/13

## 1. Import and visualization
## 2. Resample the data to have a consistent interval
## 3. Mark the onset and calculate the duration of each large spike
* minimum height is 1/2 of the maximum power_total
* minimum width is 12 minutes (based on two reasons: 1, subway baking cycle ranges from 12-15 minutes, 2, no pattern was observed within each spike, thus the flucturation within each spike is likely to be random)
## 4. Observe the pattern within each spike
* Could not observe any pattern that may associate with baking cycles within each spike
## 5. Calculate the number of baking cycle based on minimum width
