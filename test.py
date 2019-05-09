#Renewable Energy Technology
#Case 1

# import math as m
import numpy as np
import renew as rn
import power as pwr
import matplotlib.pyplot as plt
import csv

lat = 30.2672
long_std = 90
long_loc = 97.7431
beta =22
gamma = 46
area_panel = 1.6236 # m^2
n_panels = 960
eff = 0.157

########## BEGIN Bullets 1, 2, & 3 ##########
irradiance, power, irradiance_ratio_horiz, theta_i_array = pwr.YearlyPower(lat, long_std, long_loc, beta, gamma, area_panel, n_panels, eff)
irradiance = np.array(irradiance)
scaled_power = np.array(power) / 1000

gamma = 0
irradiance_gamma0, power_gamma0, irradiance_ratio_horiz_gamma0, theta_i_array_gamma0 = pwr.YearlyPower(lat, long_std, long_loc, beta, gamma, area_panel, n_panels, eff)
irradiance_gamma0 = np.array(irradiance_gamma0)
scaled_power_gamma0 = np.array(power_gamma0) / 1000

#Creating x-axis for time of day
X1 = []
for hour in range(0,24*12+1):
	X1.append(hour/12)

plt.rcParams.update({'font.size': 26})

f1 = plt.figure(1)
ax1 = plt.subplot(111)

# #Irradiance
# color = 'tab:blue'
# date = '12/21'
# ax1.plot(X1, irradiance[rn.DayOfTheYear(date)-1], color=color, linewidth=3, label=rn.dateToWords(date))
# date = '06/21'
# ax1.plot(X1, irradiance[rn.DayOfTheYear(date)-1], color=color, linestyle='dashed', linewidth=3, label=rn.dateToWords(date))
# ax1.set_xlabel('Local Time [hours]', fontsize=18)
# ax1.set_ylabel('Irradiance [W/m^2]', color=color, fontsize=18)
# ax1.tick_params(axis='y', labelcolor=color)
# ax1.set_ylim((0,1000))
# ax1.legend(loc='upper left')
# ax1.grid()

# ax2 = ax1.twinx()

#Power
color = 'tab:red'
date = '12/21'
ax1.plot(X1, scaled_power[rn.DayOfTheYear(date)-1], color=color, linewidth=5, label=rn.dateToWords(date)+', $\gamma$=46')
date = '06/21'
ax1.plot(X1, scaled_power[rn.DayOfTheYear(date)-1], color=color, linestyle='dashed', linewidth=5, label=rn.dateToWords(date)+', $\gamma$=46')
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
########## END of Bullets 1, 2, & 3 ##########

########## BEGIN Bullet 4 ##########
f2 = plt.figure(2)
ax3 = plt.subplot(111)

#ratio of beam to diffuse radiation
color = 'tab:blue'
date = '06/21'
ax3.plot(X1, irradiance_ratio_horiz[rn.DayOfTheYear(date)-1], color=color, linewidth=3)
ax3.set_xlabel('Local Time [hours]', fontsize=18)
ax3.set_ylabel('I_c_b / I_c_d', color=color, fontsize=18)
ax3.tick_params(axis='y', labelcolor=color)
ax3.grid()

plt.title('Ratio of Beam to Diffuse Irradiance for a Flat Surface (' + date + ')', fontsize=20)
plt.xlim(0,24)

f2.tight_layout()
f2.show()
########## END Bullet 4 ##########

########## BEGIN Bullet 5 ##########
theta_i_at_noon = []
for day in range(1, len(theta_i_array)+1):	
	if day >= 69 and day <307: #counteracts DST
		theta_i_at_noon.append(theta_i_array[day-1][145+12])
	else:
		theta_i_at_noon.append(theta_i_array[day-1][145])

daily_energy_production = []
for day in power:
	daily_energy_production.append(np.trapz(day, dx=1/12))
daily_energy_production = np.array(daily_energy_production)
scaled_daily_energy_production = np.array(daily_energy_production) / 1e6

#Creating x-axis for day of the year
X2 = []
for day in range(1,366):
	X2.append(day)

f3 = plt.figure(3)
ax4 = plt.subplot(111)

#angle of incidence at noon
color = 'tab:blue'
ax4.plot(X2, theta_i_at_noon, color=color, linewidth=3)
ax4.set_xlabel('Day of the Year', fontsize=18)
ax4.set_ylabel('Angle of Incidence at Noon', color=color, fontsize=18)
ax4.tick_params(axis='y', labelcolor=color)
ax4.grid()

ax5 = ax4.twinx()

#energy production
color = 'tab:red'
ax5.plot(X2, scaled_daily_energy_production, color=color, linewidth=3)
ax5.set_xlabel('Day of the Year', fontsize=18)
ax5.set_ylabel('Daily Energy Production (MWh)', color=color, fontsize=18)
ax5.tick_params(axis='y', labelcolor=color)

plt.title('Angle of Incidence and Daily Energy Production vs Day of The Year')
plt.xlim(1,365)

f3.tight_layout()
f3.show()
########## END Bullet 5 ##########

########## BEGIN Bullet 6 ##########
file = open('data.csv')
reader = csv.reader(file)
PEC_power = []
for row in reader:
	PEC_power.append(row[2])
PEC_power.reverse()
PEC_power.pop()
PEC_power = [float(x) for x in PEC_power]
PEC_power = [0 if x<0 else x for x in PEC_power]

f4 = plt.figure(4)
ax6 = plt.subplot(111)

color = 'tab:red'
date = '03/26'
ax6.plot(X1, 0.75*scaled_power[rn.DayOfTheYear(date)-1], color=color, linewidth=5, label='Model')
color= 'tab:blue'
ax6.plot(X1, PEC_power, color=color, linewidth=5, label='PEC')
ax6.set_xlabel('Local Time [hours]', fontsize=30)
ax6.set_ylabel('Power [kW]', fontsize=30)
ax6.tick_params(axis='y')
ax6.set_ylim((0,200))
ax6.legend(loc='upper left')
ax6.grid()

plt.title('Model Power Production vs PEC Power (' + date + ')', fontsize=36)
plt.xlim(0,24)

f4.tight_layout()
f4.show()
########## END Bullet 6 ##########

plt.show()