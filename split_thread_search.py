# -*- coding: utf-8 -*-
"""
We split our search into two n/2 membered nations
who are all consecutive neighbors. Then we find the valid n-membered
nations by finding the matching set of nations in the split
lists which have exactly 1 member in common.
"""

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
    return dic_borders, dic_states

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

def get_nations(n, dic_states, dic_borders, state_filename):
    nations_1 = []
    nations_2 = []
    ordered_state = sorted_states(state_filename)
    percent_selection = math.floor(len(dic_states)/n)
    #Sort states by pop # dic with pop rank?
    if n%2==0:
        len_1 = n/2+1
        len_2 = n/2
    else:
        len_1 = (n+1)/2
        len_2 = None
    for state in ordered_state[:percent_selection]:
        #start from most pop # have a counter for population # Select top total states / n
        if len_2:
            nations_1+=find_all_paths(len_1, dic_borders = dic_borders,
                                          start = state, path =[])
            nations_2+=find_all_paths(len_2, dic_borders = dic_borders,
                                          start = state, path =[])
        else:
            new_nation=find_all_paths(len_1, dic_borders = dic_borders,
                                          start = state, path =[])
            nations_1+=new_nation
            nations_2+=new_nation
            
    return nations_1,nations_2

def filter_nations(nations_1,nations_2):
    valid_nations = []
    cutoff = len(nations_1[0]+nations_2[0])-1
    for n1 in nations_1:
        for n2 in nations_2:
            nation_set = set(n1).union(set(n2))
            if len(nation_set)==cutoff:
                valid_nations.append(nation_set)
    return valid_nations



def new_nation_n_states(n, state_filename='usstates.csv', border_filename='border_data.csv'):
    borders, states= load_borders(border_filename, state_filename)
    nations_1,nations_2 = get_nations(n, states, borders, state_filename)
    nations = filter_nations(nations_1,nations_2)
    
    pop_dic = {}
    for i in nations:
      # Remove HI and AK from ordered_state
      pop_dic[sum([states.get(x,0) for x in i])] = tuple(i)
      
    max_pop = max(pop_dic.keys())
    return pop_dic[max_pop], max_pop

# print(new_nation_n_states(2, 'usstates.csv', 'border_data.csv'))
# print(new_nation_n_states(2, 'usstates.csv', 'border_data.csv'))
# print(new_nation_n_states(9, 'usstates.csv', 'border_data.csv'))
# print(new_nation_n_states(19, 'usstates.csv', 'border_data.csv'))
