# ML Automation

`ml_automation_algo` is a Python library that allows you to compare multiple machine learning models for both regression and classification tasks, using scikit-learn. It evaluates models based on various metrics and selects the best one according to the specified criterion.

## Features
- Compare multiple regression models (Linear Regression, Decision Tree, Random Forest, etc.)
- Compare multiple classification models (Logistic Regression, SVM, Random Forest, etc.)
- Select the best model based on metrics like R² Score, Accuracy, Precision, Recall, etc.

## Installation
Clone the repository and use the following command to install the dependencies:

pip install -r requirements.txt


## Usage
Here’s a basic example:

```python
from ml_model_comparator import a_b_testing_classification, get_best_model, get_model_results
from sklearn.datasets import load_wine

data = load_wine()
X, y = data.data, data.target

models, results = a_b_testing_classification(X, y)
best_model_name = get_best_model(results, metric="Precision")
print(f"The best model based on Precision is: {best_model_name}")
get_model_results(results)
```
