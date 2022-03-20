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
                good_read_sequence.append(seq + "\n")

    with open('good_reads', 'w') as good_reads:
        good_reads.writelines(list(good_read_sequence))
        good_reads.close()
