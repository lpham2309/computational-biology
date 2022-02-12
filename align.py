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
    for i in range(len(rows)+1):
        subMatrix = []
        for j in range(len(cols)+1):
            subMatrix.append(default_value)
        alignmentMatrix.append(subMatrix)
    return alignmentMatrix

def setAlignmentMatrix(rows, columns, gap):
    alignmentMatrix = createEmptyMatrix(rows, columns, 0)

    for j in range(1,len(columns)+1):
        alignmentMatrix[0][j] = j * gap
    for i in range(1,len(rows)+1):
        alignmentMatrix[i][0] = i * gap
    
    return alignmentMatrix

def setTraceBackMatrix(rows, columns):
	alignmentMatrix = createEmptyMatrix(rows, columns, '0')

	for j in range(1,len(columns)+1):
		alignmentMatrix[0][j] = 'LEFT'
	for i in range(1,len(rows)+1):
		alignmentMatrix[i][0] = 'TOP'
	alignmentMatrix[0][0] = 'DONE'
	return alignmentMatrix


def calculateGlobalAlignment(sequence_a, sequence_b, score):
    '''
    Initialize an aligment matrix to calculate score and
    a tracing matrix to keep track of the path to (0, 0) once completed
    '''
    alignment_matrix = setAlignmentMatrix(sequence_a, sequence_b, score.gap)
    traceBack = setTraceBackMatrix(sequence_a, sequence_b)

    for i in range(1, len(sequence_a)+1):
        for j in range(1, len(sequence_b)+1):
            left = alignment_matrix[i][j-1] + score.gap
            up = alignment_matrix[i-1][j] + score.gap
            diag = alignment_matrix[i-1][j-1] + score.checkMatchedSequences(sequence_a[i-1],sequence_b[j-1])
            alignment_matrix[i][j] = max(left,up,diag)
            if alignment_matrix[i][j] == diag:
                traceBack[i][j] = 'DIAGONAL'
            elif alignment_matrix[i][j] == up:
                traceBack[i][j] = 'TOP'
            elif alignment_matrix[i][j] == left:
                traceBack[i][j] = 'LEFT'
            else:
                traceBack[i][j] = 'DIAGONAL'
    return traceBack

def getGlobalSequenceAlignments(sequence_a, sequence_b, traceBack):
	rowOutput = []
	colOutput = []
	i = len(sequence_a)
	j = len(sequence_b)
	while i > 0 or j > 0:
		if traceBack[i][j] == 'DIAGONAL':
			rowOutput.append(sequence_a[i-1])
			colOutput.append(sequence_b[j-1])
			i -= 1
			j -= 1
		elif traceBack[i][j] == 'LEFT':
			rowOutput.append('-')
			colOutput.append(sequence_b[j-1])
			j -= 1
		elif traceBack[i][j] == 'TOP':
			rowOutput.append(sequence_a[i-1])
			colOutput.append('-')
			i -= 1
		elif traceBack[i][j] == 'DONE':
			break
	return rowOutput,colOutput

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
    
    traceBack = calculateGlobalAlignment(sequence_A, sequence_B, score)

    alignment_a, alignment_b = getGlobalSequenceAlignments(sequence_A, sequence_B, traceBack)

    print(printSequence(alignment_b))
    print(printSequence(alignment_a))

if __name__== "__main__":
    main(sys.argv)