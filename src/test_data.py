from random import uniform
import os

def generate_data(n, file_path, max_voltage, max_temp, max_current):
    if file_path[-4:] != ".csv":
        file_path += ".csv"

    if os.path.exists(file_path):
        os.remove(file_path)

    file = open(file_path, "a")
    voltage = 0.98 * max_voltage
    temp = 0.65 * max_temp
    current = (voltage / max_voltage) * max_current

    for i in range(n):
        v_noise, t_noise, c_noise = uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)

        line = ",".join(str(val) for val in [voltage + v_noise, temp + t_noise, current + c_noise])

        file.write(line + '\n')

def main():
   generate_data(100000, "../test", 300.0, 100.0, 20.0)

if __name__ == "__main__":
    main()