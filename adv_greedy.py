import csv

def load_regions(filename):
    states_dict = dict()

    with open(filename, 'r') as f:
        for line in csv.reader(f):
            states_dict[line[1]] = int(line[3])

    return states_dict

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
    dic_states = {k:v for k,v in dic_states.items() if k in dic_borders}
    # sorted_states = [k for k in sorted_states if k in dic_borders]
    return dic_borders, dic_states#, sorted_states


# This function returns the state and population of the "most populous
# neighbour bordering the candidate nation.
def most_populous_neighbor(states, borders, nation):
    neighbor = ''
    pop = 0

    for s in nation:
        neighbors = borders[s]
        for i in neighbors:
            curr_pop = states[i]
            if curr_pop>pop and i not in nation:
                pop = curr_pop
                neighbor = i

    return neighbor, pop

def get_best_nation(states, borders, n):
    critical_pop = 0
    best_nation = tuple()
    for i in states.keys():
        new_nation = (i,)
        max_pop = states[i]
        while len(new_nation) < n:
            next_st, pop = most_populous_neighbor(states, borders, new_nation)
            new_nation += (next_st,)
            max_pop += pop
        if critical_pop<max_pop:
            best_nation = new_nation
            critical_pop = max_pop
    return best_nation, critical_pop

def match_with_neighbors(nation, borders, states):
    n_list = [neighbor for state in nation for neighbor in borders[state] if neighbor not in nation]
    nations = [nation+(x,) for x in n_list]

    pop_dic = {}
    for i in nations:
      # Remove HI and AK from ordered_state
      pop_dic[sum([states.get(x,0) for x in i])] = tuple(i)
      
    max_pop = max(pop_dic.keys())
    return pop_dic[max_pop], max_pop

def new_nation_n_states(n, state_filename, border_filename):
    borders, states = load_borders(border_filename, state_filename)
    if n > 10:
        tend, pop = get_best_nation(states, borders, n-1)
        best_nation, critical_pop = match_with_neighbors(tend, borders, states)
    else:
        best_nation, critical_pop = get_best_nation(states, borders, n)
    return best_nation, critical_pop

## TESTING EVAL
# print(new_nation_n_states(1, 'usstates.csv', 'border_data.csv'))
# print(new_nation_n_states(2, 'usstates.csv', 'border_data.csv'))
# from datetime import datetime
# s= datetime.now()
# print(new_nation_n_states(13, 'usstates.csv', 'border_data.csv'))
# print(datetime.now() - s)
# print(new_nation_n_states(19, 'usstates.csv', 'border_data.csv'))