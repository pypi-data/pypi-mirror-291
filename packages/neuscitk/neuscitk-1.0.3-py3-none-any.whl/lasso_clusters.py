import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path
import numpy as np
import json
import sys

def main():
    def onselect(verts):
        path = Path(verts)
        indices = np.nonzero([path.contains_point(xy) for xy in clusters[:, :2]])[0]
        
        if len(indices) > 0:
            # Remove selected points from the main scatter plot
            current_mask[indices] = False
            main_scatter.set_offsets(clusters[current_mask])

            # Create a new scatter plot for the selected points
            color = np.random.rand(3,)
            new_scatter = ax.scatter(clusters[indices, 0], clusters[indices, 1], c=[color], label=f'Cluster {current_cluster[0]}')
            scatter_plots.append(new_scatter)

            # Update cluster labels
            cluster_labels[indices] = current_cluster[0]
            current_cluster[0] += 1

            # Update the legend
            ax.legend()

            fig.canvas.draw_idle()

    # Load embeddings
    input_path, output_path = sys.argv[1], sys.argv[2]
    with open(input_path, 'r') as f:
        clusters = json.load(f)
    clusters = np.array(clusters)

    # Initialize cluster labels and mask
    cluster_labels = np.zeros(len(clusters), dtype=int)
    current_cluster = [1]  # Use a list to allow modification inside onselect
    current_mask = np.ones(len(clusters), dtype=bool)

    # Draw plot
    fig, ax = plt.subplots()
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')

    main_scatter = ax.scatter(clusters[:, 0], clusters[:, 1], c='blue', label='Unassigned')
    scatter_plots = [main_scatter]

    lasso = LassoSelector(ax, onselect, props={'c': 'black', 'ls': '--'})

    ax.legend()
    plt.show()

    # Save cluster labels as JSON
    with open(output_path, 'w') as f:
        json.dump(cluster_labels.tolist(), f)

if __name__ == '__main__':
    main()