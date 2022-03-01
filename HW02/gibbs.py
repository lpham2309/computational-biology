import random
import sys

def main(argv):
    input_sequences = []
    curr_input = []
    for line in sys.stdin:
        row = None
        if not ">" in line:
            row = line.replace("\n", "")
            curr_input.append(row)
    
    # print(curr_input)
    # Assume we have 6 sequences with same length, randomize a starting position
    sequence_length = len(curr_input[0])
    initial_site = random.randrange(0, sequence_length, 1)

    # Pick a s* to remove
    random_sequence_index = random.randrange(0, len(curr_input), 1)
    curr_input.remove(curr_input[random_sequence_index])
    # print(curr_input)
    
    propensityMatrix = []
    residues = ["A", "T", "C", "G"]
    for i in range(len(residues)):
        subMatrix = []
        for j in range(len(curr_input)):
            subMatrix.append(0)
        propensityMatrix.append(subMatrix)
    
    
if __name__=='__main__':
    main(sys.argv)
