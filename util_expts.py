# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 15:33:31 2022

@author: egsra
"""
import csv

dic_borders = {}
dic_states = {}

with open('usstates.csv', 'r') as f:
   for line in csv.reader(f):
      dic_states[line[1]] = int(line[3])

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

dic_states.pop('AK')
dic_states.pop('HI')

###
# import 
def find_all_paths(n, dic_borders = dic_borders, start = 'CA', path =[]):
  path = path + [start]
  if len(path) == n:
    # print(path)
    return [path]
  paths = []
  for node in dic_borders[start]:
    newpaths = []
    if node not in path:
      newpaths = find_all_paths(n, dic_borders, node, path)
    for newpath in newpaths:
      paths.append(newpath)
  return paths

#find_all_paths(n=3, dic_borders = dic_borders, start = 'CA', path =[])


def final(n):
    nations = []
    for state in dic_states:
        nations+=find_all_paths(n, dic_borders = dic_borders,
                                          start = state, path =[])
    return nations


def nation_pop(n, dic_states=dic_states):
  nations = final(n)
  pop_dic = {}
  for i in nations:
    pop_dic[sum([dic_states[x] for x in i])] = tuple(i)
    
  max_pop = max(pop_dic.keys())
  return pop_dic[max_pop], max_pop
  
  
    
    
    
    
    
    