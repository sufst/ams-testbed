from random import gauss
from random import random
import os

def generate_data(n, file_path, max_voltage, max_temp, max_current):
    if file_path[-4:] != ".csv":
        file_path += ".csv"

    if os.path.exists(file_path):
        os.remove(file_path)

    file = open(file_path, "a")
    file.write("Time,Voltage,Temperature,Current\n")

    for i in range(n):
        perc = (1000 - abs((i % 2000) - 1000)) / 1000
        voltage, temp, current = perc * max_voltage, perc * max_temp, perc * max_current
        v_noise, t_noise, c_noise = gauss(0, 5), gauss(0, 2), gauss(0, 0.5)

        line = ",".join(str(val) for val in [i, max(random(), voltage + v_noise), max(random(), temp + t_noise), max(random(), current + c_noise)])

        file.write(line + '\n')

def main():
   generate_data(100000, "../test", 300.0, 100.0, 20.0)

if __name__ == "__main__":
    main()