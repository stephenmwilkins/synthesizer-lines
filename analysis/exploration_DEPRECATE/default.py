

import numpy as np
import matplotlib
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
from matplotlib import cm
from synthesizer.grid import Grid
import cmasher as cmr
from synthesizer.line import (
    get_fancy_line_id,
    LineRatios,
    get_bpt_kewley01,
    get_bpt_kauffman03)
import cmasher as cmr
import line_labels

# set style
plt.style.use('../matplotlibrc.txt')


grid_dir = '/Users/sw376/Dropbox/Research/data/synthesizer/grids/'
grid_name = 'bpass-2.2.1-bin_chabrier03-0.1,300.0-ages:6.,7.,8._cloudy-c23.01-fixed'

grid = Grid(grid_name, grid_dir=grid_dir)

diagram_id = 'BPT-NII'
line_names = [['O 2 3726.03A', 'O 2 3728.81A'], 'H 1 4862.69A', ['O 3 4958.91A', 'O 3 5006.84A'], 'H 1 6564.62A']
ia = 0
metallicity_limits = [0.00001, 0.04]


fig = plt.figure(figsize=(3.5, 5))


bottom = 0.1
height = 0.45
hheight = 0.325
left = 0.15
width = 0.8

ax_bpt = fig.add_axes((left, bottom, width, height))
ax_lr = fig.add_axes((left, bottom+height+0.02, width, hheight))
cax = fig.add_axes((left, bottom+height+hheight+0.02, width, 0.015))

# metallicity
cmap = cmr.get_sub_cmap('cmr.torch', 0., 0.85)
norm = Normalize(vmin=np.log10(metallicity_limits[0]), vmax=np.log10(metallicity_limits[1]))

cmapper = cm.ScalarMappable(norm=norm, cmap=cmap)
fig.colorbar(cmapper, cax=cax, orientation='horizontal')

line_styles = [':','-.','--','-']

for line_name, line_style in zip(line_names, line_styles):

    luminosity = []

    for iz, metallicity in enumerate(grid.metallicity):
        
        grid_point = (ia, iz)
        line = grid.get_line(grid_point, line_name)
       
        luminosity.append(np.log10(line.luminosity.value))
    

    if isinstance(line_name, list):
        line_id = ','.join(line_name)
    else:
        line_id = line_name

    line_label = line_labels.labels[line_id]

    ax_lr.plot(np.log10(grid.metallicity), 
               luminosity, 
               lw=1, 
               c='k', 
               ls=line_style, 
               label=rf'$\rm {line_label}$')




# plot Kewley and Kauffmann lines 
for f, ls, limit, label in zip([get_bpt_kewley01, get_bpt_kauffman03],
                                ['-', '--'],
                                [0.47, 0.05],
                                ['Kewley+2001', 'Kauffman+2003']):
    log10x = np.arange(-5., limit, 0.01)
    ax_bpt.plot(10**log10x, 10**f(log10x), ls=ls, lw=1, c='k', alpha=0.3, label=label)

x = []
y = []

for iz, metallicity in enumerate(grid.metallicity):

    colour = cmap(norm(np.log10(metallicity)))
    grid_point = (ia, iz)
    lines = grid.get_lines(grid_point)
    x_, y_ = lines.get_diagram(diagram_id)
    x.append(x_)
    y.append(y_)
    # ax_bpt.scatter(x_, y_, marker='o', s=(iz+1)*3, color=colour, zorder=2, label=rf'$\rm Z={metallicity}$')
    ax_bpt.scatter(x_, y_, marker='o', s=(iz+1)*3, color=colour, zorder=2)

ax_bpt.plot(x, y, lw=1, c='k', alpha=0.3, zorder=1)
ax_bpt.legend(fontsize=6, labelspacing=0.05)

ax_bpt.set_xlim([0.00001, 40])
ax_bpt.set_ylim([0.001, 40])
ax_bpt.set_xscale('log')
ax_bpt.set_yscale('log')

xlabel, ylabel = line_labels.diagram_label(LineRatios().diagrams[diagram_id])
ax_bpt.set_xlabel(rf'${xlabel}$')
ax_bpt.set_ylabel(rf'${ylabel}$')


ax_lr.xaxis.tick_top()
ax_lr.xaxis.set_label_position('top') 
ax_lr.set_xlim(np.log10(metallicity_limits))
# ax_lr.set_ylim([-0.5, 0.5])
ax_lr.legend(fontsize=6)
ax_lr.set_xticklabels([])
ax_lr.set_ylabel(r'$\rm log_{10}(L/erg\ s^{-1}\ M_{\odot}^{-1})$')

cax.xaxis.tick_top()
cax.xaxis.set_label_position('top')
cax.set_xlabel(r'$\rm \log_{10}(Z)$')

fig.savefig(f'figs/default_model.pdf')
fig.clf()