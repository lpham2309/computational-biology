How to run:
- Note that motif is optional. If not provided, default is motif=6
- output_file_name parameter is optional. If not, the program should print multiple alignments and their score in the console

Steps to run:
- Run python3 gibbs.py <motif_value> < <input_file_name> > <output_file_name>


Questions:

5.2) 

With motifs=6, the algorithm finds the following 
{'GCTCTT': 8.388608000000003}
{'GCTCCT': 16.777216000000006}
{'GCTCCC': 8.388608000000003}
{'GCTCCT': 16.777216000000006}
{'GCCCCT': 8.388608000000003}
{'GCTCCT': 16.777216000000006}
{'TCTCCT': 8.388608000000003}
{'GCTCCT': 16.777216000000006}
{'GCTCCT': 16.777216000000006}

I tried running with different seeds the results does look similar because the score for each run even though are different. But they are fluctuate between either index 8 or 16

![alt text](https://ibb.co/K9CQvNR)

5.3)

The problem with the approach defining convergence is we just straight picking the best highest score from the propensity matrix. From the traditional way of calculating, we would divide the best score with the sum of all scores to yield the probability of a particular alignment correlated to the S*. With the approach just selecting the best score, it would be hard to determine the likeliness between the alignment and the S* sequence because we do not have a baseline on whether the current motif fits the current model. In addition, all values produced are all greater than 1 so we cannot really know which specific index / specific starting position would produce the best with potential of "misleading" positions.

I think one way to improve convergence is calculate the mean of the likeliness instead of the sum of all likeliness. From then, we can take the best score / mean of all score in the first half and the 2nd half of the sequence. This way, we can determine where the alignment likeliness to occur and then pick the starting position based on that. For example:

if best score = 2 and it yields higher prob for the 1st half of the sequence

Start at 2nd position on the first half

if best score = 2 and it yields higher prob for the 2nd half of the sequence

Start at 2nd position starting from the mid-point