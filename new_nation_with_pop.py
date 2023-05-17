import csv
import pandas as pd


def load_regions(filename):
    states_dict = dict()

    with open(filename, 'r') as f:
        for line in csv.reader(f):
            states_dict[line[1]] = int(line[3])

    return states_dict


def load_borders(filename):
    borders_list = list()

    with open(filename, 'r') as f:
        state_list = []
        for line in csv.reader(f, 1):
            states = line[1].split('-')
            if len(states) == 2:
                borders_list.append((states[0], states[1]))
            state_list += states
    return borders_list, set(state_list)


# This function returns the state and population of the "most populous
# neighbor" bordering the candidate nation.
def most_populous_neighbor(states, borders, nation):
    neighbor = ''
    pop = 0

    for s in nation:
        for border in borders:
            if border[0] == s and border[1] in states:
                candidate = border[1]
                candidate_pop = states[border[1]]

                if candidate not in nation and candidate_pop > pop:
                    neighbor = candidate
                    pop = candidate_pop

            if border[1] == s and border[0] in states:
                candidate = border[0]
                candidate_pop = states[border[0]]

                if candidate not in nation and candidate_pop > pop:
                    neighbor = candidate
                    pop = candidate_pop

    return neighbor, pop

def add_combo(starting_state, states, borders, p, max_len=50):
    new_nation = {starting_state}
    max_pop = states[starting_state]

    # This is a "greedy" algorithm - we simply find the most populous
    # state bordering our candidate nation and append it to the list.
    while max_pop < p * 10 ** 6 and len(new_nation)<max_len:
        next_st, pop = most_populous_neighbor(states, borders, new_nation)
        if next_st!='':
            new_nation.add(next_st)
            max_pop += pop
    return new_nation, max_pop

def new_nation_with_pop(p, region_filename, border_filename):
    states = load_regions(region_filename)
    borders, state_set = load_borders(border_filename)

    # Our naive implementation arbitrarily starts with the 'first' state
    # returned by load_states. One easy improvement would be to replace this
    # with the most populous state, but you can do far better than this!
    remove_states = [x for x in states.keys() if x not in state_set]
    states_df = pd.DataFrame.from_dict(states, orient="index", columns=["pop"]).sort_values(by="pop", ascending=False)

    new_nations = []
    max_len=50
    state_ranks = states_df.index.drop(remove_states)
    
    for i in state_ranks:
        new_nation, n_pop = add_combo(starting_state=i,
                states=states, borders=borders, p=p, max_len=max_len)
        if n_pop > p * 10 ** 6:
            if len(new_nation)<max_len:
                new_nations = [new_nation]
                max_len = len(new_nation)
            elif new_nation not in new_nations:
                new_nations.append(new_nation)
    new_nations = [tuple(x) for x in new_nations]
    return new_nations
# from timeit import timeit
# s = timeit()
# print(new_nation_with_pop(34, 'usstates.csv', 'border_data.csv'))
# print(new_nation_with_pop(40, 'usstates.csv', 'border_data.csv'))
# print(new_nation_with_pop(50, 'usstates.csv', 'border_data.csv'))
# print(timeit()-s)

# TESTING EVAL!!!