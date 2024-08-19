#!/usr/bin/python3

import matplotlib.pyplot as plt
import argparse
import os
import json
from pathlib import Path
import yaml


# TODO Maybe create a moving dictionary holding all the parameters from handle_plotting
# onwards for readabbility, unsure


# create_plots is what is called automatically from within the general test script
def create_plots(data_dictionary, parameters, output_directory, plot_details={}):
    # Make a running array of context_strs throughout the program to allow adding to
    # it from anywhere
    context_strs = []
    context_strs.append(start_context_str(parameters))
    os.makedirs(output_directory, exist_ok=True)

    # A lot of this code is similar to test_general as the share much of the same logic,
    # maybe make a shared header file but unsure of the slight differences
    fixed_values = {}
    for i in parameters["core"]["fixed_variables"]:
        fixed_values[i] = parameters["program_specific"][i][0]
    fixed_values[parameters["core"]["plot_variables"]["x_axis"][0]] = parameters[
        "program_specific"
    ][parameters["core"]["plot_variables"]["x_axis"][0]]

    handle_plotting(
        data_dictionary,
        parameters,
        fixed_values,
        "separate_plots",
        0,
        plot_details,
        output_directory=output_directory,
        context_strs=context_strs,
    )

    # Save context string in output directory
    context_str = "".join(context_strs)
    with open(f"{output_directory}/context.md", "w") as file:
        file.write(context_str)


# TODO cannot decide on the inclusion of decide_separates, looks a bit cleaner, but
# seems wrong to have string deciders of whether you're in the "for" or "else" sections
def handle_plotting(
    curr_data_dictionary,
    parameters,
    fixed_parameters,
    plots_or_legend,
    current_iter,
    plot_details,
    context_strs=None,
    output_directory=None,
    label=None,
    ax=None,
):
    core = parameters["core"]
    program_specific = parameters["program_specific"]
    # If there are no separate plot variables, just run the function,
    #    otherwise set the variable for single_run_params to the variable
    # This is essentially a recursive for loop, but needed as we don't know how many
    # variables there will be, i.e., how deep a for loop
    if current_iter < len(core["plot_variables"][plots_or_legend]):
        current_parameter = core["plot_variables"][plots_or_legend][
            current_iter
        ]  # The current plots/legend parameter we are looking at
        if current_parameter != " ":
            current_parameter_values = program_specific[
                current_parameter
            ]  # The passed values in parameters for this current parameter

            data_dictionary_parameter = curr_data_dictionary[
                current_parameter
            ]  # The dictionary for that parameter in the data_dictionary

            for var in current_parameter_values:
                if check_limits(plot_details, var, current_parameter):
                    data_dictionary_var = data_dictionary_parameter[var]
                    fixed_parameters[current_parameter] = var
                    decide_separates(
                        "for",
                        plots_or_legend,
                        data_dictionary_var,
                        parameters,
                        fixed_parameters,
                        current_iter,
                        plot_details,
                        context_strs,
                        output_directory,
                        ax,
                        label,
                        current_parameter,
                        var,
                    )
                    # if plots_or_legend == "separate_plots":
                    #     separate_plots_within_for(data_dictionary_var, parameters,
                    #       fixed_parameters, current_iter, plot_details, context_strs,
                    #           output_directory)
                    # else:
                    #     legend_within_for(data_dictionary_var, parameters,
                    #       fixed_parameters, current_iter, plot_details, ax,
                    #           label, current_parameter, var)
        else:
            decide_separates(
                "else",
                plots_or_legend,
                curr_data_dictionary,
                parameters,
                fixed_parameters,
                current_iter,
                plot_details,
                context_strs,
                output_directory,
                ax,
                label,
            )
            # if plots_or_legend == "separate_plots":
            #     separate_plots_else(curr_data_dictionary, parameters,
            #       fixed_parameters, plot_details, context_strs, output_directory)
            # else:
            #     legend_else(curr_data_dictionary, parameters, plot_details, ax, label)


def decide_separates(
    decider,
    plots_or_legend,
    curr_data_dictionary,
    parameters,
    fixed_parameters,
    current_iter,
    plot_details,
    context_strs,
    output_directory,
    ax,
    label,
    current_parameter=None,
    var=None,
):
    if decider == "for":
        if plots_or_legend == "separate_plots":
            separate_plots_within_for(
                curr_data_dictionary,
                parameters,
                fixed_parameters,
                current_iter,
                plot_details,
                context_strs,
                output_directory,
            )
        else:
            legend_within_for(
                curr_data_dictionary,
                parameters,
                fixed_parameters,
                current_iter,
                plot_details,
                ax,
                label,
                current_parameter,
                var,
            )
    else:
        if plots_or_legend == "separate_plots":
            separate_plots_else(
                curr_data_dictionary,
                parameters,
                fixed_parameters,
                plot_details,
                context_strs,
                output_directory,
            )
        else:
            legend_else(curr_data_dictionary, parameters, plot_details, ax, label)


def separate_plots_within_for(
    curr_data_dictionary,
    parameters,
    fixed_parameters,
    current_iter,
    plot_details,
    context_strs,
    output_directory,
):
    handle_plotting(
        curr_data_dictionary,
        parameters,
        fixed_parameters,
        "separate_plots",
        current_iter + 1,
        plot_details,
        context_strs=context_strs,
        output_directory=output_directory,
    )


