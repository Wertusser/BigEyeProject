from collections import defaultdict

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 8)

def csv2dict(filename):
    result = defaultdict(list)
    with open(filename) as f:
        for line in f.readlines():
            word, score = line.replace("\"", "").split(",")
            score = int(score)
            if word not in result or score not in result[word]:
                result[word].append(score)
    return {key: mean(item) for key, item in result.items()}
