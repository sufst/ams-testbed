from random import gauss
from random import random
import os
import yaml
import re

"""
    Data generation script,
    Write configuration and run script to generate data.
   
    Configuration is in YAML with the following structure:
    --------------------------------
    data-path: (path)
    entries: (number of entries, integer)
   
    voltage/current/temperature:
        maximum: (maximum reading)
        noise-distribution:
            standard-deviation: (deviation for noise)
            mean: (mean for noise)
    --------------------------------
"""


def generate_csv(file_path, n, voltage_max, voltage_noise, current_max, current_noise, temp_max, temp_noise):
    file = open(file_path, "a")
    file.write("Time (ms),Voltage (V) ,Current (A),Temperature (C)\n")

    for i in range(n):
        perc = (1000 - abs((i % 2000) - 1000)) / 1000
        voltage, current, temp = perc * voltage_max, perc * current_max, perc * temp_max
        v_noise, c_noise, t_noise = gauss(**voltage_noise), gauss(**current_noise), gauss(**temp_noise)

        line = ",".join(str(val) for val in [i, max(random(), voltage + v_noise), max(random(), current + c_noise),
                                             max(random(), temp + t_noise)])

        file.write(line + '\n')


def generate_data(file_path):
    expected_format_message = ("\033[91mExpected values:\n" + "-" * 50 +
                               "\ndata-path: (path)\nnumber-of-entries: (number of entries, integer)" +
                               "\n\nvoltage:\n\tmaximum: (maximum reading)" +
                               "\n\tnoise-distribution:\n\t\tstandard-deviation: (deviation for noise)" +
                               "\n\t\tmean: (mean for noise)" +
                               "\n\ncurrent:\n\tmaximum: (maximum reading)" +
                               "\n\tnoise-distribution:\n\t\tstandard-deviation: (deviation for noise)" +
                               "\n\t\tmean: (mean for noise)" +
                               "\n\ntemperature:\n\tmaximum: (maximum reading)" +
                               "\n\tnoise-distribution:\n\t\tstandard-deviation: (deviation for noise)" +
                               "\n\t\tmean: (mean for noise)\n" + "-" * 50)

    with open(file_path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

        try:
            config['data-path'] = re.sub('(\.[a-zA-Z0-9]*)*$', '.csv', config['data-path'], count=1)
            if os.path.exists(config['data-path']):
                os.remove(config['data-path'])

            noise = {}
            for i in ('voltage', 'current', 'temperature'):
                noise[i] = {'sigma': float(config[i]['noise-distribution']['standard-deviation']),
                            'mu': float(config[i]['noise-distribution']['mean'])}

            generate_csv(config['data-path'], int(config['number-of-entries']),
                         float(config['voltage']['maximum']), noise['voltage'],
                         float(config['current']['maximum']), noise['current'],
                         float(config['temperature']['maximum']), noise['temperature'])

            print("\033[32mSuccessfully generated data at " + config['data-path'])
        except KeyError as e:
            print("\033[91mInvalid configuration, missing " + e.args[0] + "\n")
            print(expected_format_message)
        except ValueError as e:
            print("\033[91mInvalid configuration, wrong types\n" + e.args[0] + "\n")
            print(expected_format_message)


def main():
    generate_data('config.yml')
    # generate_data(100000, "../test", 300.0, 100.0, 20.0)


if __name__ == "__main__":
    main()