import numpy as np
import renew as rn
import power
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({'font.size': 16})

# Reads the configure file to create and set the needed variables
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

# Creates the filename based on the date inputted.
name = date.replace('/','-')
filename = name + '.csv'
# Solves for the date number with Jan. 1 = 1
day = pd.to_datetime(date, format='%m/%d/%Y')
new_year_day = pd.Timestamp(year=day.year, month=1, day=1)
date = (day - new_year_day).days + 1

# Reads and saves the Actual Data from the selected date.
df = pd.read_csv(filename)
actual = []
for x in range(0, len(df.index)):
    if df.loc[x, 'Solar [kW]']<0:
        df.at[x, 'Solar [kW]'] = 0
    actual.insert(0, df.loc[x, 'Solar [kW]'])

# Calls the appropriate functions in power.py to solve for the irradiances and power
clear_irradiance, clear_power, irradiance, power = power.YearlyPower(lat, long_std, long_loc, beta, gamma, area_panel, n_panels, eff, inv_eff)
clear_irradiance = np.array(clear_irradiance)
scaled_clear_power = np.array(clear_power) / 1000
irradiance = np.array(irradiance)
scaled_power = np.array(power) / 1000

plt.close()

# Creates the time vector to plot against
X1 = []
for hour in range(0,24*12+1):
	X1.append(hour/12)

plt.rcParams.update({'font.size': 26})

########## BEGIN figure 1 ##########

f1 = plt.figure(1)
ax1 = plt.subplot(111)

#Power
color = 'tab:red'
date = '12/21'
ax1.plot(X1, scaled_clear_power[rn.DayOfTheYear(date)-1], color=color, linewidth=5, label=rn.dateToWords(date)+', $\gamma$=46')
date = '06/21'
ax1.plot(X1, scaled_clear_power[rn.DayOfTheYear(date)-1], color=color, linestyle='dashed', linewidth=5, label=rn.dateToWords(date)+', $\gamma$=46')
# ax1.plot(X1, scaled_power_gamma0[rn.DayOfTheYear(date)-1], color=color, linestyle='dotted', linewidth=3, label=rn.dateToWords(date)+', $\gamma$=0')
ax1.set_ylabel('Power [kW]', fontsize=30)
ax1.tick_params(axis='y')
ax1.set_ylim((0,250))
ax1.legend(loc='upper left')
ax1.grid()

plt.tick_params(axis = 'x')
plt.title('Power vs Time', fontsize=36)
plt.xlim(0,24)

f1.tight_layout()
f1.show()

########## END figure 1 ##########

########## BEGIN figure 2 ##########
# file = open('data.csv')
# reader = csv.reader(file)
# PEC_power = []
# for row in reader:
#     PEC_power.append(row[2])
# PEC_power.reverse()
# PEC_power.pop()
# PEC_power = [float(x) for x in PEC_power]
# PEC_power = [0 if x<0 else x for x in PEC_power]

f2 = plt.figure(2)
ax2 = plt.subplot(111)

color = 'tab:red'
date = '03/26'
ax2.plot(X1, scaled_clear_power[rn.DayOfTheYear(date)-1], color=color, linewidth=5, label='Model')
color= 'tab:blue'
ax2.plot(X1, actual, color=color, linewidth=5, label='PEC')
ax2.set_xlabel('Local Time [hours]', fontsize=30)
ax2.set_ylabel('Power [kW]', fontsize=30)
ax2.tick_params(axis='y')
ax2.set_ylim((0,200))
ax2.legend(loc='upper left')
ax2.grid()

plt.title('Model Power Production vs PEC Power (' + date + ')', fontsize=36)
plt.xlim(0,24)

f2.tight_layout()
f2.show()

plt.show()


# f1 = plt.figure()
# ax1 = plt.subplot(111)

# # Plots the Irradiance values for the selected date.
# ax1.plot(X, clear_irradiance[date], color='C0', linewidth=3, label=name+' - CLEAR MODEL')
# ax1.plot(X, irradiance[date], color='C2', linewidth=3, label=name+'- MODEL')
# ax1.set_xlabel('Local Time [hours]', fontsize=18)
# ax1.set_ylabel('Irradiance [W/m^2]', fontsize=18)
# ax1.tick_params(axis='y')
# ax1.set_ylim((0,1000))
# ax1.legend(loc='upper left')
# ax1.grid()

# ax2 = ax1.twinx()

# # Plots the Power values for the selected date. 
# ax2.plot(X, scaled_clear_power[date], color='C1', linewidth=3, label=name+' - CLEAR MODEL')
# ax2.plot(X, scaled_power[date], color='C3', linewidth=3, label=name+'- MODEL')
# ax2.plot(X, actual, linewidth=3, color='C4', label=name+'- Actual Data')
# ax2.set_ylabel('Power [kW]', fontsize=18)
# ax2.tick_params(axis='y')
# ax2.set_ylim((0,250))
# ax2.legend(loc='upper right')

# plt.tick_params(axis = 'x')
# plt.title('Irradiance and Power vs Time', fontsize=20)
# plt.xlim(0,24)

# f1.tight_layout()
# f1.show()
# plt.show()
