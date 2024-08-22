from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVR, SVC
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
import numpy as np

# Regression Function
def a_b_testing_regression(X, y, test_size=0.2, random_state=42):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Define the regression models to evaluate
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree Regressor": DecisionTreeRegressor(random_state=random_state),
        "Random Forest Regressor": RandomForestRegressor(random_state=random_state),
        "Gradient Boosting Regressor": GradientBoostingRegressor(random_state=random_state),
        "Support Vector Regressor": SVR(),
        "K-Neighbors Regressor": KNeighborsRegressor()
    }

    # Dictionary to store the model performance
    results = {}

    # Iterate over each model, fit it, and evaluate its performance
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results[name] = {
            "Mean Squared Error": mse,
            "R² Score": r2
        }

    return models, results

# Classification Function
def a_b_testing_classification(X, y, test_size=0.2, random_state=42):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Define the classification models to evaluate
    models = {
        "Logistic Regression": LogisticRegression(max_iter=200),
        "Decision Tree Classifier": DecisionTreeClassifier(random_state=random_state),
        "Random Forest Classifier": RandomForestClassifier(random_state=random_state),
        "Gradient Boosting Classifier": GradientBoostingClassifier(random_state=random_state),
        "Support Vector Classifier": SVC(),
        "K-Neighbors Classifier": KNeighborsClassifier()
    }

    # Dictionary to store the model performance
    results = {}

    # Iterate over each model, fit it, and evaluate its performance
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # Evaluate the model using different metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        results[name] = {
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1
        }

    return models, results

# Function to get the best model based on a chosen metric
def get_best_model(results, metric="R² Score"):
    """Retrieve the best model based on a specified metric."""
    if metric in ["R² Score", "Mean Squared Error", "Accuracy", "Precision", "Recall", "F1 Score"]:
        best_model_name = max(results, key=lambda x: results[x][metric] if metric != "Mean Squared Error" else -results[x][metric])
    else:
        raise ValueError("Unsupported metric. Use 'R² Score', 'Mean Squared Error', 'Accuracy', 'Precision', 'Recall', or 'F1 Score'.")
    
    return best_model_name

# Function to print model results
def get_model_results(results):
    """Print the results for each model."""
    for model_name, metrics in results.items():
        metric_str = ', '.join([f"{k} = {v:.4f}" for k, v in metrics.items()])
        print(f"{model_name}: {metric_str}")


