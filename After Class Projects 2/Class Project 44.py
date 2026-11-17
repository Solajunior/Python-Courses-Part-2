import matplotlib as mpl
import matplotlib.pyplot as plt

savings = [59, 102, 345, 96, 156, 32, 65, 244, 12, 0]
days = list(range(1, len(savings) + 1))

plt.plot(days, savings)
plt.xlabel("Day")
plt.ylabel("Savings")
plt.title("Savings Over Time")
plt.show()