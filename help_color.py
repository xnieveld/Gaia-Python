''' public static float EstimateTemperature(float absolute_mag) '''
import random

def estimate_temperature(absolute_mag):
    ''' Estimates temperature from absolute magnitude '''
# absolute_mag = float
    temp = float(0)
    # print(absolute_mag)
    if absolute_mag > 15:
        temp = 2000
        print(temp)

    elif absolute_mag > 10:
        temp = random.uniform(2000, 4000)
    elif absolute_mag > 6:
        temp = random.uniform(3000, 5000)
    elif absolute_mag > 4:
        temp = random.uniform(4500, 6500)
        if random.uniform(0, 1) < 0.1:
            temp = 3000
    elif absolute_mag > 2:
        temp = random.uniform(6000, 10000)
        if random.uniform(0, 1) < 0.1:
            temp = random.uniform(3000, 6000)

    elif absolute_mag > -1:
        temp = random.uniform(10000, 20000)
        if random.uniform(0, 1) < 0.5:
            temp = random.uniform(3500, 6500)
    else:
        temp = random.uniform(20000, 40000)
        if random.uniform(0, 1) < 0.3:
            temp = random.uniform(6000, 12000)
    return temp

print(estimate_temperature(9.612088))
# print(temp)