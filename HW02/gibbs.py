'''
Name: Lam Pham
Homework 2 - Part 2
'''
from random import choice
from operator import itemgetter
import random
import sys
import numpy as np

class GibbSampling():
    '''
    Gibb Sampling instance will default to motif value, probability
    neucleotide if there is no input value indicated in the command
    '''

    def __init__(self, motif=6, prob_nucleotide=0.25):
        self.motif = motif
        self.residues = ["A", "C", "G", "T"]
        self.probability_nucleotide = prob_nucleotide

    def create_msa_with_motif(self, sequence_inputs, initial_sites):
        '''
        Create a MSA from the list of sequences using initial states and motifs
        '''
        msa_matrix = []
        for i in range(len(sequence_inputs)):
            curr_sequence_index = initial_sites[i]
            msa_matrix = sequence_inputs[i][curr_sequence_index:curr_sequence_index+self.motif]
        return msa_matrix

    def random_remove_sequence_star(self, sequences, last_sequences):
        '''
        Randomly pick a s* from the list of sequences
        It ensures to not have the sequence randomized from previous phase be re-picked
        '''

        if len(last_sequences) > 0:
            random_sequence = choice([sequences[i] for i in range(len(sequences)) if sequences[i] not in last_sequences])
            removed_seq = sequences[sequences.index(random_sequence)]
            sequences.remove(removed_seq)
        else:
            random_sequence_index = random.randrange(0, len(sequences), 1)
            removed_seq = sequences[random_sequence_index]
            sequences.remove(removed_seq)

        return removed_seq
    
    def create_propensity_matrix(self, frequency_matrix):
        '''
        A method to create a Propensity Matrix from Frequency matrix
        '''
        sum_frequency = sum(frequency_matrix[0])
        
        propensity_matrix = np.array(frequency_matrix) / sum_frequency / self.probability_nucleotide
        
        propensity_matrix = propensity_matrix.tolist()

        return propensity_matrix

    def get_residues_count(self, subsequence):
        '''
        A method to count the number of occurence for each residue
        '''
        res = {}
        for residue in self.residues:
            res[residue] = subsequence.count(residue)
        return res

    def create_frequency_matrix(self, sequence_inputs):
        '''
        A method to create a frequency matrix by dividing occurrence by total number of
        occurence of all 4 residues
        '''
        frequency_matrix = []
        for seq in sequence_inputs:
            residue_count = self.get_residues_count(seq)
            sorted_by_residue = list(residue_count.values())
            frequency_matrix.append([(sorted_count + 1) for sorted_count in sorted_by_residue])
        return frequency_matrix

    def get_highest_scoring_n_mers(self, removed_sequence, propensity_matrix):
        '''
        A method to get subsequence with highest scoring
        '''
        subsequence_scores = dict()
        for i in range(0, len(removed_sequence)-self.motif):
            curr_sum = 0
            section = removed_sequence[i: i + self.motif]
            for idx, residue in enumerate(section):
                propensity_to_residue_dict = dict(zip(self.residues, propensity_matrix[idx]))
                curr_sum += propensity_to_residue_dict[residue]
            subsequence_scores[section] = curr_sum
        best_subsequence = max(subsequence_scores, key=subsequence_scores.get)
        best_score = subsequence_scores[best_subsequence]

        return {
            best_subsequence: best_score
        }

def parse_string_inputs():
    '''
    A method to parse input data
    '''
    curr_input = []
    input_row = ''
    for line in sys.stdin:
        if ">" in line:
            curr_input.append(input_row)
            input_row = ''
        else:
            row = line.replace("\n", "")
            input_row += row
    
    return curr_input[1:]
def main(argv):
    '''
    Proceed calculating the best score for PSSM
    '''

    if len(argv) > 1:
        # Grab motif value from command
        motif= itemgetter(1)(argv)
        gibb_sampling = GibbSampling(motif=int(motif))
    else:
        gibb_sampling = GibbSampling()

    sequence_inputs = parse_string_inputs()

    last_picked_sequence = []
    
    # Assume we have n-sequences with same length, randomize a starting position
    initial_site = [random.randrange(0, 10, 1) for sequence in sequence_inputs]

    parsed_sequence_inputs = gibb_sampling.create_msa_with_motif(sequence_inputs, initial_site)
    frequency_matrix = gibb_sampling.create_frequency_matrix(parsed_sequence_inputs)
    
    propensity_matrix = gibb_sampling.create_propensity_matrix(frequency_matrix)
    
    while len(sequence_inputs) > 0:
        # Pick a s* to remove
        removed_sequence = gibb_sampling.random_remove_sequence_star(sequence_inputs, last_picked_sequence)
        # We want to have an ability to keep track of all previously picked s*
        last_picked_sequence.append(removed_sequence)
        best_score = gibb_sampling.get_highest_scoring_n_mers(removed_sequence, propensity_matrix)
        print(best_score)
if __name__=='__main__':
    main(sys.argv)
