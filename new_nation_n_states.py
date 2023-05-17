# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 02:29:07 2022

@author: egsra
"""

import csv
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
    """
    We recursively go through the paths by going from 
    node to the neighbor until the path's length is n
    """
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

def get_nations(k, dic_states, dic_borders, state_filename):
    nations_1 = []
    nations_2 = []
    #Sort states by pop # dic with pop rank?
    if k%2==0:
        # Split the list into two parts
        # to find a n membered nation sets -->
        # we find two split nation sets -->
        # Valid nations are the ones in which the members of the 
        # split nations set have exactly one member in common  
        len_1 = k/2+1
        len_2 = k/2
    else:
        len_1 = (k+1)/2
        len_2 = None
    for state in dic_states: #ordered_state[:percent_selection]:
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
    cutoff = len(nations_1[0])+len(nations_2[0])-1
    for n1 in nations_1:
        for n2 in nations_2:
            nation_set = set(n1).union(set(n2))
            if len(nation_set)==cutoff:
                valid_nations.append(nation_set)
    return valid_nations

def match_with_neighbors(nations, borders):
    val_nations = []
    for nation in nations:
        n_list = [neighbor for state in nation for neighbor in borders[state] if neighbor not in nation]
        nation_set = [nation.union({x}) for x in n_list]
        val_nations += nation_set
    return val_nations


def thirds(threads:list, n:int, borders: dict, nations:list=[], val_nations=[]):
    # update the whole nation (add two adjacent nations)
    # # Thread --> Set of three collinear states
    # nations --> Current list of n state nations
    # Val nations --> Either contains the valid nations (len=n)
    # or it contains the updated list of nations --> adding threads to the current nation
    val_nations = []
    for curr_nation in nations:
        for thread in threads:
            thread_set = set(thread)
            addn = set(curr_nation).union(thread_set)
            if len(addn)==len(curr_nation)+2:
                val_nations.append(addn)
    if len(val_nations[0])==n:
        return val_nations
    elif len(val_nations[0])==n-1:
        # If we need one more memeber for the nations -->
        # we add all the valid neighbors for the states in the nations
        return match_with_neighbors(val_nations, borders)
    else:
        # If the difference between the number of states in the current n
        val_nations = thirds(threads, n, borders, nations=val_nations, val_nations=[])
    return val_nations

def new_nation_n_states(n, state_filename='usstates.csv', border_filename='border_data.csv'):
    borders, states= load_borders(border_filename, state_filename)
    nations = []
    if n<=4:
        # For n<=4 we can get all possible nations with 
        nations_1, nations_2 = get_nations(n, states, borders, state_filename)
        nations = filter_nations(nations_1,nations_2)
    else:
        threads, _ = get_nations(3, states, borders, state_filename)
        threads_array = np.array(threads)
        thread_pop = np.array([sum([states.get(x,0) for x in i]) for i in threads])
        threads_array = threads_array[np.argsort(thread_pop)][::-1]
        subset_selection = round(len(threads_array)/n-0.5)
        threads_array = threads_array[:subset_selection]
        nations = thirds(threads,n,borders=borders,nations=threads_array)
    pop_dic = {}
    for i in nations:
      pop_dic[sum([states.get(x,0) for x in i])] = tuple(i)
      
    max_pop = max(pop_dic.keys())
    return pop_dic[max_pop], max_pop

# print(new_nation_n_states(2, 'usstates.csv', 'border_data.csv'))
# print(new_nation_n_states(2, 'usstates.csv', 'border_data.csv'))
# from datetime import datetime
# s= datetime.now()
# print(new_nation_n_states(7, 'usstates.csv', 'border_data.csv'))
# print(datetime.now() - s)
# print(new_nation_n_states(19, 'usstates.csv', 'border_data.csv'))
