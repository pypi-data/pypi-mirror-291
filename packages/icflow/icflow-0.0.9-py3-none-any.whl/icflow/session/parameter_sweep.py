#!/usr/bin/env python

import subprocess
import argparse
import os
import yaml
import datetime
from pathlib import Path
import sys
import json
import shutil

from .plot_general import create_plots


def get_absolute_path(path: str):
    dir = Path(path)
    if not dir.is_absolute():
        dir = os.getcwd() / dir
    return dir


def parse_yaml_file(path: str):
    config_path = get_absolute_path(path)

    stream = open(config_path, "r")
    conf = yaml.safe_load(stream)

    return conf


def reform_empty_or_single_keys(dictionary):
    for parameter_names in dictionary:
        # Read that isinstance(thing, dict) can behave unexpectedly
        # Hence use try except
        try:
            dictionary[parameter_names].items()
        except (AttributeError, TypeError):
            if (
                dictionary[parameter_names] is None
                or dictionary[parameter_names][0] is None
            ):
                dictionary[parameter_names] = [" "]
            if isinstance(dictionary[parameter_names], str):
                dictionary[parameter_names] = [dictionary[parameter_names]]
        else:  # no exception raised
            reform_empty_or_single_keys(dictionary[parameter_names])


def fill_params(params, conf):
    for param in conf:
        params[param] = conf[param]

    core = params["core"]
    program_specific = params["program_specific"]

    # Ensures the format for empty variables the rest of the script will recognise
    reform_empty_or_single_keys(params)

    not_fixed = []
    for plot_section in core["plot_variables"]:
        for param in core["plot_variables"][plot_section]:
            not_fixed.append(param)

    fixed = []
    for param in program_specific:
        if param not in not_fixed:
            fixed.append(param)

            if len(program_specific[param]) != 1:
                print(
                    f'ERROR: The variable "{param}" was detected as fixed, but'
                    "has 0 or multiple entries"
                )

                sys.exit(1)

    core["fixed_variables"] = fixed

    if not core["test_name"]:
        core["test_name"] = datetime.datetime.now().strftime("%Y-%m-%d_%T")


def run_tests(single_run_params, params, plots_or_legend, current_iter, dir, data_dict):
    core = params["core"]
    program_specific = params["program_specific"]
    # If there are no separate plot variables, just run the function,
    #    otherwise set the variable for single_run_params to the variable
    # This is essentially a recursive for loop, but needed as we don't know how many
    # variables there will be, i.e., how many steps the for loop will be
    if current_iter < len(core["plot_variables"][plots_or_legend]):
        current_parameter = core["plot_variables"][plots_or_legend][current_iter]
        data_dict[current_parameter] = {}
        current_parameter_values = program_specific[current_parameter]
        for var in current_parameter_values:
            data_dict[current_parameter][var] = {}
            var_dir = f"{dir}/{current_parameter}_{var}"
            single_run_params[current_parameter] = var
            run_tests(
                single_run_params,
                params,
                plots_or_legend,
                current_iter + 1,
                var_dir,
                data_dict[current_parameter][var],
            )

    elif plots_or_legend == "separate_plots" and core["plot_variables"]["legend"] != [
        " "
    ]:
        run_tests(single_run_params, params, "legend", 0, dir, data_dict)

    else:
        os.makedirs(dir, exist_ok=True)
        run_program(
            single_run_params,
            core["plot_variables"]["x_axis"][0],
            core["path_to_program"][0],
            dir,
            data_dict,
        )


def run_program(single_run_params, x_axis, program_path, dir, data_dict):
    output_file = f"{dir}/{x_axis}_"

    data_dict[x_axis] = {}
    time_dict = data_dict[x_axis]

    current_env = os.environ.copy()

    command = f"python3 {program_path} "

    for i in single_run_params:
        if i != x_axis:
            command = f"{command} --{i} {single_run_params[i]} "

    command = f"{command} --{x_axis} "
    for x in single_run_params[x_axis]:
        single_command = f"{command}{x}"
        single_output_file = f"{output_file}{x}"
        single_command = f"{single_command} > {single_output_file}"

        print(f"Command is: \n{single_command}\n")

        subprocess.run(single_command, shell=True, check=True, env=current_env)

        # TODO this section may change when we use non-arbitrary circuits, as the
        # output may differ and there should also be part checking the result is still
        # correct/in an expected range if possible unsure how to do this generally

        # This is NOT general, is using the specific output currently given by cProfile,
        #  need a better way to grab timings
        # Still a bit hacky but maybe pass line number and number of space separated
        # "words" across?

        filename = open(f"{single_output_file}", "r")
        line = filename.readline()
        while "seconds" not in line and line != "":
            line = filename.readline()
        if line == "":
            print("Reached end of file without finding time.")
            time_value = 0.0
        else:
            line = line.split()
            time_value = line[-2]
        time_dict[x] = float(time_value)


def run_sweep(config):
    if config is not None:
        conf = parse_yaml_file(config)
    else:
        print("ERROR: config file was parsed as None")
        sys.exit(1)

    params = {}
    fill_params(params, conf)
    core = params["core"]
    program_specific = params["program_specific"]

    # TODO add a specific output folder functionality
    # Create the whole test directory
    test_name = core["test_name"][0]
    directory = f"ScalingOutputs/{test_name}"
    os.makedirs(directory, exist_ok=True)

    # Resave the config file in the test directory as to keep a complete package and
    # params dictionary
    config_file_name = config.stem
    shutil.copyfile(config, f"{directory}/{config_file_name}.yaml")

    # Save the parameters as a json file, to save recreating the dictionary in
    # plot_general.py main
    with open(f"{directory}/parameters.json", "w") as outfile:
        json.dump(params, outfile, indent=4)

    # single_run_params will be filled as the program goes on, and will have a
    # unique set of values
    #   for each run of the program
    single_run_params = {}

    # All the params["fixed_variables"] variables will be the same for
    # single_run_params in all test runs, so set them up now
    for i in core["fixed_variables"]:
        single_run_params[i] = program_specific[i][0]

    x_axis_parameter = core["plot_variables"]["x_axis"][0]

    single_run_params[x_axis_parameter] = program_specific[x_axis_parameter]

    data_directory = f"{directory}/Data"
    data_dictionary = {}

    # Run and collect the data for the test runs
    run_tests(
        single_run_params, params, "separate_plots", 0, data_directory, data_dictionary
    )

    # This saves all timings into a huge dictionary, data_dictionary

    # Save the data dictionary into a json file to have more readily available
    with open(f"{data_directory}/data.json", "w") as outfile:
        json.dump(data_dictionary, outfile, indent=4)

    # TODO add a parameter here NOPLOT to disable this
    # Now pass this dictionary to the plotting function, from plot_general.py
    default_context_plots_directory = f"{directory}/ContextAndPlots"
    create_plots(data_dictionary, params, default_context_plots_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True, help="Path to config file")
    args = parser.parse_args()

    run_sweep(args.config)
