import matplotlib.pyplot as plt
import numpy as np

# Group names and bar values
group_names = ['0133', '1536', '0068']
values_1 = [0.9997, 0.9902, 0.9833]
values_2 = [1, 0.99, 0.98]

# Setting the positions and width for the bars
positions = np.arange(len(group_names))
width = 0.3

# Plotting the bars with numbers on top
fig, ax = plt.subplots()
bar1 = ax.bar(positions - width/2, values_1, width, label='True', color='skyblue')
bar2 = ax.bar(positions + width/2, values_2, width, label='Estimate', color='orange')

# Adding some text for labels, title, and custom x-axis tick labels, etc.
ax.set_xlabel('Models')
ax.set_ylabel('Accuracy')
# ax.set_title('Bar graph with 3 groups and 2 bars each')
ax.set_xticks(positions)
ax.set_xticklabels(group_names)
ax.legend(loc='lower left')

# Adding the numbers on top of each bar
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.4f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

add_labels(bar1)
add_labels(bar2)

# Show the plot
plt.savefig('bar_graph.svg')
# plt.show()
