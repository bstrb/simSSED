import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Load your data
csv_path = f"/Users/xiaodong/Desktop/UOXsim-2/combined_metrics_IQM_SUM_10_10_10_-10_10_-10_10_10_-10.csv"

df = pd.read_csv(csv_path)

# Group by event_number and get the minimum combined_metric for each event.
# This preserves the event_number as the index.
grouped_series = df.groupby("event_number")["combined_metric"].min()

# Reshape the values for clustering (each value in its own row)
grouped_values = grouped_series.values.reshape(-1, 1)

# Apply K-Means with 2 clusters
kmeans = KMeans(n_clusters=2, random_state=0)
kmeans.fit(grouped_values)
labels = kmeans.labels_
centers = kmeans.cluster_centers_.flatten()

# Since lower combined_metric is better, we want to flag the cluster with the higher center.
# The cluster with the higher center (worse metrics) is the one to cut off.
cutoff_label = np.argmax(centers)

# Compute a cutoff threshold as the mean of the two centers.
# This threshold is a rough boundary between the clusters.
sorted_centers = np.sort(centers)
cutoff = np.mean(sorted_centers)
print(f"Optimal cutoff determined by K-Means: {cutoff:.4f}")

# Identify the event numbers that belong to the "cut off" cluster (i.e. those with higher combined_metric)
cutoff_events = grouped_series[labels == cutoff_label].index.tolist()
print("Event numbers to be cut off:")
print(cutoff_events)

# Plot the histogram with the cutoff threshold indicated
plt.figure(figsize=(10, 6))
plt.hist(grouped_values, bins=100, edgecolor='black', alpha=0.6, label='Data')
plt.axvline(cutoff, color='red', linestyle='dashed', linewidth=2, label=f'Cutoff = {cutoff:.2f}')
plt.title("Histogram with K-Means Cutoff")
plt.xlabel("Combined Metric")
plt.ylabel("Frequency")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
