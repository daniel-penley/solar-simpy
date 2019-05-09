# solar-simpy

This repository contains four main Python codes. renew.py, power.py, and CloudOpacity.py are all used as imported libraries in the main file, main.py. It also contains a CONFIG.txt file, which allows the user to alter the date, location, and factors regarding the solar panels and their position and location.

renew.py defines a number of functions that establish the renewable energy parameters based on inputs such as latitude, longtitude, and time. 

power.py calculates the yearly solar power generated, based on the renewable energy parameters from renew.py.

CloudOpacity.py creates a CloudModel object, which uses SimPy to simulate clouds entering and leaving the sky, which affects the power generated. The output of CloudOpacity.py is the number of clouds currently in the sky, which power.py incorporates as a variable when calculating the yearly power generated.

The .csv files are the real-world power data for the Palmer Events Center for selected dates. Data for dates not provided can be found and downloaded here: http://egauge8794.egaug.es/

main.py pulls in the desired variables from the CONFIG.txt file and imports renew.py, power.py, and CloudOpacity.py. Running this code produces a graph of the solar power for a modeled clear day, a modeled cloudy day, and the real-world power data for the Palmer events Center.
