import math as m

def TimeMinutesToDecimal(time):
	"""
	This function converts time from the hours.minutes.seconds format to hours.decimal_minutes
	Input time as a string formatted 'hour.minute.second'
	"""
	time = time.split('.')
	time = [int(x) for x in time]
	return time[0] + time[1]/60 + time[2]/3600
	
def TimeDecimalToMinutes(x):
	"""
	This function converts time from the hours.decimal_minutes format to hours:minutes:seconds.decimal_milliseconds
	"""
	x = float(x)
	decimal_minutes1, hours = m.modf(x)
	hours = int(hours)
	decimal_minutes2 = decimal_minutes1*60
	decimal_seconds, minutes = m.modf(decimal_minutes2)
	minutes = int(minutes)
	seconds = round(decimal_seconds*60, 2)
	return str(hours) + ':' + str(minutes) + ':' + str(seconds)

def LatLong(coord):
	"""
	This function converts Latitude and Longitude from a deg.minute.second format to a decimal degree format
	Input is is a string formatted 'deg.minutes.seconds' 
	"""	
	coord = coord.split('.')
	coord = [int(x) for x in coord]
	return coord[0] + coord[1]/60 + coord[2]/3600

def DayOfTheYear(date):
	"""
	This function return the day of the year
	Input is a string formatted 'mm/dd' 
	Leap years are not taken into account
	"""
	date = date.split('/')
	date = [int(x) for x in date]
	days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	return sum(days_in_months[0:date[0]-1]) + date[1]

def I_0(N):
	"""
	This function calculate the daily solar constant as a function of the the day of the year
	N=1 on January 1st
	This function does not take leap years into account
	"""
	return 1368*(1+0.034*m.cos(2*m.pi*(N-3)/365))

def AM(theta_z):
	"""
	This function calculates Air Mass # as a function of theta_z
	theta_z is in degrees
	"""
	theta_z_rad = theta_z/360*2*m.pi
	return 1/(m.cos(theta_z_rad)+0.50572*(96.07995-theta_z)**(-1.3636))

def LocalToSolarTime(std_time, long_std, long_loc, N):
	"""
	This function finds solar time (decimal) when local time, standard longitude, local longitude, and day of the year are inputted
	input standard time as a hours.decimal_minutes
	input longitude in decimal degrees
	input day of the year as a number 
	"""

	#step 1: calculate tau for the day of the year
	tau = 2*m.pi*N/365

	#step 2: calculate ET
	#eq 9.9 coefficients
	a = [-7.3412, -9.3795, -0.3179, -0.1739]
	b = [0.4944, -3.2568, -0.0774, -0.1283]

	ET = []
	for j in range(4):
		ET.append(a[j]*m.sin((j+1)*tau) + b[j]*m.cos((j+1)*tau))
	ET_tot_decimal = sum(ET)/60

	solar_time_decimal = std_time + 4/60*(long_std - long_loc) + ET_tot_decimal
	return solar_time_decimal

def SolarToLocalTime(solar_time, long_std, long_loc, N):
	"""
	This function finds local time (decimal) when solar time, standard longitude, local longitude, and day of the year are inputted
	input solar time as a string formatted 'hours.minutes.seconds'
	input longitude as a string formatted 'degrees.minutes.seconds'
	input day of the year as a number
	"""

	#step 1: calculate tau for the day of the year
	tau = 2*m.pi*N/365

	#step 2: calculate ET
	#eq 9.9 coefficients
	a = [-7.3412, -9.3795, -0.3179, -0.1739]
	b = [0.4944, -3.2568, -0.0774, -0.1283]

	ET = []
	for j in range(4):
		ET.append(a[j]*m.sin((j+1)*tau) + b[j]*m.cos((j+1)*tau))
	ET_tot_decimal = sum(ET)/60

	local_time_decimal = TimeMinutesToDecimal(solar_time) - 4/60*(LatLong(long_std) - LatLong(long_loc)) - ET_tot_decimal
	return local_time_decimal

def Declination(N):
	"""
	This function finds declination (delta) in degrees when the day of the year is inputted
	N=1 on January 1st
	"""
	return 23.45*m.sin(m.radians(360*(284+N)/365))

def AltitudeMax(lat, delta):
	"""
	This function finds altitude at solar noon (alpha_max) in degrees when the day of the year is inputted
	input latitude as a string of the form 'degrees.minutes.seconds'
	"""
	return 90 - LatLong(lat) + delta

def HourAngle(solar_time):
	"""
	This function finds the hour angle (omega) in degrees when the solar time is supplied
	Input solar time in decimal minutes
	"""
	return solar_time*15 - 180

def ZenithAngle(delta, lat, omega):
	"""
	This function finds the zenith angle (theta_z) in degrees when the declination (delta), latitude, and hour angle (omega) are supplied
	Input delta in degrees
	Input latitude in decimal degrees
	Input omega in degrees
	"""	
	delta_radians = m.radians(delta)
	lat_radians = m.radians(lat)
	omega_radians = m.radians(omega)
	theta_z_radians = m.acos(m.sin(delta_radians)*m.sin(lat_radians) + m.cos(delta_radians)*m.cos(lat_radians)*m.cos(omega_radians))
	return theta_z_radians/2/m.pi*360

