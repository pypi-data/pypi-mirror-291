Weighted meaN oF vectOrs (INFO) Optimization Algorithm
This repository contains the implementation of INFO, a novel population-based optimization algorithm designed for solving complex optimization problems. INFO leverages a modified weighted mean approach to efficiently explore the search space and converge towards optimal solutions.

Algorithm Description
INFO distinguishes itself from conventional optimization methods through its unique three-stage process:

Updating Rule: Employs a mean-based law and convergence acceleration techniques to generate new candidate solutions (vectors) with enhanced exploration capabilities.

Vector Combining: Combines the newly generated vectors from the updating rule stage to create a promising solution, striking a balance between exploration and exploitation.

Local Search: Refines the solution obtained from the vector combining stage by conducting a local search, further improving exploitation and helping the algorithm escape local optima.

Key Features
Effective Exploration and Exploitation: The algorithm's design carefully balances exploration (searching new areas of the solution space) and exploitation (refining promising solutions) to efficiently find global optima.
Robust Performance: INFO has been rigorously tested on 48 mathematical benchmark functions and 5 constrained engineering problems, demonstrating superior performance compared to existing optimization algorithms.
High Accuracy: INFO consistently achieves high accuracy, converging to within 0.99% of the global optimum in engineering test cases, as evidenced by comparative studies.
Applications
The INFO algorithm holds significant promise for a wide range of optimization problems, including:

Engineering Design: Structural optimization, parameter tuning, and system identification.
Machine Learning: Hyperparameter optimization, feature selection, and neural network training.
Operations Research: Scheduling, resource allocation, and logistics optimization.
Contents
info.py: Python implementation of the INFO algorithm.
test_functions.py: Collection of benchmark test functions for evaluating optimization algorithms.
engineering_problems.py: Definitions of constrained engineering optimization problems.
example.py: Example script demonstrating the usage of the INFO algorithm.
Getting Started
Clone this repository.
Install the required dependencies (NumPy, SciPy).
Run the example.py script to see INFO in action.
Citation
If you use INFO in your research or applications, please cite the following paper:

Ahmadianfar, I., Heidari, A. A., Noshadian, S., Chen, H., & Gandomi, A. H. (2022). INFO: An efficient optimization algorithm based on weighted mean of vectors. Expert Systems with Applications, 195, 116516.

License
This project is licensed under the MIT License.

Feel free to contribute to the development of INFO by reporting issues, suggesting improvements, or submitting pull requests.