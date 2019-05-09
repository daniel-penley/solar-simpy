import math as m
import numpy as np
import renew as rn
import CloudOpacity as co

def YearlyPower(lat, long_std, long_loc, beta, gamma, area_panel, n_panels, eff, inv_eff):
    
    clear_irradiance = []
    clear_power = []
    irradiance = []
    power = []
    for N in range(1,366):
        I_0 = rn.I_0(N)
        delta = rn.Declination(N)
        clear_irradiance.append([])
        clear_power.append([])
        irradiance.append([])
        power.append([])
        OCI = co.cloudOpacity()
        for time in range(0,24*12+1):
            oci = OCI[time]
            solar_time = rn.LocalToSolarTime(time/12, long_std, long_loc, N)
            omega = rn.HourAngle(solar_time)
            theta_z = rn.ZenithAngle(delta, lat, omega)
            alpha = rn.Altitude(delta, lat, omega)

            gamma_s = rn.SolarAzimuth(delta, omega, alpha)
            if N >= 90 and N <= 266 and N != 1 and gamma_s < gamma_s_old:
                if gamma_s <= 0:
                    gamma_s_mod = -180 - gamma_s
                elif gamma_s > 0:
                    gamma_s_mod = 180 - gamma_s
            else:
                gamma_s_mod = gamma_s

            theta_i = rn.AngleOfIncidence(alpha, beta, gamma, gamma_s)

            if theta_z > 90:
                tau_c_b = 0
                tau_b = 0
            else:
                tau_c_b = rn.ClearBeamTransmissivity(theta_z, N)
                tau_b = rn.BeamTransmissivity(tau_c_b, oci)
            tau_c_d = rn.DiffuseTransmissivity(tau_c_b)
            tau_d = rn.DiffuseTransmissivity(tau_b)

            if theta_i > 90:
                I_c_b = 0
                I_b = 0
            else:
                I_c_b = rn.I_b(I_0, tau_c_b, theta_i)
                I_b = rn.I_b(I_0, tau_b, theta_i)
                
            I_c_d = rn.I_d(tau_c_d, I_0, theta_z, beta)
            I_d = rn.I_d(tau_d, I_0, theta_z, beta)

            if alpha < 0:
                clear_irradiance[N-1].append(0)
                irradiance[N-1].append(0)
            else:
                clear_irradiance[N-1].append(I_c_b + I_c_d)
                irradiance[N-1].append(I_b + I_d)
            clear_power[N-1].append(clear_irradiance[N-1][time]*eff*area_panel*n_panels*inv_eff)
            power[N-1].append(irradiance[N-1][time]*eff*area_panel*n_panels*inv_eff)

            gamma_s_old = gamma_s
            
    return clear_irradiance, clear_power, irradiance, power
