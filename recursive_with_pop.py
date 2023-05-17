import csv
import math
import numpy as np

def load_regions(state_filename):
    states_dict = dict()

    with open(state_filename, 'r') as f:
        for line in csv.reader(f):
            states_dict[line[1]] = int(line[3])

    return states_dict

def sorted_states(state_filename):
    states = np.loadtxt(state_filename, dtype = str, delimiter=',', usecols= 1)
    pop = np.loadtxt(state_filename, dtype = int, delimiter=',', usecols= 3)
    
    return states[np.argsort(pop)][::-1]


def load_borders(border_filename, state_filename):
    dic_states = load_regions(state_filename)
    dic_borders = {}
    with open('border_data.csv', 'r') as f:
        header = f.readline()
        for line in csv.reader(f):
            states = list(line[1].split('-'))
            if states[0] in dic_states and states[1] in dic_states:
                if states[0] in dic_borders:
                    dic_borders[states[0]].append(states[1])
                else:
                    dic_borders[states[0]] = [states[1]]
                states.reverse()
                if dic_borders.get(states[0], 0) == 0:
                    dic_borders[states[0]] = [states[1]]
                else:
                    dic_borders[states[0]].append(states[1])
    dic_states = {k:v for k,v in dic_states.items() if k in dic_borders.keys()}
    return dic_borders, dic_states

def find_all_paths(start, path, current_pop, min_pop,
 min_length, dic_borders, states):
    path += [start]
    current_pop += states[start]
    if len(path) <= min_length:
        if current_pop >= min_pop:
            return [path], min_length
        paths = []
        for node in dic_borders[start]:
            newpaths = []
            if node not in path:
                newpaths, min_length = find_all_paths(node, path, current_pop, min_pop,
                                    min_length, dic_borders, states)
                if newpaths:
                    paths += newpaths
                    if len(newpaths) < min_length:
                        min_length = len(newpaths)
        return paths, min_length
    return None, min_length

def get_nations(min_pop, dic_states, dic_borders, state_filename):
    nations = []
    ordered_state = sorted_states(state_filename)
    percent_selection = math.floor(350*10**6/min_pop)
    min_length = 50
    #Sort states by pop # dic with pop rank?
    for state in ordered_state[:percent_selection]:
        #start from most pop # have a counter for population # Select top total states / n
        nation, min_length =find_all_paths(start=state,
                                        path=[], 
                                        current_pop=dic_states[state], 
                                        min_pop=min_pop,
                                        min_length=min_length,
                                        dic_borders=dic_borders,
                                        states=dic_states)
        nations += nation
    return nations


def new_nation_with_pop(p, state_filename, border_filename):
    p = p*10**6
    borders, states= load_borders(border_filename, state_filename)
    new_nations = get_nations(p, states, borders, state_filename)
    new_nations = [tuple(x) for x in new_nations]
    return new_nations
# from timeit import timeit
# s = timeit()
# print(new_nation_with_pop(34, 'usstates.csv', 'border_data.csv'))
# print(new_nation_with_pop(40, 'usstates.csv', 'border_data.csv'))
# print(new_nation_with_pop(50, 'usstates.csv', 'border_data.csv'))
# print(timeit()-s)