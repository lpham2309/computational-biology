from operator import itemgetter
import sys

class Bruijn():
    def __init__(self, k=31):
        self.k = k
    
    def filter_non_repeated_k_mers(self, sequence_inputs):
        k_mers_count = {}
        list_of_k_mers = []
        good_read_sequence = set()
        for sequence in sequence_inputs:
            print(sequence)
            for i in range(0, len(sequence)-self.k+1):
                list_of_k_mers.append(sequence[i:self.k+i])
        print(1)
        for subseq in list_of_k_mers:
            if subseq not in k_mers_count:
                k_mers_count[subseq] = 1
            else:
                k_mers_count[subseq] += 1
        
        print(2)
        print(k_mers_count)

        for k, v in list(k_mers_count.items()):
            print(k_mers_count[k])
            if k_mers_count[k] < 2:
                del k_mers_count[k]

        print('Length = ', len(k_mers_count))
        
        for sequence in sequence_inputs:
            for subseq in k_mers_count:
                if k_mers_count[subseq] == 1:
                    continue
                elif k_mers_count[subseq] > 1 and subseq in sequence:
                    good_read_sequence.add(sequence+"\n")
        print(good_read_sequence)
        return good_read_sequence

    def write_to_file(self, sequence):
        with open('good_reads', 'w') as good_reads:
            good_reads.writelines(list(sequence))
            good_reads.close()

    def debruijnize(self, reads):
        nodes = set()
        not_starts = set()
        edges = []
        for r in reads:
            r1 = r[:-1]
            r2 = r[1:]
            nodes.add(r1)
            nodes.add(r2)
            edges.append((r1,r2))
            not_starts.add(r2)
        return (nodes,edges,list(nodes-not_starts))
    
    def make_node_edge_map(self, edges):
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
            print(trail)
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
        bruijn_graph = Bruijn()
    
    sequence_inputs = parse_string_inputs()

    
    reads = bruijn_graph.filter_non_repeated_k_mers(sequence_inputs)
    a = bruijn_graph.write_to_file(reads)
    # G = bruijn_graph.debruijnize(reads)
    # v = bruibjn_graph.visualize_debruijn(G)
    # print(v)
    # m = bruijn_graph.make_node_edge_map(G[1])
    # start = G[2][0] if (len(G[2]) > 0) else G[0][0]
    # t = bruijn_graph.eulerian_trail(m,start)
    # a = bruijn_graph.assemble_trail(t)

    


if __name__=='__main__':
    main(sys.argv)
