def correct_timestamp(readings):
    first_time = readings[0][0]
    for read in readings:
        read[0] = read[0] - first_time