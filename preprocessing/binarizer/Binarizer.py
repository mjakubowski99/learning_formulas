import numpy as np
class Binarizer:

    def binarize(self, value, bits):
        arr = np.zeros(bits).astype(np.int8)
        if value >= len(arr):
            arr[len(arr)-1] = 1
        else:
            arr[value] = 1
        return arr 

    def fit_transform(self, values, max):
        bits = max+1
        return np.array([self.binarize(value,bits) for value in values])