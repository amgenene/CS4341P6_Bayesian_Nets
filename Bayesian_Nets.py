'''
Bayesian Nets
This structure(s) will need to represent the nodes, edges,
and the conditional probability tables (CPTs) for each node.
You will need a way to represent whether each node is a query variable, evidence variable, or unknown.
'''
import sys
import Node
import random
import math
import numpy as np
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
        print(this_node.name, " CPT = ", this_node.CPT)

    #TODO For some reason the CPT values for the parentless nodes are not visible/non-existent after instatiation
    # We need to fix this if we want the code to work and I can't figure this out
    for n in all_nodes:
        print(all_nodes[n].name, " CPT = ", all_nodes[n].CPT)

    return all_nodes

#sys.setrecursionlimit(10000000)
def assign_node_state(state_file_name,all_nodes):
    with open(state_file_name) as state_file:
        state_data = state_file.readlines()
        a = state_data[0].split(',')
        list_of_nodes = []
        # print(a)
    sorted_node_name_list = sorted(all_nodes)
    for s in range(len(sorted_node_name_list)):
        all_nodes[sorted_node_name_list[s]].status = a[s]
        list_of_nodes.append(all_nodes[sorted_node_name_list[s]])
    return list_of_nodes

#TODO compare the random list with the node's CPT Table
'''
We will do this by comparing the numbers with the respective CPT values in the nodes
'''

def compare_node_status(node, index, current_8_status):
    # print("len(node)", len(node), sep=": ", end="; ")
    # print("index", index, sep=": ")
    if index > len(node) - 1:
        print("All nodes checked, returning true, match found")
        #print("Node: ", node[0].status, node[1].status, node[2].status, node[3].status, node[4].status, node[5].status, node[6].status, node[7].status, sep="   ")
        #print("Curr:", current_8_status)
        return True

    # print("Node status", node[index].status, sep=": ")
    if node[index].status == 't' or node[index].status == 'f':
        # print("case 1 entered: node status t/f")

        # If the node and the element in the array have the same status, check the next element in the array.
        if node[index].status == current_8_status[index]:
            # print("Node status: ",
            #       node[index].status,
            #       "| Current status: ",
            #       current_8_status[index],
            #       "| Node matched, continuing validation of set")
            index += 1
            return compare_node_status(node, index, current_8_status)
        else:
            # print("Node status:",
            #       node[index].status,
            #       "| Current status:",
            #       current_8_status[index],
            #       "Node mismatch, returning false, continuing search with new set")
            return False
    else:
        #print("case 2 entered: node status -/?")
        index += 1
        return compare_node_status(node, index, current_8_status)

def calc_conditional_probability(node, parents):
    index_of_CPT_array = 0
    # print("Index of CPT array: ", index_of_CPT_array)
    # Find the index of the CPT array that contains the correct conditional probability given the status of the parents
    for parent_num in range(len(parents)):
        # If the node has a true status, based on the evidence sample, add the binary value of that node to the index
        # This will provide the correct 'row in the truth table' for the conditional probability
        print(parents[parent_num].name, parents[parent_num].accepted, sep=" = ")
        if parents[parent_num].accepted == 't':
            # print("Accepted = t")
            index_increment = int(np.exp2(len(parents)-parent_num) / 2)
            print("Index inc: ", index_increment)
            index_of_CPT_array += index_increment
        # else:
        #     print("Accepted = f")

    # The conditional probability is equal to the value in the array
    conditional_probability = node.CPT[index_of_CPT_array]
    print("Conditional probability of node ", node.name, " given parents = ", conditional_probability)

    return conditional_probability

