"""Utility functions to make the pyts logo."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Arc, Rectangle


def maximum(x):
    """Return the element-wise maximum of an array and 0.

    Parameters
    ----------
    x : array
        Input data.

    Return
    ------
    x_pos : array
        Non-negative values of the array.

    """
    return np.maximum(x, 0)


def circle(x, r, a, b, x_lim):
    """Compute the y-coordinates of the arc.

    Parameters
    ----------
    x : array
        X-coordiantes of the arc.

    r : float
        Radius of the arc.

    a : float
        X-coordinate of the center of the arc.

    b : float
        Y-coordinate of the center of the arc.

    x_lim : (x_min, x_max)
        Tuple with the limits for the X-coordiantes.

    Return
    ------
    y : array
        Y-coordinates of the arc.

    """
    y = (b + np.sqrt(maximum(
        r ** 2 - ((x - a) ** 2) * (x >= x_lim[0]) * (x <= x_lim[1]))
    )) * (x >= x_lim[0]) * (x <= x_lim[1])
    return y


def pyts_time_series(x):
    """Compute the y-coordinates of the time series.

    Parameters
    ----------
    x : array
        X-coordinates of the time series.

    Return
    ------
    y : array
        Y-coordinates of the time series.

    """
    p = circle(x, r=0.2, a=0, b=0, x_lim=(-0.2, 0.2))
    y = - circle(x, r=0.2, a=0.4, b=0, x_lim=(0.2, 0.6))
    t = 0
    s = circle(x, r=0.125, a=0.9, b=-0.025, x_lim=(0.775, 0.9))
    s += 0.1 * (x >= 0.9) * (x <= 1.2)
    return p + y + t + s


def make_pyts_logo(cmap='jet', background_color='darkslategray',
                   output_file=None, dpi=400):
    """Make the pyts logo.

    Parameters
    ----------
    cmap : str
        Colormap for the time series.

    background_color : str
        Background color for the letters.

    linewidth : float (default = 12)
        Line width of the letters. It must be a positive number.

    output_file : str of None (default = None)
        Path where the image is saved. If None, the image is not saved.

    dpi : int (default = 400)
        Dots per inch.

    Notes
    -----
    Available colormaps: https://matplotlib.org/examples/color/colormaps_reference.html
    Available colors: https://matplotlib.org/3.1.0/gallery/color/named_colors.html

    """  # noqa: E501
    # Properties
    figsize = (5, 3)
    radius = 0.2
    linewidth = 20
    line_params = {'lw': linewidth, 'color': background_color,
                   'solid_capstyle': 'round'}
    arc_params = {'facecolor': 'none', 'lw': linewidth,
                  'edgecolor': background_color, 'capstyle': 'round'}

    # Create the figure
    fig, ax = plt.subplots(figsize=figsize, frameon=False)
    ax.axis('off')

    # CREATE THE "PYTS" BLACK BACKGROUND

    # Create the "p"
    arc_p = Arc((0, 0), 2 * radius, 2 * radius, **arc_params)
    line_p = Line2D([-0.2, -0.2], [-0.6, 0.2], **line_params)
    ax.add_patch(arc_p)
    ax.add_line(line_p)

    # Create the "y"
    line_left_y = Line2D([0.2, 0.2], [0, 0.15], **line_params)
    line_right_y = Line2D([0.6, 0.6], [0.15, -0.4], **line_params)
    arc_lower_y = Arc((0.4, -0.4), 2 * radius, 2 * radius,
                      theta1=-180, theta2=0, **arc_params)
    ax.add_line(line_left_y)
    ax.add_line(line_right_y)
    ax.add_patch(arc_lower_y)

    # Create the "t"
    arc_t = Arc((0.7, -0.3), radius, radius, theta1=-165,
                theta2=-90, **arc_params)
    line_middle_t = Line2D([0.5, 0.6], [0, 0], **line_params)
    line_lower_t = Line2D([0.7, 0.9], [-0.4, -0.4], **line_params)
    ax.add_patch(arc_t)
    ax.add_line(line_middle_t)
    ax.add_line(line_lower_t)

    # Create the "s"
    arc_lower_s = Arc((0.9, -0.275), 1.25 * radius, 1.25 * radius,
                      theta1=-90, theta2=91, **arc_params)
    arc_upper_s = Arc((0.9, -0.025), 1.25 * radius, 1.25 * radius,
                      theta1=181, theta2=-90, capstyle='butt',
                      facecolor='none', lw=linewidth,
                      edgecolor=background_color, zorder=2)
    ax.add_patch(arc_lower_s)
    ax.add_patch(arc_upper_s)

    # PLOT THE TIME SERIES
    x = np.linspace(-0.2, 1.2, 800)
    y = pyts_time_series(x)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(-0.2, 1.1)
    lc = LineCollection(segments, cmap=cmap, norm=norm,
                        capstyle='round', zorder=3)
    lc.set_array(x)
    lc.set_linewidth(linewidth)
    ax.add_collection(lc)

    # Fix bounding issue
    arc_upper_s = Arc((0.854, -0.05), 0.5 * radius, 0.3 * radius,
                      theta1=180, theta2=-150, capstyle='butt',
                      facecolor='none', lw=1.1 * linewidth,
                      edgecolor=background_color, zorder=4)
    rectangle_patch = Rectangle((0.8312, -0.05), width=0.1, height=0.05,
                                fill=True, color='white', zorder=5)
    ax.add_patch(arc_upper_s)
    ax.add_patch(rectangle_patch)

    # Set the good limits for the axes
    plt.xlim((-0.25, 1.25))
    plt.ylim((-0.65, 0.25))

    # Save the figure
    plt.tight_layout()
    if output_file is not None:
        plt.savefig(output_file, dpi=dpi)

    plt.show()
