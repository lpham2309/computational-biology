from collections import defaultdict
from operator import itemgetter
import sys

class Node():

    def __init__(self,
                 visited=False,
                 label='',
                 num_of_visits=1):
        self.visited = visited
        self.is_branch = False
        self.label = label
        self.num_of_visits = num_of_visits
        self.outgoing_edges = []
        self.incoming_edges = []


class Bruijn():

    def __init__(self, k=31):
        self.k = k
        self.graph_data = {}

    def filter_non_repeated_k_mers(self, sequence):
        res = []
        for i in range(0, len(sequence) - self.k + 1):
            res.append(sequence[i:self.k + i])
        return res

    def construct_deBruijn_graph(self, node_instances):
        for index, node in enumerate(node_instances):
            graph = self.graph_data
            curr_node = None
            if node not in graph:
                graph[node] = Node(label=node)
                curr_node = graph[node]
            elif node in graph:
                curr_node = graph[node]
                curr_node.num_of_visits += 1
            if index - 1 >= 0:
                curr_node.incoming_edges.append(node_instances[index - 1])
            if index + 1 < len(node_instances):
                curr_node.outgoing_edges.append(node_instances[index + 1])
            curr_node.is_branch = len(curr_node.incoming_edges) > 1 or len(
                    curr_node.outgoing_edges) > 1

    def iterate_helper(self, curr_node, result):
        # validate curr_node if it's visited or is a branching node
        if curr_node.visited or curr_node.is_branch:
            return result
    
        incoming_edges = curr_node.incoming_edges
        outgoing_edges = curr_node.outgoing_edges

        # mark current node as visited
        curr_node.visited = True

        # recursively iterate through all incoming + outgoing node
        incoming_path, outgoing_path = '', ''
        for edge in incoming_edges:
            incoming_node = self.graph_data[edge]
            if self.iterate_helper(incoming_node, result) != None:
                incoming_path += self.iterate_helper(incoming_node, result)
        for edge in outgoing_edges:
            outgoing_node = self.graph_data[edge]
            if self.iterate_helper(outgoing_node, result) != None:
                outgoing_path += self.iterate_helper(outgoing_node, result)
        result += (incoming_path + curr_node.label+ outgoing_path)
        return result

    def iterate_graph(self):
        substrings = self.graph_data.keys()
        eulerian_path = None
        for substring in substrings:
            substringGraphNode = self.graph_data[substring]
            eulerian_path = self.iterate_helper(substringGraphNode, '')
            if eulerian_path:
                with open('output_contigs', 'a') as output_contigs:
                    output_contigs.write(eulerian_path+"\n")
                    output_contigs.close()
                with open('contig_lengths', 'a') as contig_lengths:
                    contig_lengths.write(str(len(eulerian_path))+"\n")
                    contig_lengths.close()
                    
def parse_string_inputs():
    '''
    A method to parse input data
    '''
    curr_input = []
    for line in sys.stdin:
        row = line.replace("\n", "")
        curr_input.append(row)

    return curr_input

def main(argv):

    if len(argv) > 1:
        k_mers = itemgetter(1)(argv)
        bruijn_graph = Bruijn(k=int(k_mers))
    else:
        bruijn_graph = Bruijn()

    sequence_inputs = parse_string_inputs()

    labeled_nodes = []

    for sequence in sequence_inputs:
        labeled_nodes += bruijn_graph.filter_non_repeated_k_mers(sequence)
        bruijn_graph.construct_deBruijn_graph(labeled_nodes)
    
    bruijn_graph.iterate_graph()


if __name__ == '__main__':
    main(sys.argv)