def calc_probability(query, nodes, evidence):
    print("Node: ", nodes[query].name, "| Query: ", query)
    print("Num parents: ", len(nodes[query].parents))
    if nodes[query].parents:
        # The conditional probability of the query node is based off its parents
        conditional_probability_query = calc_conditional_probability(nodes[query], nodes[query].parents)
        # For each parent of the query node, find its probability
        for parent in range(len(nodes[query].parents)):
            probability = conditional_probability_query * calc_probability(parent, nodes[query].parents, evidence) # The first term (query+1) is likely wrong
            print("Prob so far: ", probability)
        return probability
    else:
        print("calc_prob no parents")
        print("Len CPT: ", len(nodes[query].CPT))
        print("Query: ", query)
        print("Query cpt: ", nodes[query].name)
        if nodes[query].accepted == 't':
            probability = nodes[query].CPT[0]
        else:
            probability = 1 - nodes[query].CPT[0]
        return probability

    # if query.parents:
    #     # For each parent P of the query node, calculate the conditional probability of P given it's parents
    #     for ParentNode in query.parents:
    #         return calc_conditional_probability(ParentNode, evidence)
    # else:
    #     # If the query has no parents return the probability from the network option file given for its status
    #     if evidence[element] == 't':
    #         probability = query.CPT[0]
    #     else:
    #         probability = 1 - query.CPT[0]

#TODO now compare the given list and the query list and return the normalized percent

def rejection_sampling(list_compared, node):
    true_index = []
    false_index = []
    possible_satisfied = []
    list_accepted_sample = []

    for i in node:
        if i.status == '?':
            base_index = node.index(i)
        if i.status == 't':
            true_index.append(node.index(i))
        if i.status == 'f':
            false_index.append(node.index(i))

    for j in range(len(list_compared)):
        for k in true_index:
            if j % k == 0 and list_compared[j] == 't':
                possible_satisfied.append(list_compared[j])
        for l in false_index:
            if j % l == 0 and list_compared[j] == 'f':
                possible_satisfied.append((list_compared[j]))

    print("Base index: ", base_index)

    # To find a series of accepted samples in the randomly generated sample set, loop through sets of 8 adjacent
    # elements, starting with the first 8 elements. Compare the status of these elements to the required status of that
    # node in the list of nodes in the network. This is specified by the query file.
    # If the value for the node is t or f, the status of the element in the set of 8 array must match the node's status
    # If the value for the node is -, the status of the element in the set of 8 array doesn't have to match the status
    #    of the status of the node
    # If the value for the node is ?, this is the query variable -> want to know probability of ? node given other nodes
    for d in range(0, len(possible_satisfied)):
        # a is the set of 8 elements from the set of randomly generated statuses that are being compared to the 8 node's
        # statuses. It is a list of these statuses, statuses being true = 't' and false = 'f'
        a = possible_satisfied[d:d+8]
        # print(a)
        # print(" *** Comparing new set of nodes *** ")
        # Compare the statuses of the nodes in a to the nodes statuses as described in the query file. If the function
        # finds a set of statuses that match, return true. Append the matching statues to the list of accepted samples
        # and exit search. Otherwise return false and continue with a new set from the randomly generated set.
        if compare_node_status(node, 0, a):
            # print("TRUE")
            # print("d: ", d)
            # Append the elements of a to the list of accepted elements
            for element in range(0, len(a)):
                list_accepted_sample.append(a[element])
                node[element].accepted = a[element]
            break

    print("Sample statuses, match nodes: ", list_accepted_sample)

    # Calculate the probability of node ? given evidence nodes E
    # The node that is the query is in the base_index. Start calculating here, as this is the parent with no children
    Probability = calc_probability(base_index, node, list_accepted_sample)
    return Probability



def create_random(num_samples):
    rand_list = []
    for i in range(0, num_samples):
        x = random.uniform(0,1)
        x = round(x, 2)
        rand_list.append(x)
    # print(len(rand_list))
    return rand_list

create_sample = create_random(200)
the_nodes = build_bayesian_network('network_option_b.txt')
assigned_nodes = assign_node_state('query1.txt', the_nodes)
#dem_samples = sampling_comparisons(create_sample, assigned_nodes)
Probability_rejection_sampling = rejection_sampling(create_sample, assigned_nodes)
print("Probability: ", Probability_rejection_sampling)


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
