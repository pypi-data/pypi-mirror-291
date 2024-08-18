import numpy as np
from numpy.ma.core import ceil
import matplotlib.pyplot as plt
from scipy.spatial import distance

class CSGT:
    def __init__(self, x, y, input_len, sigma=1.0, learning_rate=0.5, norm='L1', decay_function='g', factor=None, random_state=None, metric='euclidean', train_type='hard'):
        self.x = x
        self.y = y
        self.input_len = input_len
        self.sigma = sigma
        self.initial_sigma = sigma
        self.lr = learning_rate
        self.initial_lr = learning_rate
        self.decay_function = decay_function
        self.norm = norm
        self.factor = factor
        self.weight = None
        self.distances = []
        self.train_type = train_type
        self.random_state = random_state
        self.metric = metric
        self.umatrix = None
        self.num_epochs = None
        self.neighbors = None
        self.radius = sigma

    def initialize_weight(self):
        if self.random_state is not None:
            np.random.seed(self.random_state)
        self.weight = np.random.random_sample(size=(self.x, self.y, self.input_len))
        if self.norm == 'L2':
            self.weight /= np.linalg.norm(self.weight, axis=-1, keepdims=True)

    def e_distance(self, x, y):
        return distance.euclidean(x, y)

    def m_distance(self, x, y):
        return distance.cityblock(x, y)

    def calculate_distance(self, p1, p2):
        if self.metric == 'euclidean':
            return distance.euclidean(p1, p2)
        elif self.metric == 'manhattan':
            return distance.cityblock(p1, p2)
        elif self.metric == 'cosine':
            return distance.cosine(p1, p2)

    def bestMatchingNeuron(self, data, t):
        winner = [0, 0]
        shortest_distance = np.Inf
        for row in range(self.x):
            for column in range(self.y):
                dist = self.calculate_distance(self.weight[row, column], data[t])
                if dist < shortest_distance:
                    shortest_distance = dist
                    winner = [row, column]
        return winner

    def decay(self, step):
        t = 1.0 - (np.float64(step) / self.num_epochs)
        if self.decay_function == 'g':
            self.radius = ceil(self.initial_sigma * t)
            return self.initial_lr * t, ceil(t * self.initial_sigma)
        elif self.decay_function == 'e':
            self.radius = ceil(self.initial_sigma * np.exp(-t))
            return self.initial_lr * np.exp(-t), ceil(self.initial_sigma * np.exp(-t))
        elif self.decay_function == 's_e':
            self.radius = ceil(self.initial_sigma * np.exp(-t / self.factor))
            return self.initial_lr * np.exp(-t / self.factor), np.ceil(self.initial_sigma * np.exp(-t / self.factor))
        elif self.decay_function == 'l':
            self.radius = ceil(self.initial_sigma * (1 - t))
            return self.initial_lr * (1 - t), ceil(self.initial_sigma * (1 - t))
        elif self.decay_function == 'i':
            self.radius = ceil(self.initial_sigma / (1 + t))
            return self.initial_lr / (1 + t), ceil(self.initial_sigma / (1 + t))
        elif self.decay_function == 'p':
            self.radius = ceil(self.initial_sigma / (1 + t**self.factor))
            return self.initial_lr / (1 + t**self.factor), ceil(self.initial_sigma / (1 + t**self.factor))

    def train(self, data, epoch, random=True):
        self.num_epochs = epoch
        for i in range(epoch):
            if (i + 1) % 1000 == 0:
                print("Iteration: ", i + 1)
            learning_rate, neighbourhood_range = self.decay(i)
            if not random:
                index = i % data.shape[0]
            else:
                index = np.random.randint(0, high=data.shape[0])
            winner = self.bestMatchingNeuron(data, index)
            for row in range(self.x):
                for column in range(self.y):
                    if self.train_type == 'gaussian':
                        dist = np.linalg.norm(np.array([row, column]) - np.array(winner))
                        influence = np.exp(-dist**2 / (2 * neighbourhood_range**2))
                        self.weight[row, column] += influence * learning_rate * (data[index] - self.weight[row, column])
                    elif self.train_type == 'hard':
                        if self.m_distance([row, column], winner) <= neighbourhood_range:
                            self.weight[row, column] += learning_rate * (data[index] - self.weight[row, column])
                    elif self.train_type == 'comb':
                        grid_distance = np.linalg.norm(np.array([row, column]) - np.array(winner))
                        if grid_distance <= neighbourhood_range:
                            influence = np.exp(-grid_distance**2 / (2 * neighbourhood_range**2))
                            self.weight[row, column] += influence * learning_rate * (data - self.weight[row, column])
        print('SOM Model Training Completed')

    def get_neighbors(self, i, j):
        self.neighbors = []
        for x in range(max(i - int(self.radius), 0), min(i + int(self.radius) + 1, self.x)):
            for y in range(max(j - int(self.radius), 0), min(j + int(self.radius) + 1, self.y)):
                self.neighbors.append((x, y))
        return self.neighbors

    def plot_hit_map(self, data):
        hit_map = np.zeros((self.x, self.y))
        for i in range(data.shape[0]):
            winner = self.bestMatchingNeuron(data, i)
            hit_map[winner[0], winner[1]] += 1
        plt.figure(figsize=(10, 8))
        plt.title('Hit Map')
        plt.imshow(hit_map.T, cmap='Blues', interpolation='nearest')
        plt.colorbar()
        plt.show()

    def distance_map(self, data):
        u_matrix = np.zeros(shape=(self.x, self.y), dtype=np.float64)
        map_weights = self.weight
        for i in range(self.x):
            for j in range(self.y):
                v = map_weights[i][j]
                sum_dists = 0.0
                ct = 0
                if i - 1 >= 0:    # above
                    sum_dists += self.e_distance(v, map_weights[i - 1][j])
                    ct += 1
                if i + 1 <= self.x - 1:   # below
                    sum_dists += self.e_distance(v, map_weights[i + 1][j])
                    ct += 1
                if j - 1 >= 0:   # left
                    sum_dists += self.e_distance(v, map_weights[i][j - 1])
                    ct += 1
                if j + 1 <= self.y - 1:   # right
                    sum_dists += self.e_distance(v, map_weights[i][j + 1])
                    ct += 1
                u_matrix[i][j] = sum_dists / ct
        u_matrix_normalized = (u_matrix - np.min(u_matrix)) / (np.max(u_matrix) - np.min(u_matrix))

        # Plot the U-matrix
        self.umatrix = u_matrix_normalized
        return self.umatrix

    def plot_u_matrix(self, data):
        self.umatrix = self.distance_map(data)
        plt.figure(figsize=(10, 8))
        plt.title('U-Matrix')
        plt.imshow(self.umatrix.T, cmap='Blues', interpolation='nearest')
        plt.show()

    def quantization_error(self, data):
        total_error = 0
        for i in range(data.shape[0]):
            bmu = self.bestMatchingNeuron(data, i)
            bmu_weight = self.weight[bmu[0], bmu[1]]
            total_error += np.linalg.norm(data[i] - bmu_weight)
        return total_error / len(data)

    def topographic_error(self, data):
        error_count = 0
        for sample in data:
            bmu1, bmu2 = self.find_two_best_matching_neurons(sample)
            if not self.are_adjacent(bmu1, bmu2):
                error_count += 1
        return error_count / len(data)

    def find_two_best_matching_neurons(self, sample):
        distances = np.array([[np.linalg.norm(neuron - sample) for neuron in row] for row in self.weight])
        bmu1 = np.unravel_index(np.argmin(distances), distances.shape)
        distances[bmu1] = np.inf
        bmu2 = np.unravel_index(np.argmin(distances), distances.shape)
        return bmu1, bmu2

    def are_adjacent(self, bmu1, bmu2):
        return np.linalg.norm(np.array(bmu1) - np.array(bmu2)) <= 1

    def win_map(self, data):
        wm = {}
        for i in range(data.shape[0]):
            bmu = self.bestMatchingNeuron(data, i)
            bmu_tuple = (bmu[0], bmu[1])
            if bmu_tuple in wm:
                wm[bmu_tuple].append(data[i])
            else:
                wm[bmu_tuple] = [data[i]]
        return wm

    def get_data_points_for_neuron(self, data, neuron_x, neuron_y):
        wm = self.win_map(data)
        neuron_index = (neuron_x, neuron_y)
        if neuron_index in wm:
            return wm[neuron_index]
        else:
            return []  # No data points for this neuron