def Altitude(delta, lat, omega):
	"""
	This function finds the altitude (alpha) in degrees when the declination (delta), latitude, and hour angle (omega) are supplied
	Input delta in degrees
	Input latitude in decimal degrees
	Input omega in degrees
	"""	
	delta_radians = m.radians(delta)
	lat_radians = m.radians(lat)
	omega_radians = m.radians(omega)
	alpha_radians = m.asin(m.sin(delta_radians)*m.sin(lat_radians) + m.cos(delta_radians)*m.cos(lat_radians)*m.cos(omega_radians))
	return alpha_radians/2/m.pi*360

def SolarAzimuth(delta, omega, alpha):
	"""
	This function finds the solar azimuth (gamma_s) in degrees when the declination (delta), hour angle(omega), and altitude (alpha) are supplied
	Input delta in degrees
	Input omega in degrees
	Input alpha in degrees
	"""	
	delta_radians = m.radians(delta)
	omega_radians = m.radians(omega)
	alpha_radians = m.radians(alpha)
	gamma_s_radians = m.asin(m.cos(delta_radians)*m.sin(omega_radians)/m.cos(alpha_radians))
	return gamma_s_radians/2/m.pi*360

def AngleOfIncidence(alpha, beta, gamma, gamma_s):
	"""
	This function finds the angle of incidencee (theta_i) in degrees when the altitude (alpha), tilt angle (beta), azimuth (gamma), and solar azimuth (gamma_s) are supplied
	Input alpha in degrees
	Input beta in degrees (for a horizontal surface, beta = 0)
	Input gamma in degrees (for a south facing surface, gamma = 0)
	Input gamma_s in degrees
	"""	
	alpha_radians = m.radians(alpha)
	beta_radians = m.radians(beta)
	gamma_radians = m.radians(gamma)
	gamma_s_radians = m.radians(gamma_s)
	theta_i_radians =  m.acos(m.sin(alpha_radians)*m.cos(beta_radians) + m.cos(alpha_radians)*m.sin(beta_radians)*m.cos(gamma_radians - gamma_s_radians))
	return theta_i_radians/2/m.pi*360

def I_Beta_b(I_n_b, theta_i):
	"""
	This function finds the hourly beam radiation normal to a tilted surface when the hourly beam radiation normal to the ground (I_n_b) and the angle of incidence (theta_i) is supplied
	Input theta_i in degrees
	"""		
	theta_i_radians = m.radians(theta_i)
	return I_n_b*m.cos(theta_i_radians)/2/m.pi*360

def BeamTransmissivity(theta_z, N, A=0.149):
	"""
	This function finds the beam transmissivity, tau_b
	Input theta_z in degrees
	N is the day of the year
	A is the altitude in km (defualts to 0.149 for Austin, TX)
	The 23km haze model is used (for mid-latitude)
	"""

	#Haze Model	
	if N == 172: #June 21st, middle of summer --- N = 172
		r_0 = 0.97
		r_1 = 0.99
		r_k = 1.02
	elif N == 355: #December 21st, middle of winter --- N = 355
		r_0 = 1.03
		r_1 = 1.01
		r_k = 1.00
	elif N >= 1 and N < 172:
		r_0 = (0.97-1.03)/(172+10)*N + 1.0267
		r_1 = (0.99-1.01)/(172+10)*N + 1.0089
		r_k = (1.02-1.00)/(172+10)*N + 1.001099
	elif N > 172 and N < 355:
		r_0 = (1.03-0.97)/(355-172)*N + 0.91361
		r_1 = (1.01-0.99)/(355-172)*N + 0.9712
		r_k = (1.00-1.02)/(355-172)*N + 1.0388
	elif N > 355 and N <= 365:
		r_0 = (0.97-1.03)/(536-355)*N + 1.14768
		r_1 = (0.99-1.01)/(536-355)*N + 1.04923
		r_k = (1.02-1.00)/(536-355)*N + 0.98077

	a_0_star = 0.4237 - 0.008216*(6-A)**2
	a_1_star = 0.5055 + 0.00595*(6.5-A)**2
	k_star = 0.2711 + 0.01858*(2.5-A)**2

	a_0 = r_0*a_0_star
	a_1 = r_1*a_1_star
	k = r_k*k_star

	theta_z_radians = m.radians(theta_z)

	return a_0 + a_1*m.e**(-k/m.cos(theta_z_radians))

def I_c_b(I_0, tau_b, theta_i):
	"""
	This function finds the clear-day beam Insolation in W/m^2
	Input theta_i in degrees
	This works for flat and tilted panels (beta > 0)
	"""
	theta_i_radians = m.radians(theta_i)
	return I_0*tau_b*m.cos(theta_i_radians)

def DiffuseTransmissivity(tau_b):
	"""
	This function finds the diffuse transmissivity, tau_d
	"""
	return 0.271 - 0.294*tau_b

def I_c_d(tau_d, I_0, theta_z, beta):
	"""
	This function find the clear-day diffuse insolation in W/m^2
	Input theta_z in degrees
	Input beta as radians
	"""
	theta_z_radians = m.radians(theta_z)
	beta_radians = m.radians(beta)
	return tau_d*I_0*m.cos(theta_z_radians)*(1+m.cos(beta_radians))/2