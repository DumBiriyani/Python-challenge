# -*- coding: utf-8 -*-
"""
Uses recursion to find paths with length n
in a graph with 
"""

import csv
import math
import numpy as np

def load_regions(state_filename):
    states = np.loadtxt(state_filename, dtype = str, delimiter=',', usecols= 1)
    pop = np.loadtxt(state_filename, dtype = int, delimiter=',', usecols= 3)
    states = states[np.argsort(pop)][::-1]
    pop = np.sort(pop)[::-1]
    return dict(zip(states, pop)), states


def load_borders(border_filename, state_filename):
    dic_states, sorted_states = load_regions(state_filename)
    dic_borders = {}
    with open(border_filename, 'r') as f:
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
    return dic_borders, dic_states, sorted_states

def find_all_paths(n, dic_borders, start, path):
  path = path + [start]
  if len(path) == n:
    return [path]
  paths = []
  for node in dic_borders[start]:
    newpaths = []
    if node not in path:
      newpaths = find_all_paths(n, dic_borders, node, path)
      paths += newpaths
  return paths

def get_nations(n, dic_states, dic_borders, state_filename, sorted_states):
    nations = []
    ordered_state = sorted_states(state_filename)
    percent_selection = math.floor(len(dic_states)/n)
    #Sort states by pop # dic with pop rank?
    for state in ordered_state[:percent_selection]:
        #start from most pop # have a counter for population # Select top total states / n
        nations+=find_all_paths(n, dic_borders = dic_borders,
                                          start = state, path =[])
    return nations


def new_nation_n_states(n, state_filename='usstates.csv', border_filename='border_data.csv'):
    borders, states, sorted_states = load_borders(border_filename, state_filename)
    nations = get_nations(n, states, borders, state_filename, sorted_states)
    pop_dic = {}
    for i in nations:
      pop_dic[sum([states.get(x,0) for x in i])] = tuple(i)
      
    max_pop = max(pop_dic.keys())
    return pop_dic[max_pop], max_pop

# print(new_nation_n_states(1, 'usstates.csv', 'border_data.csv'))
# print(new_nation_n_states(2, 'usstates.csv', 'border_data.csv'))
# print(new_nation_n_states(3, 'usstates.csv', 'border_data.csv'))
# print(new_nation_n_states(19, 'usstates.csv', 'border_data.csv'))
