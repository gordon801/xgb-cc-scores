# XGBoost Modelling - Credit Card Scores
In this project, I used provided LendingClub data and the output from an XGBoost model to produce XGB prediction scores for each observation in the LendingClub dataset.

## Inputs
* creditcard_3001.csv: LendingClub credit card data with 3001 observations. 
![image](https://user-images.githubusercontent.com/62014067/127531644-d90f252a-5ba5-4825-bbdf-37da382c146f.png)

* xgb_tree_1000.txt: Text file dump from an XGBoost model containing 1000 ensemble trees.
![image](https://user-images.githubusercontent.com/62014067/127531730-fe5ca4e2-a692-46ce-91fe-4527a6fdcc82.png)

## Program
* xgboost_process.py

This program parses the input files, creates binary trees from the xgb_tree data, and defines a traversal algorithm. To obtain the overall prediction score for a particular observation, it sums the individual prediction scores from traversing each of the 1000 ensemble trees. It repeats this process for each of the 3001 observations and outputs the resultant prediction scores to 'test_result.csv'.

## Output
* test_result.csv: List of 3001 prediction scores corresponding to each LendingClub observation.

![image](https://user-images.githubusercontent.com/62014067/127531985-eb0ec91b-3c46-4305-b49c-094a12f8e0dd.png)
