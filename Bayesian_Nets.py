'''
Bayesian Nets
This structure(s) will need to represent the nodes, edges,
and the conditional probability tables (CPTs) for each node.
You will need a way to represent whether each node is a query variable, evidence variable, or unknown.
'''

import Node
import random
import math
#import numpy as np
import sys


# if __name__ == "__main__":
#     input_file_name = sys.argv[1]
#     with open(input_file_name) as file:
#         data = file.readlines()


def build_bayesian_network(file_name):
    with open(file_name) as file:
        data = file.readlines()
    all_nodes = {}
    for line in data:
        node_name,node_value=line.split(':')

        # parse the values
        garbage,parents_bracket, cpt_bracket = node_value.split('[')
        parents_bracket = parents_bracket.replace(']', '')
        cpt_bracket = cpt_bracket.replace(']','')
        parents_name_list = parents_bracket.split()
        cpt_values_list = cpt_bracket.split()

        # create the current node
        this_node = Node.Node(node_name)
        # create all parents
        if parents_name_list:
            for p in parents_name_list:
                if p in all_nodes:
                    # append this node to parent's children list
                    all_nodes[p].children.append(this_node)
                    # add parent node to current node's parents
                    this_node.parents.append(all_nodes[p])
                else:
                    # create parent node
                    new_parent = Node.Node(p)
                    # append this node to parent's children list
                    new_parent.children.append(this_node)
                    # add parent node to current node's parents
                    this_node.parents.append(new_parent)
                    # add parent to node dict
                    all_nodes[p] = new_parent
                    # add to node dict
            if this_node.name in all_nodes:
                this_node.parents.extend(all_nodes[this_node.name].parents)
                this_node.children.extend(all_nodes[this_node.name].children)
            all_nodes[this_node.name] = this_node
        # create all cpt
        for v in cpt_values_list:
            this_node.CPT.append(float(v))

    # for n in all_nodes:
    #     # print(n)
    #     for pp in all_nodes[n].parents:
    #         # print('   ',n,' child is: ',pp.name)

    return all_nodes


def assign_node_state(state_file_name,all_nodes):
    with open(state_file_name) as state_file:
        state_data = state_file.readlines()
        a = state_data[0].split(',')
        list_of_nodes = []
        # print(a)
    sorted_node_name_list = sorted(all_nodes)
    for s in range(len(sorted_node_name_list)):
        all_nodes[sorted_node_name_list[s]].status = a[s]
        all_nodes[sorted_node_name_list[s]].query_list.append(a)
        list_of_nodes.append(all_nodes[sorted_node_name_list[s]])
    return list_of_nodes

#TODO compare the random list with the node's CPT Table
'''
We will do this by comparing the numbers with the respective CPT values in the nodes
'''
def sampling_comparisons(rand_list, node):
    list_of_comparisons = []
    for i in rand_list:
        for j in node:
            for k in j.CPT:
                if i <= k:
                    list_of_comparisons.append('t')
                else:
                    list_of_comparisons.append('f')
    return list_of_comparisons


#TODO now compare the given list and the query list and return the normalized percent
def rejection_sampling(list_compared, node):
    true_index = []
    false_index = []
    possible_satisfied = []
    distances_between_tru = []
    distances_between_false = []
    distances_between_tru_and_false = []
    list_accepted_sample = []
    for i in node:
        if i.status == '?':
            base_index = node.index(i)
        if i.status == 't':
            true_index.append(node.index(i))
        if i.status == 'f':
            false_index.append(node.index(i))
    for a in true_index:
        for b in false_index:
            distances_between_tru_and_false.append(abs(a-b))
    for c in range(0, len(true_index) - 1):
        distances_between_tru.append(abs(true_index[c] - true_index[c+1]))
    for d in range(0, len(false_index) - 1):
        distances_between_false.append(abs(false_index[d] - false_index[d+1]))
    for j in range(0, len(list_compared)):
        for k in true_index:
            if j % k == 0 and list_compared[j] == 't':
                possible_satisfied.append(list_compared[j])
        for l in false_index:
            if j % l == 0 and list_compared[j] == 'f':
                possible_satisfied.append((list_compared[j]))
    for d in range(0, len(possible_satisfied)):
        for e in range(0, len(node[0].query_list)):
            if node[0].query_list[e] == 't' and possible_satisfied[d] == 'f':
                continue
            elif node[0].query_list[e] == 'f' and possible_satisfied[d] == 't':
                continue
            elif node[0].query_list[e] == 'f' and possible_satisfied[d] == 'f':
                list_accepted_sample.append(possible_satisfied[d])
            elif node[0].query_list[e] == 't' and possible_satisfied[d] == 't':
                list_accepted_sample.append(possible_satisfied[d])
            elif node[0].query_list[e] == '-' or e == '?':
                list_accepted_sample.append(possible_satisfied[d])
    return list_accepted_sample
    pass



def create_random(num_samples):
    rand_list = []
    for i in range(0, num_samples):
        x = random.uniform(0,1)
        x = round(x, 2)
        rand_list.append(x)
    return rand_list


create_sample = create_random(10000)
the_nodes = build_bayesian_network('network_option_b.txt')
assigned_nodes = assign_node_state('query1.txt', the_nodes)
dem_samples = sampling_comparisons(create_sample, assigned_nodes)
rejection_sampling(dem_samples, assigned_nodes)



    #
    #
    #
    # out_file = open(sys.argv[2],'w')
    #
    # # if result:
    # #     for a in param.list_of_bags:
    # #         line = [a.name+' ']
    # #         for b in a.contains:
    # #             line.append(b.name)
    # #             line.append(' ')
    # #         out_file.write(''.join(line))
    # #         out_file.write('\n')
    # #         num_of_items = 'number of items: ' + str(len(a.contains)) + '\n'
    # #         out_file.write(num_of_items)
    # #         total_weight_capacity = 'total weight: '+str(a.current_load)+' '+'total capacity: '+str(a.capacity)+'\n'
    # #         out_file.write(total_weight_capacity)
    # #         wasted = 'wasted capacity: ' + str(a.capacity - a.current_load)+'\n'
    # #         out_file.write(wasted)
    # #         out_file.write('\n')
    # # else:
    # #     out_file.write('No solution found')
    # #
    # #
    # #
