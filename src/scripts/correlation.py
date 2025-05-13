import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Example data: actual vs predicted
real = np.array([1, 2, 3, 4, 5])
pred = np.array([1.2, 2.1, 2.9, 4.05, 5.1])

# Compute Pearson correlation
r, p = pearsonr(real, pred)
r_rounded = round(r, 3)

# Plotting the data
plt.figure(figsize=(6, 4))
plt.scatter(real, pred, color='blue', label='Data Points')
plt.plot(real, real, color='gray', linestyle='--', label='Ideal Fit (y = x)')
plt.title(f'Predicted vs Real Values\nPearson r = {r_rounded}')
plt.xlabel('Real Values')
plt.ylabel('Predicted Values')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
