# plot the evolution of the specific ionising luminosity for different ions

import numpy as np
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
from matplotlib import cm
from synthesizer.grid import Grid
import cmasher as cmr
import cmasher as cmr


# set style
plt.style.use('../../matplotlibrc.txt')

grid_dir = '/Users/sw376/Dropbox/Research/data/synthesizer/grids/'
grid_name = 'bpass-2.2.1-bin_chabrier03-0.1,300.0'

grid = Grid(grid_name, grid_dir=grid_dir, read_lines=False)


for ion, specific_ionising_luminosity in grid.log10_specific_ionising_lum.items():

    print(ion)
    print(specific_ionising_luminosity.shape)

    fig = plt.figure(figsize=(3.5, 3.))

    bottom = 0.15
    height = 0.7
    left = 0.15
    width = 0.8

    ax = fig.add_axes((left, bottom, width, height))
    cax = fig.add_axes((left, bottom+height, width, 0.025))

    # metallicity
    cmap = cmr.get_sub_cmap('cmr.torch', 0., 0.85)
    norm = Normalize(vmin=np.log10(grid.metallicity[0]), vmax=np.log10(grid.metallicity[-1]))

    cmapper = cm.ScalarMappable(norm=norm, cmap=cmap)
    fig.colorbar(cmapper, cax=cax, orientation='horizontal')

    for iz, metallicity in enumerate(grid.metallicity):

        s = grid.log10age < 9.1

        ax.plot(grid.log10age[s], specific_ionising_luminosity[s, iz], c=cmap(norm(np.log10(metallicity))), lw=1)


    ax.set_xlim([6., 9.])
    # ax.set_ylim([0.001, 40])

    ax.set_xlabel(r'$\log_{10}(age/yr)$')
    ax.set_ylabel(rf'$\log_{{10}}(\dot{{n}}_{{{ion}}}/s^{{-1}}\ M_{{\odot}}^{{-1}})$')

    cax.xaxis.tick_top()
    cax.xaxis.set_label_position('top')
    cax.xaxis.set_tick_params(labelsize=7)
    cax.set_xlabel(r'$\log_{10}(Z)$', fontsize=7)

    fig.savefig(f'figs/specific_ionising_luminosity_{ion}.pdf')
    fig.clf()


# hardness


fig = plt.figure(figsize=(3.5, 3.))

bottom = 0.15
height = 0.7
left = 0.15
width = 0.8

ax = fig.add_axes((left, bottom, width, height))
cax = fig.add_axes((left, bottom+height, width, 0.025))

# metallicity
cmap = cmr.get_sub_cmap('cmr.torch', 0., 0.85)
norm = Normalize(vmin=np.log10(grid.metallicity[0]), vmax=np.log10(grid.metallicity[-1]))

cmapper = cm.ScalarMappable(norm=norm, cmap=cmap)
fig.colorbar(cmapper, cax=cax, orientation='horizontal')

for iz, metallicity in enumerate(grid.metallicity):

    s = grid.log10age < 9.1

    ratio = grid.log10_specific_ionising_lum['HeII'][s, iz]-grid.log10_specific_ionising_lum['HI'][s, iz]

    ax.plot(grid.log10age[s], ratio, c=cmap(norm(np.log10(metallicity))), lw=1)


ax.set_xlim([6., 9.])
# ax.set_ylim([0.001, 40])

ax.set_xlabel(r'$\log_{10}(age/yr)$')
ax.set_ylabel(r'$\log_{10}(\dot{n}_{HeII}/\dot{n}_{HI})$')

cax.xaxis.tick_top()
cax.xaxis.set_label_position('top')
cax.xaxis.set_tick_params(labelsize=7)
cax.set_xlabel(r'$\log_{10}(Z)$', fontsize=7)

fig.savefig(f'figs/hardness.pdf')
fig.clf()




fig = plt.figure(figsize=(3.5, 6.))

bottom = 0.1
height = 0.275
left = 0.15
width = 0.8

ax1 = fig.add_axes((left, bottom, width, height))
ax2 = fig.add_axes((left, bottom+height, width, height))
ax3 = fig.add_axes((left, bottom+height*2, width, height))
cax = fig.add_axes((left, bottom+height*3, width, 0.01))

for (ion, specific_ionising_luminosity), ax in zip(grid.log10_specific_ionising_lum.items(), [ax3, ax2]):

    # metallicity
    cmap = cmr.get_sub_cmap('cmr.torch', 0., 0.85)
    norm = Normalize(vmin=np.log10(grid.metallicity[0]), vmax=np.log10(grid.metallicity[-1]))

    cmapper = cm.ScalarMappable(norm=norm, cmap=cmap)
    fig.colorbar(cmapper, cax=cax, orientation='horizontal')

    for iz, metallicity in enumerate(grid.metallicity):
        s = grid.log10age < 9.1
        ax.plot(grid.log10age[s], specific_ionising_luminosity[s, iz], c=cmap(norm(np.log10(metallicity))), lw=1)

    ax.set_xlim([6., 9.])
    ax.xaxis.set_ticklabels([])
    ax.set_ylabel(rf'$\log_{{10}}(\dot{{n}}_{{{ion}}}/s^{{-1}}\ M_{{\odot}}^{{-1}})$')

    

# hardness
for iz, metallicity in enumerate(grid.metallicity):

    s = grid.log10age < 9.1

    ratio = grid.log10_specific_ionising_lum['HeII'][s, iz]-grid.log10_specific_ionising_lum['HI'][s, iz]

    ax1.plot(grid.log10age[s], ratio, c=cmap(norm(np.log10(metallicity))), lw=1)

ax1.set_xlim([6., 9.])
ax1.set_xlabel(r'$\log_{10}(age/yr)$')
ax1.set_ylabel(r'$\log_{10}(\dot{n}_{HeII}/\dot{n}_{HI})$')

cax.xaxis.tick_top()
cax.xaxis.set_label_position('top')
cax.xaxis.set_tick_params(labelsize=7)
cax.set_xlabel(r'$\log_{10}(Z)$', fontsize=7)

fig.savefig(f'figs/specific_ionising_luminosity.pdf')
fig.clf()
