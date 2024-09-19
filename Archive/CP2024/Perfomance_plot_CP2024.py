import sys
sys.path.append('.')
import subprocess
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

# Load data
data = pd.read_csv('./experiments/data.csv')

# Create scatter plot
plt.figure(figsize=(14, 10))
plt.scatter(data['SpecName'], data['NewSpec'], label='NewSpec', color='darkgreen', marker='o')
plt.scatter(data['SpecName'], data['OldSpec'], label='OldSpec', color='darkblue', marker='o')
plt.scatter(data['SpecName'], data['OldTimeOut'], label='OldTimeOut', color='red', marker='o')
plt.scatter(data['SpecName'], data['BothTimeOut'], label='BothTimeOut', color='darkgoldenrod', marker='o')

# Set y-axis to log scale
plt.yscale('log')

# Add labels and title
plt.xlabel('SpecNames')
plt.ylabel('time(s)')
plt.title('Time Comparison Across Specifications')
plt.legend()

# Select a subset of SpecNames for clarity on x-axis
subset_spacing = len(data['SpecName']) // 25  # show only 10% of the labels to avoid overlap
plt.xticks(data['SpecName'][::subset_spacing], rotation=30, fontsize=8)

# Turn off gridlines
plt.grid(False)

# Save plot as SVG
plt.tight_layout()
plt.savefig('./experiments/performance_scatter_plot.svg', format='svg')

plt.show()
