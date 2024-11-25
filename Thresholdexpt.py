import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm  # For progress bars

# Assume these are given
# function_descriptions: List of function description strings
# function_description_embeddings: np.array of shape (num_functions, embedding_dim)
# validation_utterances: List of validation utterance strings
# validation_utterance_embeddings: np.array of shape (num_validation_utterances, embedding_dim)
# true_function_descriptions: List of indices corresponding to the true function descriptions for each validation utterance

# Example data (You need to replace these with your actual data)
# function_descriptions = ['function1', 'function2', 'function3', ...]
# function_description_embeddings = np.array([...])  # Shape: (num_functions, embedding_dim)
# validation_utterances = ['utterance1', 'utterance2', 'utterance3', ...]
# validation_utterance_embeddings = np.array([...])  # Shape: (num_validation_utterances, embedding_dim)
# true_function_descriptions = [0, 1, 2, ...]  # Indices of the true function descriptions

# Step 1: Compute similarity scores between validation utterances and function descriptions
sim_scores = cosine_similarity(validation_utterance_embeddings, function_description_embeddings)
num_utterances = validation_utterance_embeddings.shape[0]
num_functions = function_description_embeddings.shape[0]

# Step 2: Optimize thresholds for each function description
optimal_thresholds = np.zeros(num_functions)
optimal_f1_scores = np.zeros(num_functions)
thresholds = np.linspace(0, 1, 100)  # Adjust the range and number of thresholds as needed

for j in tqdm(range(num_functions), desc="Optimizing thresholds"):
    # True labels for function description j
    true_labels = np.array([1 if true_function_descriptions[i] == j else 0 for i in range(num_utterances)])
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
    optimal_f1_scores[j] = best_f1

# Step 3: Inference function using the optimal thresholds
def predict_function_description(runtime_utterance_embedding, function_description_embeddings, optimal_thresholds):
    """
    Predicts the function description(s) for a given runtime utterance embedding.
    
    Parameters:
    - runtime_utterance_embedding: np.array of shape (embedding_dim,)
    - function_description_embeddings: np.array of shape (num_functions, embedding_dim)
    - optimal_thresholds: np.array of shape (num_functions,)
    
    Returns:
    - predictions: List of tuples (function_description_index, similarity_score)
    """
    # Compute similarity scores
    scores = cosine_similarity(runtime_utterance_embedding.reshape(1, -1), function_description_embeddings).flatten()
    
    # Compare scores with thresholds
    predictions = []
    for j in range(len(optimal_thresholds)):
        if scores[j] >= optimal_thresholds[j]:
            predictions.append((j, scores[j]))
    
    # Sort predictions by similarity score in descending order
    predictions.sort(key=lambda x: x[1], reverse=True)
    
    return predictions  # Returns a list of function description indices and their scores

# Example usage
# runtime_utterance_embedding = np.array([...])  # Replace with your actual embedding
# predictions = predict_function_description(runtime_utterance_embedding, function_description_embeddings, optimal_thresholds)

# if predictions:
#     for idx, score in predictions:
#         print(f"Predicted Function Description: {function_descriptions[idx]}, Similarity Score: {score}")
# else:
#     print("No function description passed the threshold.")
