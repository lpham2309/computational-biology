import random
import sys
from collections import Counter

def main(argv):
    curr_input = []
    for line in sys.stdin:
        row = None
        if not ">" in line:
            row = line.replace("\n", "")
            curr_input.append(row)
    
    # Assume we have 6 sequences with same length, randomize a starting position
    sequence_length = len(curr_input[0])
    initial_site = random.randrange(0, sequence_length, 1)

    residues = sorted(["A", "T", "C", "G"])
    propensityMatrix = []

    for seq in curr_input:
        propensityMatrix.append([(sorted_count + 1) / 64 / 0.25 for sorted_count in list(dict(sorted(Counter(seq).items())).values())])

    # Pick a s* to remove
    random_sequence_index = random.randrange(0, len(curr_input), 1)
    removed_seq = curr_input[random_sequence_index]
    curr_input.remove( removed_seq)
    temp = dict()
    for i in range(0, len(removed_seq)-initial_site):
        curr_sum = 0
        section = removed_seq[i: i + initial_site]
        for idx, residue in enumerate(section):
            propensity_to_residue_dict = dict(zip(residues, propensityMatrix[idx]))
            curr_sum += propensity_to_residue_dict[residue]
        temp[section] = curr_sum
        
if __name__=='__main__':
    main(sys.argv)
