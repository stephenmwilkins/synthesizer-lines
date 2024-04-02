import numpy as np
import matplotlib.pyplot as plt
from synthesizer.grid import Grid
from synthesizer.line import (
    LineRatios,
    get_bpt_kewley01,
    get_bpt_kauffman03)
import cmasher as cmr
import line_labels

# set style
plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')


grid_dir = '/Users/sw376/Dropbox/Research/data/synthesizer/grids/'
incident_grid = 'bpass-2.2.1-bin_chabrier03-0.1,300.0'
default_model = 'c23.01-sps'
grid_name = f'{incident_grid}_cloudy-{default_model}'

grid = Grid(grid_name, grid_dir=grid_dir)







# set style
plt.style.use('../matplotlibrc.txt')


for diagram_id in ['BPT-NII']:

    fig = plt.figure(figsize=(3.5, 3.5))
    left = 0.15
    height = 0.75
    bottom = 0.15
    width = 0.8
    ax = fig.add_axes((left, bottom, width, height))


    # plot Kewley and Kauffmann lines 
    for f, ls, limit, label in zip([get_bpt_kewley01, get_bpt_kauffman03],
                                   ['-', '--'],
                                   [0.47, 0.05],
                                   ['Kewley+2001', 'Kauffman+2003']):
        log10x = np.arange(-5., limit, 0.01)
        ax.plot(10**log10x, 10**f(log10x), ls=ls, lw=1, c='k', alpha=0.3, label=label)

    log10ages = [6., 6.5, 7., 7.5, 8., 8.5, 9.]

    cmap = cmr.gothic
    colours = cmr.take_cmap_colors(cmap, len(log10ages), cmap_range=(0.15, 0.85))

    for iz, metallicity in enumerate(grid.metallicity):

        x = []
        y = []

        # plot lines of constant metallicity
        for ia, log10age in enumerate(grid.log10age):

            grid_point = (ia, iz)
            lines = grid.get_lines(grid_point)
            x_, y_ = lines.get_diagram(diagram_id)
            x.append(x_)
            y.append(y_)

        ax.plot(x, y, c='k', alpha=0.1, ls='-', lw=1)

    # plot marker for specific ages
    for ia, (log10age, colour) in enumerate(zip(log10ages, colours)):

        x = []
        y = []

        for iz, metallicity in enumerate(grid.metallicity):

            grid_point = grid.get_grid_point((log10age, metallicity))
            lines = grid.get_lines(grid_point)
            x_, y_ = lines.get_diagram(diagram_id)
            x.append(x_)
            y.append(y_)
            ax.scatter(x_, y_, marker='o', s=3, color=colour)

        ax.plot(x, y, c=colour, ls='-', label=f'$\log_{{10}}(age/Myr)={log10age-6.0}$')


    ax.set_xlim([0.00001, 40])
    ax.set_ylim([0.001, 40])
    ax.set_xscale('log')
    ax.set_yscale('log')


    xlabel, ylabel = line_labels.diagram_label(LineRatios().diagrams[diagram_id])

    ax.set_xlabel(rf'${xlabel}$')
    ax.set_ylabel(rf'${ylabel}$')


    ax.legend(loc='lower right', fontsize=6, labelspacing=0.0)

    fig.savefig(f'figs/{diagram_id}-reference.pdf')
    fig.clf()