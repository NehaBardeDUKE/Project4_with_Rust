import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

# Assume these are given
# df: DataFrame with columns ['utterance', 'ground_truth_function_description']
# db_description_embeddings: List of function description embeddings (list of np.array)

# Example:
# df = pd.DataFrame({'utterance': ['utterance1', 'utterance2', ...],
#                    'ground_truth_function_description': ['function1', 'function2', ...]})
# db_description_embeddings = [np.array([...]), np.array([...]), ...]

# Step 1: Prepare Data
utterance_embeddings = np.array([embedding_function(utt) for utt in df['utterance']])  # Replace embedding_function with your encoding function
ground_truth_indices = [function_description_to_index(desc) for desc in df['ground_truth_function_description']]  # Map descriptions to indices

# Convert db_description_embeddings to a single numpy array
db_description_embeddings = np.array(db_description_embeddings)
num_functions = db_description_embeddings.shape[0]

# Step 2: Compute similarity scores
sim_scores = cosine_similarity(utterance_embeddings, db_description_embeddings)
num_utterances = utterance_embeddings.shape[0]

# Step 3: Optimize thresholds for each function description
optimal_thresholds = np.zeros(num_functions)
thresholds = np.linspace(0, 1, 100)  # Adjust as needed

for j in tqdm(range(num_functions), desc="Optimizing thresholds"):
    # True labels for function description j
    true_labels = np.array([1 if ground_truth_indices[i] == j else 0 for i in range(num_utterances)])
    scores = sim_scores[:, j]

    best_f1 = 0
    best_threshold = 0

    for t in thresholds:
        predicted_labels = (scores >= t).astype(int)

        TP = np.sum((predicted_labels == 1) & (true_labels == 1))
        FP = np.sum((predicted_labels == 1) & (true_labels == 0))
        FN = np.sum((predicted_labels == 0) & (true_labels == 1))

        if TP + FP == 0 or TP + FN == 0:
            f1 = 0
        else:
            precision = TP / (TP + FP)
            recall = TP / (TP + FN)
            if precision + recall == 0:
                f1 = 0
            else:
                f1 = 2 * precision * recall / (precision + recall)

        if f1 > best_f1:
            best_f1 = f1
            best_threshold = t

    optimal_thresholds[j] = best_threshold

# Step 4: Create the final zip of (description_embedding, threshold)
result = list(zip(db_description_embeddings, optimal_thresholds))

# Output
print("Thresholds optimized for all function descriptions.")
