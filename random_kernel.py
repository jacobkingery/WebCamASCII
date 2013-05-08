from random import randint
import numpy as np

def random_kernel(n, max, value):
    kernel = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            kernel[i][j] = randint(-max, max)
    kernel[n/2][n/2] = -np.sum(kernel) + kernel[n/2][n/2] +value
    return kernel.tolist()

if __name__ == '__main__':
    print random_kernel(3, 1, 0)
