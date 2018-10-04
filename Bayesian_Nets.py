'''
Bayesian Nets
This structure(s) will need to represent the nodes, edges,
and the conditional probability tables (CPTs) for each node.
You will need a way to represent whether each node is a query variable, evidence variable, or unknown.
'''

import Node
#import numpy as np
import sys


if __name__ == "__main__":
    input_file_name = sys.argv[1]
    with open(input_file_name) as file:
        data = file.readlines()

    def InterpretFile(file):
        counter = 1
        parent_counter = 0
        parents = []
        for line in file:
            node_name, node_value, = line.split(':')
            counter=1
            if parent_counter > 1:
                parents.append(']')
            if node_value[counter] == '[':
                while node_value[counter] != ']':
                    parents.append(node_value[counter])
                    counter += 1
                    parent_counter += 1

        rp = []
        print(parents)
        for p in parents:
            if p.isdigit() or p == ']' or p == '[':
                rp.append(p)
        print(rp)
    InterpretFile(data)













    out_file = open(sys.argv[2],'w')

    # if result:
    #     for a in param.list_of_bags:
    #         line = [a.name+' ']
    #         for b in a.contains:
    #             line.append(b.name)
    #             line.append(' ')
    #         out_file.write(''.join(line))
    #         out_file.write('\n')
    #         num_of_items = 'number of items: ' + str(len(a.contains)) + '\n'
    #         out_file.write(num_of_items)
    #         total_weight_capacity = 'total weight: '+str(a.current_load)+' '+'total capacity: '+str(a.capacity)+'\n'
    #         out_file.write(total_weight_capacity)
    #         wasted = 'wasted capacity: ' + str(a.capacity - a.current_load)+'\n'
    #         out_file.write(wasted)
    #         out_file.write('\n')
    # else:
    #     out_file.write('No solution found')
    #
    #
    #
