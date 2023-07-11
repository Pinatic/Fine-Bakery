# Stress test Calculator

The `calculate_and_save_euclidean_distances` script calculates the Euclidean distances between ingredient embeddings and saves the results to an output file. This README file provides instructions on how to use the script.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3.x installed on your system.
- Required dependencies: `numpy` and `scikit-learn`.

You can install the dependencies by running the following command:


pip install numpy scikit-learn


## Usage

To use the `calculate_and_save_euclidean_distances` script, follow these steps:

1. Place the ingredient embedding files in the specified locations:

   - Ensure that the embedding files are in the pickle format (`*.pkl`).
   - Update the `embedding_files` list in the script to include the file paths of your ingredient embeddings.

2. Specify the output file path:

   - Update the `output_file` variable in the script to specify the desired output file path.
   - The output file will contain the calculated execution times for each embedding file.

3. Run the script:

   python stress test.py


4. Check the output:

   - The script will calculate the Euclidean distances and measure the execution time for each embedding file.
   - The execution times for each embedding file will be saved in the output file.

## Stress Test Results

During the execution of the script, the calculated execution times for each embedding file will be displayed as output. Here are the execution times for the stress test:

```
Execution times in stress test:
pre computing distance for Graph 1: 3.4829177856445312 seconds
pre computing distance for Graph 2: 3.3550143241882324 seconds
pre computing distance for Graph 3: 5.896399974822998 seconds
pre computing distance for Graph 4: 5.92773962020874 seconds
```

Please note that the execution times may vary depending on your system's performance and the size of the ingredient embeddings.

## Conclusion

The `stress test` script provides a convenient way to calculate the Euclidean distances between ingredient embeddings and save the results. 