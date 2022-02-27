'''
Name: Lam Pham
Homework 1 - Part 2
'''

import sys
from operator import itemgetter

class ScoreSchemeParams():
    '''
    ScoreSchemeParams instance will default to match, mismatch and gap value
    if there is no value inputs indicated in the command
    '''
    def __init__(self, match=4, mismatch=-2, gap=-2):
        self.match = match
        self.mismatch = mismatch
        self.gap = gap

    def checkMatchedSequences(self, sequence_a, sequence_b):
        if sequence_a != sequence_b:
            return self.mismatch
        else:
            return self.match

def createEmptyMatrix(rows, cols, default_value):
    '''
    Initiate an empty matrix with rows and columns equivalent 
    to both input sequence length
    '''
    alignmentMatrix = []
    for i in range(len(rows) + 1):
        subMatrix = []
        for j in range(len(cols) + 1):
            subMatrix.append(default_value)
        alignmentMatrix.append(subMatrix)
    return alignmentMatrix

def setAlignmentMatrix(rows, columns, gap):
    alignmentMatrix = createEmptyMatrix(rows, columns, 0)

    for j in range(1,len(columns) + 1):
        alignmentMatrix[0][j] = j * gap
    for i in range(1,len(rows)+1):
        alignmentMatrix[i][0] = i * gap
    
    return alignmentMatrix

def setTraceBackMatrix(rows, columns):
	alignmentMatrix = createEmptyMatrix(rows, columns, '0')

	for j in range(1, len(columns) + 1):
		alignmentMatrix[0][j] = 'LEFT'
	for i in range(1, len(rows) + 1):
		alignmentMatrix[i][0] = 'TOP'
	alignmentMatrix[0][0] = 'COMPLETED'
	return alignmentMatrix


def calculateGlobalAlignment(sequence_a, sequence_b, score):
    '''
    Initialize an aligment matrix to calculate score and
    a tracing matrix to keep track of the path to (0, 0) once completed
    '''
    alignment_matrix = setAlignmentMatrix(sequence_a, sequence_b, score.gap)
    traceBack = setTraceBackMatrix(sequence_a, sequence_b)

    for i in range(1, len(sequence_a) + 1):
        for j in range(1, len(sequence_b) + 1):
            left_value = alignment_matrix[i][j-1] + score.gap
            top_value = alignment_matrix[i-1][j] + score.gap
            diagonal_value = alignment_matrix[i-1][j-1] + score.checkMatchedSequences(sequence_a[i-1],sequence_b[j-1])
            alignment_matrix[i][j] = max(left_value, top_value, diagonal_value)
            if alignment_matrix[i][j] == diagonal_value:
                traceBack[i][j] = 'DIAGONAL'
            elif alignment_matrix[i][j] == top_value:
                traceBack[i][j] = 'TOP'
            elif alignment_matrix[i][j] == left_value:
                traceBack[i][j] = 'LEFT'
            else:
                traceBack[i][j] = 'COMPLETED'
    return traceBack

def getGlobalSequenceAlignments(sequence_a, sequence_b, traceBack):
    rowOutput = []
    colOutput = []
    length_sequence_a = len(sequence_a)
    length_sequence_b = len(sequence_b)
    while length_sequence_a > 0 or length_sequence_b > 0:
        if traceBack[length_sequence_a][length_sequence_b] == 'DIAGONAL':
            rowOutput.append(sequence_a[length_sequence_a-1])
            colOutput.append(sequence_b[length_sequence_b-1])
            length_sequence_a -= 1
            length_sequence_b -= 1
        elif traceBack[length_sequence_a][length_sequence_b] == 'TOP':
            rowOutput.append(sequence_a[length_sequence_a-1])
            colOutput.append('-')
            length_sequence_a -= 1
        elif traceBack[length_sequence_a][length_sequence_b] == 'LEFT':
            rowOutput.append('-')
            colOutput.append(sequence_b[length_sequence_b-1])
            length_sequence_b -= 1
        elif traceBack[length_sequence_a][length_sequence_b] == 'COMPLETED':
            break
    return rowOutput, colOutput

def printSequence(sequence):
    output_string = ""
    for i in sequence[::-1]:
        output_string += i
    return output_string

def main(argv):
    
    input_sequences = []
    curr_input = []
    for line in sys.stdin:
        row = None
        if not ">" in line:
            row = line.replace("\n", "")
            curr_input.append(row)
    # Always a better way to do this, for now I'll keep both input sequences with similar length
    if len(curr_input) % 2 == 0:
        next_sequence = ''.join(curr_input[:len(curr_input) // 2])
        curr_sequence = ''.join(curr_input[len(curr_input) // 2:])
        input_sequences.append(curr_sequence)
        input_sequences.append(next_sequence)

    sequence_A, sequence_B = itemgetter(0,1)(input_sequences)

    if len(argv) > 1:
        # Grab match, mismatch and gap value from command
        match, mismatch, gap = itemgetter(1, 2, 3)(argv)
        score = ScoreSchemeParams(int(match), int(mismatch), int(gap))
    else:
        score = ScoreSchemeParams()
    
    traceBackMatrix = calculateGlobalAlignment(sequence_A, sequence_B, score)

    alignment_a, alignment_b = getGlobalSequenceAlignments(sequence_A, sequence_B, traceBackMatrix)

    print(printSequence(alignment_b))
    print(printSequence(alignment_a))

if __name__== "__main__":
    main(sys.argv)