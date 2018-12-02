import networkx as nx
import numpy as np
import math
import os
import random

###########################################
# Change this variable to the path to
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "/home/justinwei/cs170/inputs"

###########################################
# Change this variable if you want
# your outputs to be put in a
# different folder
###########################################
path_to_outputs = "/home/justinwei/cs170/outputs"


def parse_input(folder_name):
    '''
        Parses an input and returns the corresponding graph and parameters

        Inputs:
            folder_name - a string representing the path to the input folder

        Outputs:
            (graph, num_buses, size_bus, constraints)
            graph - the graph as a NetworkX object
            num_buses - an integer representing the number of buses you can allocate to
            size_buses - an integer representing the number of students that can fit on a bus
            constraints - a list where each element is a list vertices which represents a single rowdy group
    '''
    graph = nx.read_gml(folder_name + "/graph.gml")
    parameters = open(folder_name + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []

    for line in parameters:
        line = line[1: -2]
        curr_constraint = [num.replace("'", "") for num in line.split(", ")]
        constraints.append(curr_constraint)

    return graph, num_buses, size_bus, constraints


def make_move(s0, s1, bus_array, bus_tracker, student_rowdy_dict):
    bus_s0 = -1
    bus_s1 = -1
    for i in range(len(bus_array)):
        if s0 in bus_array[i]:
            bus_s0 = i
        if s1 in bus_array[i]:
            bus_s1 = i
        if s0 >= 0 and s1 >= 0:
            break
    if bus_s0 == bus_s1:
        return (bus_array, bus_tracker)
    bus_array[bus_s0].remove(s0)
    bus_array[bus_s1].remove(s1)
    bus_array[bus_s1].add(s0)
    bus_array[bus_s0].add(s1)
    s0_rowdy = student_rowdy_dict[s0]
    s1_rowdy = student_rowdy_dict[s1]
    for item in s0_rowdy:
        update = bus_tracker[bus_s0][item]
        update.add(s0)
        bus_tracker[bus_s0][item] = update

        update2 = bus_tracker[bus_s1][item]
        update2.remove(s0)
        bus_tracker[bus_s1][item] = update2
    for item in s1_rowdy:
        update = bus_tracker[bus_s1][item]
        update.add(s1)
        bus_tracker[bus_s1][item] = update

        update2 = bus_tracker[bus_s0][item]
        update2.remove(s1)
        bus_tracker[bus_s0][item] = update2
    return (bus_array, bus_tracker)


def simulated_annealing(graph, students, bus_array, bus_tracker, student_rowdy_dict, constraints):
    length = len(students)
    T = 1.
    swappers = random.sample(range(len(students)), 2)
    s0 = swappers[0]
    s1 = swappers[1]
    n_best = count_score(graph, bus_array, bus_tracker, constraints)
    n = 0
    bus_array_update = bus_array
    bus_tracker_update = bus_tracker
    while T > 0.001:
        newmove = make_move(s0, s1, bus_array_update, bus_tracker_update, student_rowdy_dict)
        n = count_score(graph, newmove[0], newmove[1], constraints)
        delta = n - n_best
        if delta > 0:
            n_best = n
            bus_array_update = newmove[0]
            bus_tracker_update = newmove[1]
        elif math.exp(delta / T) > random.random():
            n_best = n
            bus_array_update = newmove[0]
            bus_tracker_update = newmove[1]
        T -= 0.001

    return bus_array_update


def contains_rowdy(bus, bus_tracker, constraints):
    rowdies = []
    for group in bus_tracker[bus].keys():
        if len(bus_tracker[bus][group]) < 1:
            rowdies.append(constraints[group])
    if len(rowdies) == 0:
        return (False, [])
    else:
        return (True, rowdies)


def count_score(graph, bus_array, bus_tracker, constraints):
    count = 0
    for busnum in range(len(bus_array)):
        bus = bus_array[busnum]
        result_rowdy = contains_rowdy(busnum, bus_tracker, constraints)
        if result_rowdy[0]:
            for i in result_rowdy[1]:
                for person in i:
                    if person in bus:
                        bus.remove(person)
        for i in range(len(bus)):
            j = i + 1
            while j < len(bus):
                count += graph.number_of_edges(bus[i], bus[j])
                j += 1
    return count


def solve(graph, num_buses, size_bus, constraints):
    students = list(graph.nodes)

    #     global dictionary of students to their rowdy groups
    student_rowdy_dict = {}
    for student in students:
        student_rowdy_dict[student] = []
        for i in range(len(constraints)):
            if student in constraints[i]:
                curr_key = student_rowdy_dict[student]
                student_rowdy_dict[student] = curr_key + [i]

    #     list of dictionaries for each bus
    bus_tracker = []
    for bus in range(num_buses):
        bus_tracker.append({})
        for group in range(len(constraints)):
            bus_tracker[bus][group] = constraints[group]

    #     random initial assignments// bus_array is a list of lists
    bus_array = []
    if size_bus == 0:
        return
    for i in range(num_buses):
        bus_array.append([])
    for i in range(len(students)):
        rand_bus = int(np.random.randint(low=0, high=num_buses, size=1))
        if len(bus_array[rand_bus]) < size_bus:
            bus_array[rand_bus].append(students[i])
            for rowdy_num in student_rowdy_dict[students[i]]:
                curr_list = bus_tracker[rand_bus][rowdy_num]
                curr_list.remove(students[i])
                bus_tracker[rand_bus][rowdy_num] = curr_list
            i += 1

    return simulated_annealing(graph, students, bus_array, bus_tracker, student_rowdy_dict, constraints)

    # TODO: Write this method as you like. We'd recommend changing the arguments here as well


#     pass

def main():
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''
    size_categories = ["small", "medium", "large"]
    if not os.path.isdir(path_to_outputs):
        os.mkdir(path_to_outputs)

    for size in size_categories:
        category_path = path_to_inputs + "/" + size
        output_category_path = path_to_outputs + "/" + size
        category_dir = os.fsencode(category_path)

        if not os.path.isdir(output_category_path):
            os.mkdir(output_category_path)

        for input_folder in os.listdir(category_dir):
            input_name = os.fsdecode(input_folder)
            graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
            solution = solve(graph, num_buses, size_bus, constraints)
            output_file = open(output_category_path + "/" + input_name + ".out", "w")

            # TODO: modify this to write your solution to your
            #      file properly as it might not be correct to
            #      just write the variable solution to a file
            for bus in solution:
                output_file.write(str(bus))

            output_file.close()


if __name__ == '__main__':
    main()
