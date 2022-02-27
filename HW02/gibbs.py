import random

def main(argv):
    input_sequences = []
    curr_input = []
    for line in sys.stdin:
        row = None
        if not ">" in line:
            row = line.replace("\n", "")
            curr_input.append(row)
    
    # Assume we have 6 sequences with same length, randomize a starting position
    sequence_length = len(curr_input[0])
    initial_site = random.randrange(0, sequence_length, 1)

    # Pick a s* to remove
    random_sequence_index = random.randrange(0, len(curr_input), 1)
    curr_input.remove(curr_input[random_sequence_index])

    propensityMatrix = []
    for i in range(len())

