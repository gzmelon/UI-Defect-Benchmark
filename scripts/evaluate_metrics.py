import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from scipy.stats import pearsonr

def evaluate_defect_classification(y_true, y_pred, class_names=None):
    """
    Calculates standard Machine Learning metrics for UI defect classification.
    """
    acc = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    
    metrics = {
        "Accuracy": round(acc, 4),
        "Precision": round(precision, 4),
        "Recall": round(recall, 4),
        "F1-Score": round(f1, 4)
    }
    return metrics

def evaluate_human_alignment(human_expert_scores, model_confidence_scores):
    """
    Calculates the Pearson Correlation Coefficient between the CM-GAT model's 
    predicted severity scores and the ground-truth scores provided by 50 UX experts.
    """
    correlation, p_value = pearsonr(human_expert_scores, model_confidence_scores)
    
    alignment_metrics = {
        "Pearson_Correlation (r)": round(correlation, 4),
        "P-value": "{:.2e}".format(p_value),
        "Significance": "Highly Significant (p < 0.01)" if p_value < 0.01 else "Not Significant"
    }
    return alignment_metrics

if __name__ == "__main__":
    print("="*50)
    print(" Figma-Defect-3.5K: Evaluation Metrics Script")
    print("="*50)

    # ---------------------------------------------------------
    # Mock Data: Simulating model outputs for demonstration
    # Classes: 0: Normal, 1: CSS Occlusion, 2: Misalignment, 3: Contrast
    # ---------------------------------------------------------
    y_true_mock = np.array([1, 0, 2, 1, 3, 0, 1, 2, 2, 1])
    y_pred_mock = np.array([1, 0, 2, 0, 3, 0, 1, 2, 1, 1])
    
    print("\n[1] Sub-task: UI Defect Classification Performance")
    clf_metrics = evaluate_defect_classification(y_true_mock, y_pred_mock)
    for k, v in clf_metrics.items():
        print(f"    - {k}: {v}")

    # ---------------------------------------------------------
    # Mock Data: Simulating UX Expert Scores vs Model Scores (1.0 to 5.0 scale)
    # ---------------------------------------------------------
    human_scores = np.array([4.8, 1.2, 3.5, 4.0, 4.9, 1.0, 4.5, 3.8, 3.9, 4.2])
    model_scores = np.array([4.5, 1.5, 3.2, 3.8, 4.7, 1.1, 4.6, 3.5, 3.4, 4.0])

    print("\n[2] Sub-task: Human-Model Alignment (UX Expert Validation)")
    align_metrics = evaluate_human_alignment(human_scores, model_scores)
    for k, v in align_metrics.items():
        print(f"    - {k}: {v}")
    
    print("\nEvaluation completed successfully.")
