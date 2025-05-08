import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# Load gene expression data
data_url = "https://raw.githubusercontent.com/pine-bio-support/omicslogic/master/PDX_HTSeq_gene_expression.txt"
data = pd.read_csv(data_url, sep="\t", index_col=0)

# Remove genes with all zero expression
data = data.loc[data.sum(axis=1) != 0]

# Extract sample names
names_pdx = data.columns.tolist()

# Define phenotypic classes (adjust based on dataset)
meta_classes = ["ER"] * 7 + ["TN"] * 7  # Modify if dataset size differs

# Create metadata DataFrame
meta_data = pd.DataFrame({"Sample": names_pdx, "Class": meta_classes})
meta_data.set_index("Sample", inplace=True)

# Extract gene expression matrix and labels
X = data.T.values  # Transpose to have samples as rows
y = meta_data.loc[data.columns, "Class"].values  # Match class labels

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Standardize data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Perform Linear Discriminant Analysis (LDA)
lda = LinearDiscriminantAnalysis()
lda.fit(X_train, y_train)

# Predict on test set
y_pred = lda.predict(X_test)

# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
print(classification_report(y_test, y_pred))

# Transform data into LDA space
X_train_lda = lda.transform(X_train)
X_test_lda = lda.transform(X_test)

# Save transformed data
np.savetxt("X_train_lda.csv", X_train_lda, delimiter=",")
np.savetxt("X_test_lda.csv", X_test_lda, delimiter=",")

# Plot LDA projection
plt.figure(figsize=(8, 6))
sns.scatterplot(x=X_train_lda[:, 0], y=X_train_lda[:, 1], hue=y_train, palette="coolwarm", alpha=0.8)
plt.xlabel("LDA Component 1")
plt.ylabel("LDA Component 2")
plt.title("LDA Projection of Training Data")
plt.legend(title="Class")
plt.grid(True)
plt.show()

# Plot explained variance
plt.figure(figsize=(6, 4))
explained_var_ratio = lda.explained_variance_ratio_
plt.bar(range(1, len(explained_var_ratio) + 1), explained_var_ratio, alpha=0.7)
plt.xlabel("LDA Component")
plt.ylabel("Explained Variance Ratio")
plt.title("Explained Variance by LDA Components")
plt.show()