def legend_within_for(
    curr_data_dictionary,
    parameters,
    fixed_parameters,
    current_iter,
    plot_details,
    ax,
    label,
    current_parameter,
    var,
):
    new_label = f"{label}{current_parameter}_{var} "
    # TODO need to think about how to do multiple parameters on a legend
    handle_plotting(
        curr_data_dictionary,
        parameters,
        fixed_parameters,
        "legend",
        current_iter + 1,
        plot_details,
        ax=ax,
        label=new_label,
    )


def separate_plots_else(
    curr_data_dictionary,
    parameters,
    fixed_parameters,
    plot_details,
    context_strs,
    output_directory,
):
    # Handle a single plot, so go through all the legend variables
    # Looks like it is doing nothing but resets the plot every time, otherwise get
    #   one big plot with all the data
    plt.figure()
    ax = plt.subplot(111)
    label = ""
    handle_plotting(
        curr_data_dictionary,
        parameters,
        fixed_parameters,
        "legend",
        0,
        plot_details,
        ax=ax,
        label=label,
    )

    plot_name = "PLOT"
    separate_plots = parameters["core"]["plot_variables"]["separate_plots"]
    for i in separate_plots:
        plot_name = f"{plot_name}_{i}-{fixed_parameters[i]}"

    if len(separate_plots) == 0:
        plot_directory = f"{output_directory}/{plot_name}"
    else:
        # Remove the starting "PLOT_" from the directory name
        plot_directory = f"{output_directory}/{plot_name[5:]}"

    os.makedirs(plot_directory, exist_ok=True)

    plot_image_path = f"{plot_directory}/{plot_name}.svg"
    configurePlot(ax, parameters)
    plt.savefig(plot_image_path)

    with open(f"{plot_directory}/specific_parameters.json", "w") as outfile:
        json.dump(fixed_parameters, outfile, indent=4)

    context_to_plot_path = f"../{os.path.relpath(plot_image_path, output_directory)}"
    add_plot_context_str(
        context_strs, parameters, fixed_parameters, context_to_plot_path
    )


def check_limits(plot_details, var, parameter):
    if plot_details != {}:
        limits = plot_details["limits"]
        if parameter in limits:
            if var < limits[parameter]["lower"] or var > limits[parameter]["upper"]:
                return False
    return True


def legend_else(curr_data_dictionary, parameters, plot_details, ax, label):
    x_vals = {}
    x_axis = parameters["core"]["plot_variables"]["x_axis"]

    for i in curr_data_dictionary[x_axis[0]].items():
        if check_limits(plot_details, i[0], x_axis[0]):
            x_vals[i[0]] = i[1]

    ax.plot(*zip(*sorted(x_vals.items())), label=f"{label}")  # color = ...)


def configurePlot(ax, parameters):
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    plot_variables = parameters["core"]["plot_variables"]

    x_parameter = plot_variables["x_axis"][0]
    x_title = x_parameter
    ax.set_xlabel(f"{x_title}")
    ax.set_ylabel("Time (s)")

    legends_title = ""
    for i in plot_variables["legend"]:
        legends_title = f"{legends_title}{i}, "
    if len(legends_title) > 2:
        legends_title = legends_title[:-2]  # Remove the final ", "

    title = f"How {x_parameter} affects overall time when \nchanging {legends_title}"
    ax.set_title(title)


def start_context_str(parameters):
    core = parameters["core"]
    test_name = core["test_name"][0]
    output = (
        f"# Context and plot for test: {test_name}\n\n"
        "The following variables were fixed for the entire test:\n\n"
    )

    for i in core["fixed_variables"]:
        val = parameters["program_specific"][i][0]
        output = f"{output}{i}: {val}\n"

    output = f"{output}\n\n"

    return output


def add_plot_context_str(context_strs, parameters, fixed_parameters, plot_path):

    this_str = "The following plot is for: "
    for i in parameters["core"]["plot_variables"]["separate_plots"]:
        this_str = f"{this_str}{i} {fixed_parameters[i]}, "
    this_str = this_str[:-2]  # Remove final ", "
    # Add plot TODO need to check this link will work, plot_path may also be incorrect
    this_str = f"{this_str}\n\n![image]({plot_path})\n\n"
    context_strs.append(this_str)


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--test_data_json",
        type=str,
        required=True,
        help="file storing the test data, a dictionary json.",
    )
    parser.add_argument(
        "--test_parameters_json",
        type=str,
        required=True,
        help="file storing the test parameters, a dictionary json.",
    )
    parser.add_argument(
        "--save_directory", type=str, default=".", help="location to save outputs."
    )
    parser.add_argument(
        "--plot_config",
        type=str,
        help="config file containing  some plot details, limits etc.",
    )  # Just limits for now but structure is there for further expansion
    args = parser.parse_args()

    if args.plot_config is not None:
        conf = parse_yaml_file(args.plot_config)
    else:
        conf = {}

    # Parse the json file into a python dictionary

    # The data dictionary has integer (and maybe float) keys, when saving to json these
    # are automatically changed into strings, so need to fix this
    # Temporary fix, need to think about restructuring
    def maybe_int_or_float(key):
        """Converts strings that represent valid ints to int, then tries to floats,
        then leaving other strings unchanged"""
        try:
            return int(key)
        except ValueError:
            try:
                return float(key)
            except ValueError:
                return key

    def key_to_int_or_float(obj):
        """Replaces all string keys representing valid ints/floats with ints/floats"""
        return {maybe_int_or_float(k): v for k, v in obj.items()}

    with open(args.test_data_json) as json_file:
        json_dict = json.load(json_file, object_hook=key_to_int_or_float)

    with open(args.test_parameters_json) as json_file:
        parameter_dict = json.load(json_file)

    create_plots(json_dict, parameter_dict, args.save_directory, plot_details=conf)
