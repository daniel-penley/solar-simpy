#Renewable Energy Technology
#Pwer Function

import math as m
import numpy as np
import renew as rn

def YearlyPower(lat, long_std, long_loc, beta, gamma, area_panel, n_panels, eff):
	#Figure 1: Irradiance for Austin and Total System Power Delivery vs Time of Day, Sunny Day, Dec. 21
	irradiance = []
	power = []
	for N in range(1,366):
		# print('day:', N)
		I_0 = rn.I_0(N)
		delta = rn.Declination(N)
		irradiance.append([])
		power.append([])
		for time in range(0,24*12+1):
			solar_time = rn.LocalToSolarTime(time/12, long_std, long_loc, N)
			# print('solar time:', solar_time)
			omega = rn.HourAngle(solar_time)
			# print('hour angle:', omega)
			theta_z = rn.ZenithAngle(delta, lat, omega)
			# print('zenith angle:', theta_z)
			alpha = rn.Altitude(delta, lat, omega)

			gamma_s = rn.SolarAzimuth(delta, omega, alpha)
			if N >= 90 and N <= 266 and N != 1 and gamma_s < gamma_s_old:
				if gamma_s <= 0:
					gamma_s_mod = -180 - gamma_s
				elif gamma_s > 0:
					gamma_s_mod = 180 - gamma_s
			else:
				gamma_s_mod = gamma_s

			# print('gamma_s:', gamma_s)
			# print('gamma_s:', gamma_s_mod)

			theta_i = rn.AngleOfIncidence(alpha, beta, gamma, gamma_s)
			# print('angle of incidence:', theta_i)

			if theta_z > 90:
				tau_b = 0
			else:
				tau_b = rn.BeamTransmissivity(theta_z, N)
			# print('beam transmissivity:', tau_b)
			tau_d = rn.DiffuseTransmissivity(tau_b)
			# print('tau_d:', tau_d)

			if theta_i > 90:
				I_c_b = 0
			else:
				I_c_b = rn.I_c_b(I_0, tau_b, theta_i)
			# print('I_c_b:', I_c_b)	
			I_c_d = 0	
			I_c_d = rn.I_c_d(tau_d, I_0, theta_z, beta)
			# print('I_c_d:', I_c_d)

			if alpha < 0:
				irradiance[N-1].append(0)
			else:
				irradiance[N-1].append(I_c_b + I_c_d)
			power[N-1].append(irradiance[N-1][time]*eff*area_panel*n_panels)

			gamma_s_old = gamma_s
		# print(irradiance[N-1])
	return irradiance, power