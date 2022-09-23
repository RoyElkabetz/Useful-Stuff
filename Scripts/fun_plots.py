import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({"font.size": 20})

a = [3, 5]
b = [5, 3]
n = len(a)
dt = 1e-5
dx = 1e-3
tt = np.linspace(0, 1, int(1 / dt))
xx = np.linspace(0, 1, int(1 / dx))

B_a_b = []
beta_dist = []
error = []
stds = [0.04, 0.04]

labels = ["movement", "cognition"]
for i in range(n):
    B_a_b.append(np.sum(np.power(tt, a[i] - 1) * np.power(1 - tt, b[i] - 1)) * dt)
    beta_dist.append(np.power(xx, a[i] - 1) * np.power(1 - xx, b[i] - 1) / B_a_b[i])

    gaussian_error = 1 / np.sqrt(2 * np.pi * 0.5) * np.exp(-(xx - xx[np.argmax(beta_dist[i])]) ** 2 / stds[i])
    error.append(gaussian_error)

sum_betas = beta_dist[0] + beta_dist[1]
plt.figure(figsize=(15, 8))
for i in range(n):
    plt.plot(xx, beta_dist[i], label=labels[i])
    plt.fill_between(xx, beta_dist[i] - error[i], beta_dist[i] + error[i], alpha=0.3)
plt.vlines(xx[np.argmax(sum_betas)], 0, beta_dist[0][np.argmax(sum_betas)], linestyle='--', color="red",
           label="global\noptimum")
plt.xlabel("Years of age")
plt.ylabel("Performance")
plt.xticks([0, 0.5, 1.], [0, 40, 120])
plt.yticks(ticks=[])
plt.legend()
plt.savefig("../fun_plots/performance_vs_age.png")
plt.show()