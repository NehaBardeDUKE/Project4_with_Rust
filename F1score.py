import pandas as pd
from sklearn.metrics import f1_score

# Example dataframe
data = {
    'ground_truth': [['apple', 'orchards'], ['banana'], ['grape', 'pear']],
    'predictions': [['apple', 'oranges', 'orchards'], ['banana', 'kiwi'], ['pear']]
}
df = pd.DataFrame(data)

# Function to calculate row-level F1 score
def calculate_f1_score(row):
    ground_truth = set(row['ground_truth'])
    predictions = set(row['predictions'])
    if len(ground_truth) == 0:  # Handle edge case with empty ground truth
        return 1.0 if len(predictions) == 0 else 0.0
    tp = len(ground_truth & predictions)
    precision = tp / len(predictions) if len(predictions) > 0 else 0
    recall = tp / len(ground_truth)
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

# Apply the function to each row
df['f1_score'] = df.apply(calculate_f1_score, axis=1)

# Calculate overall F1 score
overall_f1_score = df['f1_score'].mean()

print("Per-row F1 Scores:")
print(df)
print(f"Overall F1 Score: {overall_f1_score}")
