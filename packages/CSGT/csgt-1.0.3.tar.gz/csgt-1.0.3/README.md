# CSGT - Cluster-Sort-Gradient-Tuning

**CSGT** (Cluster-Sort-Gradient-Tuning) is a robust Python library designed for implementing Self-Organizing Maps (SOMs), a type of unsupervised learning algorithm that uses competitive learning to perform dimensionality reduction and data clustering. The library focuses on gradient-based optimization techniques, providing advanced features for data visualization and analysis through U-Matrix and hit maps, along with error quantification metrics like quantization and topographic errors.

## Key Features

- **Self-Organizing Map (SOM) Implementation**: Train SOMs with customizable grid size, learning rate, neighborhood function, and training algorithms.
- **Gradient-Based Optimization**: Dynamic learning rate and neighborhood size adjustment using various decay functions, allowing flexible control over model convergence.
- **Distance Metrics**: Support multiple distance metrics including Euclidean, Manhattan (L1), and Cosine distances for neuron weight updates and winner selection.
- **Error Metrics**: Calculating quantization and topographic errors to assess the performance and quality of the SOM.
- **Visualization Tools**: Generation of U-Matrix and hit maps to visually interpret and evaluate the SOM, helping to identify data clusters and relationships.

## Installation

You can install the package directly from PyPI:

```bash
pip install CSGT
```

## Getting Started

### Importing the Library
```bash
from CSGT import CSGT
import numpy as np
```
### Initializing the CSGO Model
```bash
# Sample data
data = np.random.random((100, 3))

# Initialize the CSGO model with a 10x10 grid and 3-dimensional input data
model = CSGT(x=10, y=10, input_len=3)
```
### Training the Model
```bash
# Train the SOM with 10,000 epochs
model.train(data, epoch=10000)
```
### Visualizing the U-Matrix
```bash
# Plot the U-Matrix to visualize the topological relationships of the neurons
model.plot_u_matrix(data)
```
### Visualizing the Hit Map
```bash
# Plot the hit map to visualize neuron activation frequencies
model.plot_hit_map(data)
```
## CSGT Class and Methods
### Initialization: CSGO.__init__()
```bash
CSGT(x, y, input_len, sigma=1.0, learning_rate=0.5, norm='L1', decay_function='g', factor=None, random_state=None, metric='euclidean', train_type='hard')
```
#### Parameters:
1. `x, y`: Dimensions of the SOM grid.
2. `input_len`: Length of the input vectors.
3. `sigma`: Initial neighborhood radius, controlling the spread of the influence of the BMU.
4. `learning_rate`: Initial learning rate for updating the neurons' weights.
5. `norm`: Normalization type for neuron weights ('L1' or 'L2').
6. `decay_function`: Function to decay learning rate and neighborhood radius. Options:
   - ``g``: Linear decay (Default)
   - ``e``: Exponential decay
   - ``s_e``: Scaled exponential decay
   - ``l``: Linear decay with a different formulation
   - ``i``: Inverse decay
   - ``p``: Polynomial decay
8. `factor`: Additional factor for the decay function (used in 's_e' and 'p' decay).
9. `random_state`: Seed for random number generation, ensuring reproducibility.
10. `metric`: Distance metric to calculate distances between input vectors and neuron weights ('euclidean', 'manhattan', or 'cosine').
11. `train_type`: Type of neighborhood function to be used during training. Options:
    - ``hard``: Quantized neighborhood function.
    - ``gaussian``: Gaussian neighborhood function.
    - ``comb``: Combination of hard and Gaussian functions.

### Weight Initialization: CSGT.initialize_weight()
Initializes the neuron weight vectors based on the input length and normalization type.

### Distance Calculation: CSGT.calculate_distance()
Calculates the distance between two vectors using the specified metric.

### Best Matching Unit (BMU): CSGT.bestMatchingNeuron()
Identifies the neuron on the grid that best matches the current input vector based on the minimum distance.

### Decay Function: CSGT.decay()
Applies the selected decay function to adjust the learning rate and neighborhood radius over time.

### Training the SOM: CSGT.train()
Trains the SOM over a specified number of epochs, adjusting neuron weights based on the input data.

### U-Matrix Calculation: CSGT.distance_map()
Generates the U-Matrix, a matrix that visualizes the distances between the neuron weights, helping to identify clusters and topological structures.

### Plotting the U-Matrix: CSGT.plot_u_matrix()
Displays the U-Matrix using a heatmap to represent the distances between neighboring neurons.

### Plotting the Hit Map: CSGT.plot_hit_map()
Generates and displays a hit map that shows how frequently each neuron has been the BMU for the input vectors.

### Quantization Error: CSGT.quantization_error()
Calculates the quantization error, which measures the average distance between the input vectors and their corresponding BMUs. Lower quantization errors indicate a better fit of the SOM to the input data.

### Topographic Error: CSGT.topographic_error()
Calculates the topographic error, which measures the proportion of input vectors for which the first and second BMUs are not adjacent. Lower topographic errors indicate a better preservation of the input data topology.

### Winning Neuron Map: CSGT.win_map()
Returns a map of neurons with the corresponding input vectors that each neuron has won during training.

### Neighbor Retrieval: CSGT.get_neighbors()
Returns the list of neighbors for a specified neuron based on the current neighborhood radius.

## Mathematical Background
### Self-Organizing Maps (SOM)
SOMs are a type of artificial neural network introduced by Teuvo Kohonen in the 1980s. They use competitive learning to project high-dimensional data onto a lower-dimensional (usually 2D) grid, preserving the topological relationships of the input data. Each neuron in the SOM corresponds to a weight vector, and during training, the neurons compete to be the best matching unit (BMU) for each input vector. The BMU and its neighboring neurons have their weights updated to become more similar to the input vector.

### Quantization Error
Quantization error is a crucial metric in evaluating SOMs. It quantifies the error introduced when representing high-dimensional data using the discrete grid of neurons in the SOM. Mathematically, it is defined as the average Euclidean distance between the input vectors and their BMUs.

### U-Matrix
The U-Matrix (Unified Distance Matrix) is a visualization tool used in SOMs to represent the distances between neighboring neurons. It helps in identifying clusters and understanding the topological structure of the SOM.

## Example Use Cases
Clustering: Grouping high-dimensional data into clusters for pattern recognition and data analysis.
Dimensionality Reduction: Projecting high-dimensional data onto a 2D grid while preserving the relationships among data points.
Visualization: Understanding and interpreting the structure and relationships in complex datasets through U-Matrix and hit maps.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

# Author
- Manav Gupta
- Email: manav26102002@gmail.com
