#Renewable Energy Technology
#Case 1

# import math as m
import numpy as np
# print(np.__file__)
import renew as rn
import power
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 16})

lat = 30.2672
long_std = 90
long_loc = 97.7431
beta =22
gamma = 46
area_panel = 1.6236 # m^2
n_panels = 960
eff = 0.157

irradiance_std, power_std = power.YearlyPower(lat, long_std, long_loc, beta, gamma, area_panel, n_panels, eff)
irradiance_std = np.array(irradiance_std)
scaled_power_std = np.array(power_std) / 1000

gamma = 0
irradiance_gamma0, power_gamma0 = power.YearlyPower(lat, long_std, long_loc, beta, gamma, area_panel, n_panels, eff)
irradiance_gamma0 = np.array(irradiance_gamma0)
scaled_power_gamma0 = np.array(power_gamma0) / 1000

X = []
for hour in range(0,24*12+1):
	X.append(hour/12)

f1 = plt.figure()
ax1 = plt.subplot(111)

#Irradiance
color = 'tab:blue'
ax1.plot(X, irradiance_std[rn.DayOfTheYear('12/21')-1], color=color, linewidth=3, label='Dec. 21')
ax1.plot(X, irradiance_std[rn.DayOfTheYear('6/21')-1], color=color, linestyle='dashed', linewidth=3, label='Jun. 21')
ax1.set_xlabel('Local Time [hours]', fontsize=18)
ax1.set_ylabel('Irradiance [W/m^2]', color=color, fontsize=18)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim((0,1000))
ax1.legend(loc='upper left')
ax1.grid()

ax2 = ax1.twinx()

#Power
color = 'tab:red'
ax2.plot(X, scaled_power_std[rn.DayOfTheYear('12/21')-1], color=color, linewidth=3, label='Dec. 21, $\gamma$=46')
ax2.plot(X, scaled_power_std[rn.DayOfTheYear('6/21')-1], color=color, linestyle='dashed', linewidth=3, label='Jun. 21, $\gamma$=46')
ax2.plot(X, scaled_power_gamma0[rn.DayOfTheYear('6/21')-1], color=color, linestyle='dotted', linewidth=3, label='Jun. 21, $\gamma$=46')
ax2.set_ylabel('Power [kW]', color=color, fontsize=18)
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim((0,250))
ax2.legend(loc='upper right')

plt.tick_params(axis = 'x')
plt.title('Irradiance and Power vs Time', fontsize=20)
plt.xlim(0,24)

f1.tight_layout()
f1.show()