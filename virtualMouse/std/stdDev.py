import csv
import statistics as stats

SAMPLE_RATE = 200

X = []
A_MU = []
# Y = []
# Z = []

with open('readings.csv', 'r', newline='') as readings:
    for reading in csv.DictReader(readings):
        X.append(float(reading['x']))
        A_MU.append(float(reading['a_mu']))
        # Y.append(float(reading['y']))
        # Z.append(float(reading['z']))

stdevX = stats.stdev(X)
stdevA_MU = stats.stdev(A_MU)
# stdevY = stats.stdev(Y)
# stdevZ = stats.stdev(Z)

print('stdevX', stdevX)
print('stdevA_MU', stdevA_MU)
# print('stdevY', stdevY)
# print('stdevZ', stdevZ)
print()

varX = stats.variance(X)
varA_MU = stats.variance(A_MU)
# varY = stats.variance(Y)
# varZ = stats.variance(Z)

print('varX', varX)
print('varA_MU', varA_MU)
# print('varY', varY)
# print('varZ', varZ)

with open('results.txt', 'w', newline='') as results:
    results.write('Sample Rate ' + str(SAMPLE_RATE) + '\n')
    results.write('\n')

    results.write('stdevX ' + str(stdevX) + '\n')
    results.write('stdevA_MU ' + str(stdevA_MU) + '\n')
    # results.write('stdevY ' + str(stdevY) + '\n')
    # results.write('stdevZ ' + str(stdevZ) + '\n')
    results.write('\n')

    results.write('varX   ' + str(varX) + '\n')
    results.write('varA_MU   ' + str(varA_MU) + '\n')
    # results.write('varY   ' + str(varZ) + '\n')
    # results.write('varZ   ' + str(varZ) + '\n')
    results.write('\n')