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
plt.style.use('../matplotlibrc.txt')

grid_dir = '/Users/sw376/Dropbox/Research/data/synthesizer/grids/'
incident_grid = 'bpass-2.2.1-bin_chabrier03-0.1,300.0'
default_model = 'c23.01-fixed'
grid_name = f'{incident_grid}_cloudy-{default_model}'

grid = Grid(grid_name, grid_dir=grid_dir)

log10ages = np.arange(6.0, 8.1, 0.2)

cmap = cmr.sunburst_r
colours = cmr.take_cmap_colors(cmap, len(log10ages), cmap_range=(0.15, 0.85))

diagrams = ['BPT-NII', 'OHNO']
ratios = ['R3', 'R2', 'R23', 'S2', "O32", "Ne3O2", "Si2"]
line_names = [['O 2 3726.03A', 'O 2 3728.81A'], 'H 1 4862.69A', ['O 3 4958.91A', 'O 3 5006.84A'], 'H 1 6564.62A']
line_line_styles = [':','-.','--','-']
ia = 0
metallicity_limits = np.array([0.00002, 0.04])



# ------------------------------------------------------------------------
# line luminosity ratio diagram

fig = plt.figure(figsize=(3.5, 2.5))
gs = fig.add_gridspec(2, 2,
                    hspace=0,
                    wspace=0, 
                    left=0.15,
                    right=0.95, 
                    bottom=0.025,
                    top=0.85,
                    )
axes = gs.subplots()

for line_name, ax in zip(line_names, axes.flatten()):

    # plot lines of constant metallicity
    for ia, (log10age, c) in enumerate(zip(log10ages, colours)):

        ratio = []

        for iz, metallicity in enumerate(grid.metallicity):

            grid_point = grid.get_grid_point((log10age, metallicity))
            dline = grid.get_line((0, iz), line_name)
            line = grid.get_line((ia, iz), line_name)
        
            ratio.append(np.log10(line.luminosity.value/dline.luminosity.value))
        
        ax.plot(
            grid.metallicity, 
            ratio,
            lw=1,
            c=c,
            ls='-',
            zorder=2)

for ax, line_name in zip(axes.flatten(), line_names):
    if isinstance(line_name, list):
        line_name = ','.join(line_name)
    line_label = rf'$\rm {line_labels.labels[line_name]}$'
    ax.text(0.00003, 0.75, line_label, fontsize=7)
    ax.axhline(0.0, c='k', alpha=0.2, lw=4)
    ax.set_xlim(metallicity_limits)
    ax.set_ylim([-0.99, 0.99])
    ax.set_xscale('log')

for ax in axes[1, :]:
    ax.set_xticklabels([])

for ax in axes[0, :]:
    ax.tick_params(top=True, labeltop=True)

for ax in axes[:, 1]:
    ax.yaxis.tick_right()
    ax.set_yticklabels([])

fig.supxlabel(r'$\rm Z$', x=0.55, y=0.95, fontsize=8)
fig.supylabel(r'$\rm log_{10}(L/L_{default})$', x=0.025, y=0.45, fontsize=8)

fig.savefig(f'figs/luminosity_ratio-age.pdf')
fig.clf()

# ------------------------------------------------------------------------
# ratios

ncols = int(np.ceil(len(ratios)/2.))

fig = plt.figure(figsize=(3.5, 3.5))
gs = fig.add_gridspec(ncols, 2,
                        hspace=0,
                        wspace=0, 
                        left=0.15,
                        right=0.85, 
                        bottom=0.025,
                        top=0.9,
                        )
axes = gs.subplots()

for ratio_id, ax in zip(ratios, axes.flatten()):

    # plot lines of constant metallicity
    for ia, (log10age, c) in enumerate(zip(log10ages, colours)):

        ratio = []

        for iz, metallicity in enumerate(grid.metallicity):

            grid_point = grid.get_grid_point((log10age, metallicity))
            lines = grid.get_lines(grid_point)            
            ratio.append(np.log10(lines.get_ratio(ratio_id)))
        
        ax.plot(
            grid.metallicity, 
            ratio,
            lw=1,
            c=c,
            ls='-',
            zorder=2)

for ax, ratio_id in zip(axes.flatten(), ratios):
    
    ax.set_ylabel(ratio_id)
    # ax.axhline(0.0, c='k', alpha=0.2, lw=4)
    ax.set_xlim(metallicity_limits)
    # ax.set_ylim([-0.99, 0.99])
    ax.set_xscale('log')

for ax in axes[-1, :]:
    ax.set_xticklabels([])

for ax in axes[0, :]:
    ax.tick_params(top=True, labeltop=True)

for ax in axes[:, 1]:
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    # ax.set_yticklabels([])

fig.supxlabel(r'$\rm Z$', x=0.55, y=0.95, fontsize=8)
# fig.supylabel(r'$\rm log_{10}(L/L_{default})$', x=0.025, y=0.45, fontsize=8)

fig.savefig(f'figs/ratios-age.pdf')
fig.clf()



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

    for iz, metallicity in enumerate(grid.metallicity):

        x = []
        y = []

        # plot lines of constant metallicity
        for ia, log10age in enumerate(log10ages):

            grid_point = grid.get_grid_point((log10age, metallicity))
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

        ax.plot(x, y, c=colour, ls='-', label=f'$\log_{{10}}(age/Myr)={log10age-6.0:.1f}$')


    ax.set_xlim([0.00001, 40])
    ax.set_ylim([0.001, 40])
    ax.set_xscale('log')
    ax.set_yscale('log')


    xlabel, ylabel = line_labels.diagram_label(LineRatios().diagrams[diagram_id])

    ax.set_xlabel(rf'${xlabel}$')
    ax.set_ylabel(rf'${ylabel}$')


    ax.legend(loc='lower center', fontsize=6, labelspacing=0.0)

    fig.savefig(f'figs/{diagram_id}-age.pdf')
    fig.clf()