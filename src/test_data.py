import os
import re
from random import gauss, random
from sys import argv, exit

import yaml
from yaml.scanner import ScannerError

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

usage_message = "usage: test_data.py <configuration file>"
generic_script_message = "This script will generate data from a given yml configuration file"
expected_format_message = ("Expected values in configuration file:\n" + "-" * 50 +
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


# Takes parsed values and generates file
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


# Takes config to generate data file using generate_csv
def generate_data(file_path):
    # Parse configuration file
    with open(file_path) as file:
        try:
            config = yaml.load(file, Loader=yaml.FullLoader)
        except ScannerError as e:
            print("\033[91mInvalid configuration, is not valid yaml: ", end='')
            print(e)
            quit(1)

        if not isinstance(config, dict):
            printError("Invalid configuration, is not valid yaml\nConfiguration should be in following format")

        try:
            # Check file path and if file exists
            config['data-path'] = re.sub('(\.[a-zA-Z0-9]*)*$', '.csv', config['data-path'], count=1)
            if os.path.exists(config['data-path']):
                os.remove(config['data-path'])
                print("Clearing existing data...")

            # Parse noise, KeyError will be thrown if missing in config
            noise = {}
            for i in ('voltage', 'current', 'temperature'):
                noise[i] = {'sigma': float(config[i]['noise-distribution']['standard-deviation']),
                            'mu': float(config[i]['noise-distribution']['mean'])}

            # Call generate_csv to actually generate data, KeyError or ValueError will be thrown if issue in config
            generate_csv(config['data-path'], int(config['number-of-entries']),
                         float(config['voltage']['maximum']), noise['voltage'],
                         float(config['current']['maximum']), noise['current'],
                         float(config['temperature']['maximum']), noise['temperature'])

            print("\033[32mSuccessfully generated data at " + config['data-path'])
        except KeyError as e:
            # Parsing error: missing value in yml file
            printError("\033[91mInvalid configuration, missing " + e.args[0], print_usage=False)
        except ValueError as e:
            # Parsing error: value has the wrong type in yml file
            printError("\033[91mInvalid configuration, wrong types\n" + e.args[0], print_usage=False)


# Printing errors (used for usage and most parse errors)
def printError(message=generic_script_message, print_usage=True, print_expected=True, exit_code=1):
    if exit_code == 1:
        print("\033[91m", end='')

    if print_usage:
        print(usage_message + "\n")

    print(message)

    if print_expected:
        print("\n\n" + expected_format_message)

    exit(exit_code)


def main(*args):
    try:
        if args[1] == '-h' or args[1] == '--help':
            printError(exit_code=0)

        split_path = args[1].split(".", 1)
        if len(split_path) < 2 or split_path[1] != 'yml':
            printError("Not a yaml file, configuration file should end in .yml")

        generate_data(args[1])
    except IndexError:
        printError(exit_code=0)
    except FileNotFoundError:
        printError("Configuration file not found", print_usage=False, print_expected=False)


if __name__ == "__main__":
    main(*argv)
