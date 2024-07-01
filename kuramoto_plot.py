import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from IPython.display import HTML

def animate_kuramoto(*oscillator_data, natural_frequencies=None, show_average=False, interval=50, steps_per_frame=3, save_gif=None):
    """Produces an animation of Kuramoto oscillators which can be viewed in a Jupyter notebook.

    Args:
        oscillator_data: List of 1D Numpy arrays, each of which is a timeseries of Kuramoto
            oscillator phases. Each should be equal length.
        natural_frequencies: 1D Numpy array containing natural frequencies of oscillators,
            used to color code oscillators
        show_avereage: If True, animates average position of oscillators
        interval: Delay between frames in milliseconds
        steps_per_frame: Number of timeseries steps per frame
        save_fig: Filename to save a gif of the animation to

    Returns:
        An IPython display object which contains an animation of the Kuramoto oscillators.
    """

    # Get oscillator position data and calculate relevant x and y positions
    number_of_oscillators = len(oscillator_data)
    data = np.array(oscillator_data)
    xs = np.cos(data)
    ys = np.sin(data)
    avg_x = np.mean(xs, axis=0)
    avg_y = np.mean(ys, axis=0)

    # Create background of figure
    fig = plt.figure(figsize=(4,4))
    ax = plt.axes(xlim=(-1.2, 1.2), ylim=(-1.2, 1.2))
    ax.axis('off')
    ax.add_patch(plt.Circle((0, 0), radius=1, edgecolor='grey', facecolor='None'))

    # Assign colors to each of the oscillators based on natural frequencies
    if natural_frequencies is not None:
        cmap = cm.coolwarm
        norm = Normalize(vmin=min(natural_frequencies), vmax=max(natural_frequencies))
        natural_frequency_colors = cmap(norm(natural_frequencies))

    # Function to draw each frame of the animation
    def animate(i):

        # Remove old points
        for line in ax.get_lines():  
            line.remove()

        # Display new points
        timestep_num = i * steps_per_frame
        pts = []
        for i in range(number_of_oscillators):
            if natural_frequencies is not None:
                pt, = ax.plot(xs[i, timestep_num], ys[i, timestep_num], marker='o', color=natural_frequency_colors[i], markeredgecolor='k')
            else:
                pt, = ax.plot(xs[i, timestep_num], ys[i, timestep_num], marker='o', color='k', markeredgecolor='k')
            pts.append(pt)
        
        # Display average position of oscillators
        if show_average:
            pt, = ax.plot(avg_x[timestep_num], avg_y[timestep_num], marker='x', color='gray', markeredgecolor='k')
            pts.append(pt)
        
        return pts
        
    # Create animation
    anim = animation.FuncAnimation(fig, animate, frames=data.shape[1]//steps_per_frame, interval=interval, blit=True)
    plt.close()

    # Save to file
    if save_gif:
        anim.save(save_gif)
        
    return(HTML(anim.to_jshtml()))