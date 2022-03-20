from operator import itemgetter
import sys
import numpy as np

class Node():
    def __init__(self, marker=False, is_branch=False, label='', num_of_visits=1, outgoing_edges=[]):
        self.marker = marker
        self.is_branch = is_branch
        self.label = label
        self.num_of_visits = num_of_visits
        self.outgoing_edges = outgoing_edges
class Bruijn():
    def __init__(self, k=31, graph_data = {}):
        self.k = k
        self.graph_data = graph_data
    
    def filter_non_repeated_k_mers(self, sequence):
        res = []
        for i in range(0, len(sequence)-self.k+1):
            res.append(Node(label=sequence[i:self.k+i]))
        return res
    
    def write_to_file(self, sequence_inputs):
        k_mers_count = {}
        good_read_sequence = []
        list_of_k_mers = None
        for sequence in sequence_inputs:
            list_of_k_mers = self.filter_non_repeated_k_mers(sequence)

        for subseq in list_of_k_mers:
            if subseq not in k_mers_count:
                k_mers_count[subseq] = 1
            else:
                k_mers_count[subseq] += 1
        
        print(k_mers_count)
        # for k, v in list(k_mers_count.items()):
        #     if k_mers_count[k] < 2:
        #         del k_mers_count[k]
        for subseq in k_mers_count:
            for seq in sequence_inputs:
                if k_mers_count[subseq] >= 2 and subseq in sequence_inputs:
                    good_read_sequence.append(seq+"\n")

        with open('good_reads', 'w') as good_reads:
            good_reads.writelines(list(good_read_sequence))
            good_reads.close()

    def construct_deBruijn_graph(self, node_instances, all_nodes, all_edges, not_starting_node):

        # for curr_node in node_instances:
        #     last_node = curr_node.label[:-1]
        #     surrounding_node = curr_node.label[1:]
        #     all_nodes.add(last_node)
        #     all_nodes.add(surrounding_node)
        #     all_edges.append((last_node,surrounding_node))

        #     not_starting_node.add(surrounding_node)
        # return (all_nodes,all_edges,list(all_nodes-not_starting_node))


        for index, node in enumerate(node_instances):
            if node not in self.graph_data:
                self.graph_data[node] = Node(label=node)
            else:
                self.graph_data[node].num_of_visits += 1
                self.graph_data[node].marker = True
                self.is_branch = True
                if index + 1 < len(node_instances):
                    self.graph_data[node].outgoing_edges.append(node_instances[index+1])
    
    def filter_graph_by_one_occurence(self):
        for key, data in self.graph_data.items():
            if data.num_of_visits < 2:
                del self.graph_data[key]
        
    def make_node_edge_map(self, edges):
        # print("Edges: ", edges)
        node_edge_map = {}
        for e in edges:
            n = e[0]
            if n in node_edge_map:
                node_edge_map[n].append(e[1])
            else:
                node_edge_map[n] = [e[1]]
        return node_edge_map

    def eulerian_trail(self, m,v):
        nemap = m
        result_trail = []
        start = v
        result_trail.append(start)
        while(True):
            trail = []
            previous = start
            while(True):
                if(previous not in nemap):
                    break
                next = nemap[previous].pop()
                if(len(nemap[previous]) == 0):
                    nemap.pop(previous,None)
                trail.append(next)
                if(next == start):
                    break
                previous = next
            # completed one trail
            # print(trail)
            index = result_trail.index(start)
            result_trail = result_trail[0:index+1] + trail + result_trail[index+1:len(result_trail)]
            # choose new start
            if(len(nemap)==0):
                break
            found_new_start = False
            for n in result_trail:
                if n in nemap:
                    start = n
                    found_new_start = True
                    break # from for loop
            if not found_new_start:
                print("error")
                print("result_trail",result_trail)
                print(nemap)
                break
        return result_trail

    def assemble_trail(self, trail):
        if len(trail) == 0:
            return ""
        result = trail[0][:-1]
        for node in trail:
            result += node[-1]
        return result

    def visualize_debruijn(self, G):
        nodes = G[0]
        edges = G[1]
        dot_str= 'digraph "DeBruijn graph" {\n '
        for node in nodes:
            dot_str += '    %s [label="%s"] ;\n' %(node,node)
        for src,dst in edges:
            dot_str += '    %s->%s;\n' %(src,dst)
        return dot_str + '}\n'
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
        k_mers= itemgetter(1)(argv)
        bruijn_graph = Bruijn(k=int(k_mers))
    else:
        bruijn_graph = Bruijn(k=5)
    
    sequence_inputs = parse_string_inputs()

    all_nodes = None
    starting_node = None
    all_edges = None

    total_nodes = set()
    total_not_starting_node = set()
    total_all_edges = []

    labeled_nodes = []


    for sequence in sequence_inputs:
        labeled_nodes += bruijn_graph.filter_non_repeated_k_mers(sequence)
        bruijn_graph.construct_deBruijn_graph(bruijn_graph.graph_data, labeled_nodes, total_nodes, total_all_edges, total_not_starting_node)

        print(starting_node)
    # bruijn_graph.count_repeated_nodes(labeled_nodes, total_nodes)
        # m = bruijn_graph.make_node_edge_map(graph_nodes[1])
        # graph_nodes = list(graph_nodes)
        # start = graph_nodes[2][0] if (len(graph_nodes[2]) > 0) else graph_nodes[0][0]
        # t = bruijn_graph.eulerian_trail(m,start)
        # print(t)
        # a = bruijn_graph.assemble_trail(t)
        # print(a)

    
    bruijn_graph.filter_graph_by_one_occurence()

if __name__=='__main__':
    main(sys.argv)
