"""Utility function to make a GitHub ribbon."""

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def make_github_ribbon(background_color='darkslategray', text_color='white',
                       text='Fork me on GitHub', fontsize=14, figsize=(3, 3),
                       output_file=None, dpi=400):
    """Make a GitHub ribbon.

    Parameters
    ----------
    background_color : str
        Background color.

    text_color : str
        Text color.

    text : str (default = 'Fork me on GitHub')
        The text on the ribbon.

    fontsize : int or float (default = 13)
        Font size for the text.

    figsize : tuple (default = (3, 3))
        Figure size.

    output_file : str or None (default = None)
        Path of the output file. If None, the figure
        is not saved.

    dpi : int or float (default = 400)
        Dots per inch.

    """
    # Create the figure
    fig = plt.figure(figsize=figsize, frameon=False)
    ax = fig.add_subplot(111, aspect='equal')
    ax.axis('off')

    # Define the coordinates of the trapezoid
    left, center, right = 0.3, 0.4, 0.6

    # Plot the trapezoid
    x = [left, center, right, right]
    y = [right, right, center, left]
    ax.add_patch(Polygon(xy=list(zip(x, y)), color=background_color))

    # Plot the text
    fontdict = {'fontname': 'DejaVu Sans',
                'fontsize': fontsize,
                'fontweight': 'heavy'}
    plt.text(0.475, 0.475, text, color=text_color, fontdict=fontdict,
             ha='center', va='center', rotation=-45)

    # Plot the small dashed lines
    epsilon = 0.005
    plt.plot([left + epsilon, right], [right, left + epsilon],
             '--', color=text_color, lw=0.6)
    plt.plot([center - epsilon, right], [right, center - epsilon],
             '--', color=text_color, lw=0.6)

    # Set the limits of the axes
    plt.xlim(left, right)
    plt.ylim(left, right)

    # Save the figure
    if output_file is not None:
        plt.savefig(output_file, dpi=dpi, transparent=True)

    plt.show()
