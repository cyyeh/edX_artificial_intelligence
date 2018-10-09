import sys
import numpy as np

def normalize(data):
    return np.average(data), np.std(data)

def gradient(w, x, y):
    y_estimate = np.dot(x, w)   
    error = y_estimate - y
    return (1.0/len(x)) * (np.dot(error, x))

def squared_error(w, x, y):
    y_estimate = np.dot(x, w)
    error = y_estimate - y
    return np.dot(error.transpose(), error)

def writeResult(f, alpha, iterations, weights):
    f.write(str(alpha) + ',' + str(iterations) + ',' + str(weights[0]) + ',' + str(weights[1]) + ',' + str(weights[2]) + '\n')

def main():
    if len(sys.argv) == 3:
        input_file_name = sys.argv[1]
        output_file_name = sys.argv[2]

        xn = []
        features = {
            'age': [],
            'weight': []
        }
        labels = []

        with open(input_file_name, mode='r') as f:
            lines = f.read().splitlines()
            for line in lines:
                inputs = line.split(',')
                features['age'].append(float(inputs[0]))
                features['weight'].append(float(inputs[1]))
                labels.append(float(inputs[-1]))

        # preprocessing: normalization on features
        avg_age, std_dev_age = normalize(features['age'])
        avg_weight, std_dev_weight = normalize(features['weight']) 

        for age, weight in zip(features['age'], features['weight']):
            xn.append([1.0, (age - avg_age) / std_dev_age, (weight - avg_weight) / std_dev_weight])

        # Linear Regression
        alphas = (0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10) # learning rates
        iterations = 100

        with open(output_file_name, mode='w') as f:
            for alpha in alphas:
                weights = np.zeros(3)
                for _ in range(iterations):
                    weights = weights - alpha * gradient(weights, xn, labels)
                writeResult(f, alpha, iterations, weights)
            
            # find best heuristic
            iterations = (100, 500, 1000, 5000, 10000)
            min_error = 100000
            heuristic = {
                'alpha': None,
                'iteration': None,
                'b_0': None,
                'b_age': None,
                'b_weight': None
            }

            for alpha in alphas:
                for iteration in iterations:
                    weights = np.zeros(3)
                    for _ in range(iteration):
                        weights = weights - alpha * gradient(weights, xn, labels)
                    error = squared_error(weights, xn, labels)
                    if error < min_error:
                        min_error = error
                        heuristic['alpha'] = alpha
                        heuristic['iteration'] = iteration
                        heuristic['b_0'] = weights[0]
                        heuristic['b_1'] = weights[1]
                        heuristic['b_2'] = weights[2]
            
            writeResult(f, heuristic['alpha'], heuristic['iteration'], (heuristic['b_0'], heuristic['b_1'], heuristic['b_2']))

    else:
        print('Usage:', sys.argv[0], "input_file, output_file")
        sys.exit(1)

if __name__ == "__main__":
    main()