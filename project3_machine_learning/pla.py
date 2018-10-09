import numpy as np
import matplotlib.pyplot as plt
import math
import sys

def converge(xn, N, weights):
    misclassified_indices = []
    for i in range(N):
        if not np.sign(np.dot(weights, [xn[i][0], xn[i][1], 1])):
            sign = -1
        else:
            sign = np.sign(np.dot(weights, [xn[i][0], xn[i][1], 1]))
    
        if sign != xn[i][-1]:
            misclassified_indices.append(i)
    
    if not misclassified_indices:
        return True, misclassified_indices
    else:
        return False, misclassified_indices

def main():
    if len(sys.argv) == 3:
        input_file_name = sys.argv[1]
        output_file_name = sys.argv[2]

        xn = []

        with open(input_file_name, mode='r') as f:
            lines = f.read().splitlines()
            for line in lines:
                xn.append([int(val) for val in line.split(',')])
                
        # PLA(perceptron learning algorithm)
        weights = np.zeros(3)
        misclassified_indices = list(range(len(xn)))
        pla_over = False
        with open(output_file_name, mode='w') as f:
            while not pla_over:
                rand_x = xn[np.random.choice(misclassified_indices)]
                
                if not np.sign(np.dot(weights, [rand_x[0], rand_x[1], 1])):
                    sign = -1
                else:
                    sign = np.sign(np.dot(weights, [rand_x[0], rand_x[1], 1]))
                
                if sign != rand_x[-1]:
                    weights += np.dot(rand_x[-1], [rand_x[0], rand_x[1], 1])# update weight, w <- w + yx
                    f.write(str(weights[0]) + ',' + str(weights[1]) + ',' + str(weights[2]))
                    f.write('\n')

                pla_over, misclassified_indices = converge(xn, len(xn), weights)

        # plot xn, and approximate function with weights learned
        plot_x1_plus1, plot_x2_plus1, plot_x1_minus1, plot_x2_minus1 = [], [], [], []
        
        for i in range(len(xn)):
            if xn[i][-1] == 1:
                plot_x1_plus1.append(xn[i][0])
                plot_x2_plus1.append(xn[i][1])
            elif xn[i][-1] == -1:
                plot_x1_minus1.append(xn[i][0])
                plot_x2_minus1.append(xn[i][1])

        plt.scatter(plot_x1_plus1, plot_x2_plus1, c='b') # all +1 points
        plt.scatter(plot_x1_minus1, plot_x2_minus1, c='r') # all -1 points
        plt.plot([0, -weights[2]/weights[0]], [-weights[2]/weights[1], 0]) # line to separate +1/-1 points
        plt.show()
    else:
        print('Usage:', sys.argv[0], "input_file, output_file")
        sys.exit(1)
            
    
if __name__ == "__main__":
    main()