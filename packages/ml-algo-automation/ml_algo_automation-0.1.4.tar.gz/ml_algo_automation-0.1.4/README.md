# ML Automation

`ml_algo_automation` is a Python library that allows you to compare multiple machine learning models for both regression and classification tasks, using scikit-learn. It evaluates models based on various metrics and selects the best one according to the specified criterion.

## Features

- Compare multiple regression models (Linear Regression, Decision Tree, Random Forest, etc.)
- Compare multiple classification models (Logistic Regression, SVM, Random Forest, etc.)
- Select the best model based on metrics like R² Score, Accuracy, Precision, Recall, etc.

## Installation

You can install the package via pip:

```bash
pip install ml-algo-automation
```


## Usage

###Regression Example

```python
from ml_algo_automation.ml_model_comparator import a_b_testing_regression, get_best_model, get_model_results
from sklearn.datasets import load_diabetes

# Load the diabetes dataset
data = load_diabetes()
X, y = data.data, data.target

# Run the regression testing function
models, results = a_b_testing_regression(X, y)

# Find the best model based on R² Score
best_model_name = get_best_model(results, metric="R² Score")
print(f"\nThe best model based on R² Score is: {best_model_name} with an R² Score of {results[best_model_name]['R² Score']:.4f}\n")

# Print all model results
get_model_results(results)
```

###Classification Example

```python
from ml_algo_automation.ml_model_comparator import a_b_testing_classification, get_best_model, get_model_results
from sklearn.datasets import load_wine

# Load a sample dataset
data = load_wine()
X, y = data.data, data.target

# Run the classification testing function
models, results = a_b_testing_classification(X, y)

# Find the best model based on Precision
best_model_name = get_best_model(results, metric="Precision")
print(f"\nThe best model based on Precision is: {best_model_name} with a Precision of {results[best_model_name]['Precision']:.4f}\n")

# Print all model results
get_model_results(results)

```

