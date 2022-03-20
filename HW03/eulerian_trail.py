def eulerian_trail(self, m, v):
    nemap = m
    result_trail = []
    start = v
    result_trail.append(start)
    while (True):
        trail = []
        previous = start
        while (True):
            if (previous not in nemap):
                break
            next = nemap[previous].pop()
            if (len(nemap[previous]) == 0):
                nemap.pop(previous, None)
            trail.append(next)
            if (next == start):
                break
            previous = next
        # completed one trail
        # print(trail)
        index = result_trail.index(start)
        result_trail = result_trail[0:index + 1] + trail + result_trail[
            index + 1:len(result_trail)]
        # choose new start
        if (len(nemap) == 0):
            break
        found_new_start = False
        for n in result_trail:
            if n in nemap:
                start = n
                found_new_start = True
                break  # from for loop
        if not found_new_start:
            print("error")
            print("result_trail", result_trail)
            print(nemap)
            break
    return result_trail
