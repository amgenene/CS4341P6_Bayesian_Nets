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
            all_nodes[this_node.name].CPT.append(float(v))

    # for n in all_nodes:
    #     print(n)
    #     print('   ', ' p is: ', all_nodes[n].CPT)
    #     for pp in all_nodes[n].parents:
    #         print('   ',' p is: ',pp.name)

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


def compare_node_status(node, index, current_8_status):
    # If the search index is greater than the amount of nodes, all nodes have been searched and returned true, meaning
    # a match has been found.
    if index > len(node) - 1:
        return True

    # If the node being checked has a status of true or false, check that the node and the element have the same status
    if node[index].status == 't' or node[index].status == 'f':
        # If the node and the element in the array have the same status, check the next element in the array.
        if node[index].status == current_8_status[index]:
            index += 1
            return compare_node_status(node, index, current_8_status)
        # If there is a mismatch, end the search and restart with a new set
        else:
            return False
    # If the node is not true or false, the status of the node is not important and the search can continue with the
    # next node
    else:
        index += 1
        return compare_node_status(node, index, current_8_status)

def calc_conditional_probability(node, parents):
    # Initially, the index of the CPT array is zero, representing the first element in the array. This must be modified
    # by the states of the nodes to determine the correct element in the array
    index_of_CPT_array = 0

    # Find the index of the CPT array that contains the correct conditional probability given the status of the parents
    for parent_num in range(0, len(parents)):
        # If the node has a true status, based on the evidence sample, add the binary value of that node to the index
        # This will provide the correct 'row in the truth table' for the conditional probability. If the status of the
        # node is false, this is like a zero in the truth table so its value is not added to the index variable.
        if parents[parent_num].accepted == 't':
            # The index increment is equal to the "binary value" the node has in the truth table. The array of parents
            # is read in like the values of a truth table, so each element in the array should have a value equal to
            # 2^(n-index), where n is the length of the array and index is the nodes index in the array. This is then
            # divided by two because binary is a base two system.
            index_increment = int(np.exp2(len(parents)-parent_num) / 2)

            # The correct place in the array is the sum of the true nodes values
            index_of_CPT_array += index_increment

    # The conditional probability is equal to the value in the array at the correct location, according to the state of
    # the parent nodes. Having found this index above, it is now trivial to retrieve the value.
    conditional_probability = node.CPT[index_of_CPT_array]
    return conditional_probability

def calc_probability(query, nodes, evidence):
    # If the query node has parents, find the conditional probability of the query node given the parent states
    if nodes[query].parents:
        # Find the conditional probability of the query node based off its parents and the CPTable
        conditional_probability_query = calc_conditional_probability(nodes[query], nodes[query].parents)

        # Probability initially equals conditional probability of query node from above
        probability = conditional_probability_query

        # For each parent of the query node, find its probability and multiply it in to the total probability
        for parent in range(len(nodes[query].parents)):
            # This is a recursive call to the calc_probability function to find the probability of all parents of query
            probability *= calc_probability(parent, nodes[query].parents, evidence)
        return probability

    # If the query node does not have parents, find its probability given its state
    else:
        # If the node is true, the probability is given in the CPTable
        if nodes[query].accepted == 't':
            probability = nodes[query].CPT[0]
        # If the node is false, the probability is 1 - the value in the CPTable
        else:
            probability = 1 - nodes[query].CPT[0]
        return probability

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

    for j in range(0, len(list_compared)):
        for k in true_index:
            if j % k == 0 and list_compared[j] == 't':
                possible_satisfied.append(list_compared[j])
        for l in false_index:
            if j % l == 0 and list_compared[j] == 'f':
                possible_satisfied.append((list_compared[j]))

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

        # Compare the statuses of the nodes in a to the nodes statuses as described in the query file. If the function
        # finds a set of statuses that match, return true. Append the matching statues to the list of accepted samples
        # and exit search. Otherwise return false and continue with a new set from the randomly generated set.
        if compare_node_status(node, 0, a):
            # Append the elements of a to the list of accepted elements and set the accepted value of each node to the
            # status of the accepted elements
            for element in range(0, len(a)):
                list_accepted_sample.append(a[element])
                node[element].accepted = a[element]
            break

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
dem_samples = sampling_comparisons(create_sample, assigned_nodes)
Probability_rejection_sampling = rejection_sampling(dem_samples, assigned_nodes)
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
