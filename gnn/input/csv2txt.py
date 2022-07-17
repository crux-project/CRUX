import pandas as pd
import os

if not os.path.exists('./txt/'):
    os.makedirs('./txt/')

test = pd.read_csv('csv/test.csv')

# Node: Encode model as 0, data as 1
models = test['m.id'].unique()
datasets = test['d.id'].unique()

with open('txt/node.txt', 'a+') as f:
    for m in models:
        f.write(m + '\t' + str(0) + '\n')
    for d in datasets:
        f.write(d + '\t' + str(1) + '\n')

# model = pd.read_csv('csv/model.csv')
# data = pd.read_csv('csv/data.csv')
# with open('txt/node.txt', 'a+') as f:
#     for line in model.values:
#         f.write((str(line[0]) + '\t' + str(0) + '\n'))
#     for line in data.values:
#         f.write((str(line[0]) + '\t' + str(1) + '\n'))


# Test: (model, data) [runningTimes, f1_score, precision, recall]
with open('txt/edge.txt', 'a+') as f:
    for line in test.values:
        performance = [line[2], line[3], line[4], line[5]]
        f.write('(' + (str(line[0]) + ',' + (str(line[1]) + ')'
                                             + '\t' + str(performance) + '\n')))


# Top5: (model, data) [runningTimes, f1_score, precision, recall]
def perform(a, b, c, d):
    return 0.4 * b + 0.1 * c + 0.1 * d - 0.01 * a


test['performance'] = test.apply(lambda test: perform(
    test['r.runningTimes'], test['r.f1_score'], test['r.precision'], test['r.recall']), axis=1)
test['rank'] = test['performance'].groupby(test['d.id']).rank(ascending=False, method='first').astype(int)

test.to_csv('csv/test_rank.csv')

with open('txt/top5.txt', 'a+') as f:
    for line in test.values:
        if line[-1] > 5:
            continue

        performance = [line[2], line[3], line[4], line[5]]
        f.write('(' + (str(line[0]) + ',' + (str(line[1]) + ')'
                                             + '\t' + str(performance) + '\n')))
