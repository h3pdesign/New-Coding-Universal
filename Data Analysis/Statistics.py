
# %%# Our data
import matplotlib.pyplot as plt

labels = ["JavaScript", "Java", "Python", "C#"]

usage = [69.8, 45.3, 38.8, 34.4]


# Generating the y positions. Later, we'll use them to replace them with labels.

y_positions = range(len(labels))


# Creating our bar plot

plt.bar(y_positions, usage)

plt.xticks(y_positions, labels)

plt.ylabel("Usage (%)")

plt.title("Programming language usage")

plt.show()


# Creating boxplot
values = [1, 2, 5, 6, 6, 7, 7, 8, 8, 8, 9, 10, 21]


plt.boxplot(values)

plt.yticks(range(1, 22))

plt.ylabel("Value")

plt.show()

# %%
