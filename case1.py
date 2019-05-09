#Renewable Energy Technology
#Case 1

# import math as m
import numpy as np
# print(np.__file__)
import renew as rn
import power

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({'font.size': 16})

constants = {}
with open("CONFIG.txt") as config:
    for line in config:
        if line[0]=='*' or line == '\n':
            continue
        else:
            (key, val) = line.rstrip().split(': ')
            if key == 'date':
                constants[key] = val
            else:
                constants[key] = float(val)
locals().update(constants)
std_long = [x * 15 for x in range(0, 24)]
for num in std_long:
    if long_loc>=num and long_loc<num+15:
        long_std = num
        
day = pd.to_datetime(date, format='%m/%d/%Y')
new_year_day = pd.Timestamp(year=day.year, month=1, day=1)
date = (day - new_year_day).days + 1

# Actual Data
df = pd.read_csv('data.csv')
actual = []
for x in range(0, len(df.index)):
    if df.loc[x, 'Solar [kW]']<0:
        df.at[x, 'Solar [kW]'] = 0
    actual.insert(0, df.loc[x, 'Solar [kW]'])

clear_irradiance, clear_power, irradiance, power = power.YearlyPower(lat, long_std, long_loc, beta, gamma, area_panel, n_panels, eff, inv_eff)
clear_irradiance = np.array(clear_irradiance)
scaled_clear_power = np.array(clear_power) / 1000
irradiance = np.array(irradiance)
scaled_power = np.array(power) / 1000

#gamma = 0
#irradiance_gamma0, power_gamma0 = power.YearlyPower(lat, long_std, long_loc, beta, gamma, area_panel, n_panels, eff, inv_eff)
#irradiance_gamma0 = np.array(irradiance_gamma0)
#scaled_power_gamma0 = np.array(power_gamma0) / 1000

X = []
for hour in range(0,24*12+1):
	X.append(hour/12)

f1 = plt.figure()
ax1 = plt.subplot(111)

#Irradiance
color = 'tab:blue'
ax1.plot(X, clear_irradiance[rn.DayOfTheYear('3/26')-1], color=color, linewidth=3, label='Mar. 26 - CLEAR')
ax1.plot(X, irradiance[rn.DayOfTheYear('3/26')-1], color='green', linewidth=3, label='Mar. 26')
ax1.set_xlabel('Local Time [hours]', fontsize=18)
ax1.set_ylabel('Irradiance [W/m^2]', color=color, fontsize=18)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim((0,1000))
ax1.legend(loc='upper left')
ax1.grid()

ax2 = ax1.twinx()

#Power
color = 'tab:red'
ax2.plot(X, scaled_clear_power[rn.DayOfTheYear('3/26')-1], color=color, linewidth=3, label='Mar. 26 - CLEAR')
ax2.plot(X, scaled_power[rn.DayOfTheYear('3/26')-1], color='yellow', linewidth=3, label='Mar. 26')
ax2.plot(X, actual, color='cyan', linewidth=3, label='Actual Data')
ax2.set_ylabel('Power [kW]', color=color, fontsize=18)
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim((0,250))
ax2.legend(loc='upper right')

plt.tick_params(axis = 'x')
plt.title('Irradiance and Power vs Time', fontsize=20)
plt.xlim(0,24)

f1.tight_layout()
f1.show()
plt.show()
