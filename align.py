'''
Name: Lam Pham
Homework 1 - Part 2
'''

import sys
from operator import itemgetter

class ScoreSchemeParams():
    def __init__(self, match=4, mismatch=-2, gap=-2):
        self.match = match
        self.mismatch = mismatch
        self.gap = gap

    def checkMatchedSequences(self, sequence_a, sequence_b):
        if sequence_a != sequence_b:
            return self.mismatch
        else:
            return self.match


def setAlignmentMatrix(rows, columns, gap):
    alignmentMatrix = []
    for i in range(len(rows)+1):
        subMatrix = []
        for j in range(len(columns)+1):
            subMatrix.append(0)
        alignmentMatrix.append(subMatrix)

    for j in range(1,len(columns)+1):
        alignmentMatrix[0][j] = j * gap
    for i in range(1,len(rows)+1):
        alignmentMatrix[i][0] = i * gap
    
    return alignmentMatrix

def setTraceBackMatrix(rows, columns):
	matrix = []
	for i in range(len(rows)+1):
		subMatrix = []
		for j in range(1, len(columns)+1):
			subMatrix.append('0')
		matrix.append(subMatrix)

	for j in range(1,len(columns)+1):
		matrix[0][j] = 'LEFT'
	for i in range(1,len(rows)+1):
		matrix[i][0] = 'TOP'
	matrix[0][0] = 'DONE'
	return matrix


def calculateGlobalAlignment(sequence_a, sequence_b, score):
    alignment_matrix = setAlignmentMatrix(sequence_a, sequence_b, score.gap)
    traceBack = setTraceBackMatrix(sequence_a, sequence_b)

    for i in range(1,len(sequence_a)+1):
        for j in range(1,len(sequence_b)+1):
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

def getAlignedSequences(sequence_a, sequence_b, traceBack):
	xSeq = []
	ySeq = []
	i = len(sequence_a)
	j = len(sequence_b)
	while(i > 0 or j > 0):
		if traceBack[i][j] == 'DIAGONAL':
			xSeq.append(sequence_a[i-1])
			ySeq.append(sequence_b[j-1])
			i = i-1
			j = j-1
		elif traceBack[i][j] == 'LEFT':
			xSeq.append('-')
			ySeq.append(sequence_b[j-1])
			j = j-1
		elif traceBack[i][j] == 'TOP':
			# Up holds true when '-' is added from y string and x[j-1] from x string
			xSeq.append(sequence_a[i-1])
			ySeq.append('-')
			i = i-1
		elif traceBack[i][j] == 'DONE':
			break
	return xSeq,ySeq

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

    alignment_a, alignment_b = getAlignedSequences(sequence_A, sequence_B,traceBack)

    print(printSequence(alignment_b))
    print(printSequence(alignment_a))

if __name__== "__main__":
    main(sys.argv)