import numpy as np
from copy import deepcopy


def alg(data, params):

    # LASTN = 6
    # AVG = 50
    # STD = 5
    # DIFF_MIN = -10
    # DIFF_MAX = 100000

    AVG, STD, LASTN, DIFF_MIN, DIFF_MAX = params

    prev_avg = 100000
    # prev_avg = float(np.mean([x[1] for x in data[0: LASTN]]))
    processed = 0
    processed_array = []

    if len(data) > LASTN:
        data = [[x[0], float(x[1])] for x in data]

        for i in range(LASTN - 1, len(data)):
            avg = float(np.mean([x[1] for x in data[i - (LASTN - 1): i + 1]]))
            std = float(np.std([x[1] for x in data[i - (LASTN - 1): i + 1]]))

            if avg > AVG and std < STD and DIFF_MIN < avg - prev_avg < DIFF_MAX:
                processed += avg - prev_avg
                # prev_avg = avg

            if processed < 0:
                processed = 0

            processed_array.append((data[i][0], processed))
            prev_avg = avg

    return deepcopy(processed_array)
