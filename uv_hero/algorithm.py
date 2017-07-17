import numpy as np
from copy import deepcopy

# A0
def alg0(raw_data, params):

    # the resulting array
    processed_array = []

    # unpacking the constants
    AVG, STD, LASTN, DIFF_MIN, DIFF_MAX = params

    # initializing the variables
    prev_avg = 100000
    processed = 0

    # check if there are at least LASTN raw data points
    if len(raw_data) > LASTN:

        # iterating through the raw data points
        for i in range(LASTN - 1, len(raw_data)):
            # getting the last LASTN readings
            last_LASTN_readings = [x[1] for x in raw_data[i - (LASTN - 1): i + 1]]

            # getting the average and standard deviation
            avg = float(np.mean(last_LASTN_readings))
            std = float(np.std (last_LASTN_readings))

            # adding the difference to the processed point
            if avg > AVG and std < STD and DIFF_MIN < (avg - prev_avg) < DIFF_MAX:
                processed += (avg - prev_avg)

            # appending the processed point
            processed_array.append((raw_data[i][0], processed))

            # updating the previous average
            prev_avg = avg

    # return the processed array
    return deepcopy(processed_array)

# A1
def alg1(data, params):
    AVG, STD, LASTN, DIFF_MIN, DIFF_MAX = params

    prev_avg = 100000
    prev_valid_avg = 1000000
    # prev_avg = float(np.mean([x[1] for x in data[0: LASTN]]))
    processed = 0
    processed_array = []

    if len(data) > LASTN:

        for i in range(LASTN - 1, len(data)):
            avg = float(np.mean([x[1] for x in data[i - (LASTN - 1): i + 1]]))
            std = float(np.std([x[1] for x in data[i - (LASTN - 1): i + 1]]))

            if avg > AVG and std < STD and DIFF_MIN < avg - prev_avg < DIFF_MAX:
                # processed += avg - prev_avg
                # prev_valid_avg = avg

                # if processed < 0:
                #    processed = 0

                if (avg - prev_valid_avg) > 10:
                    processed += avg - prev_valid_avg
                else:
                    processed += avg - prev_avg

                prev_valid_avg = avg

            processed_array.append((data[i][0], processed))
            prev_avg = avg

    return deepcopy(processed_array)

# A2
def alg(data, params):
    AVG, STD, LASTN, DIFF_MIN, DIFF_MAX, MULT, INTV = params
    # print(params)
    prev_avg = 100000
    prev_valid_avg = 1000000
    processed = 0
    processed_array = []
    avg_array = np.zeros(len(data))
    prev_valid_index = 1

    if len(data) > LASTN:
        data = [[x[0], float(x[1])] for x in data]

        for i in range(LASTN - 1, len(data)):
            avg = float(np.mean([x[1] for x in data[i - (LASTN - 1): i + 1]]))
            std = float(np.std([x[1] for x in data[i - (LASTN - 1): i + 1]]))
            avg_array[i] = avg

            if avg > AVG and std < STD and DIFF_MIN < avg - prev_avg < DIFF_MAX:

                if (avg - prev_valid_avg) > 10:
                    processed += avg - prev_valid_avg

                elif 200 < avg < (MULT * prev_valid_avg):
                    marker = 0
                    if (i - prev_valid_index) > INTV:
                        binary_array = np.zeros(i - INTV - prev_valid_index + 2)
                        for k in range(prev_valid_index, (i - (INTV - 2))):
                            test_array = avg_array[k:k + INTV]
                            for j in range(0, INTV):
                                if test_array[j] > 20:
                                    binary_array[k - prev_valid_index] = 1

                        for m in range(0, len(binary_array)):
                            if binary_array[m] == 0:
                                marker = 1

                    if marker == 1:
                        processed += avg - 200
                    else:
                        processed += avg - prev_avg

                else:
                    processed += avg - prev_avg

                prev_valid_avg = avg
                prev_valid_index = i

            processed_array.append((data[i][0], processed))
            prev_avg = avg

    return deepcopy(processed_array)
