import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt

pgf_with_custom_preamble = {
    "pgf.texsystem": "xelatex",
    "font.family": "sans-serif", # use san serif/main font for text elements
    "font.size": 10,
    "text.usetex": False,    # use inline math for ticks
    "pgf.rcfonts": False,   
    "pgf.preamble": [
        r"\usepackage{amsmath}",
        r"\usepackage{fontspec}",
        r"\setmainfont{Avenir Next}",
        r"\setsansfont{Avenir Next}",
        r"\usepackage{units}",
    ]
}
mpl.rcParams.update(pgf_with_custom_preamble)

#define colors http://colorschemedesigner.com/csd-3.5/#3B400hWs0dJMP
color0      = '#476A92'
color0light = '#9EC0E7'
color1      = '#BAD55E'
color1light = '#E3F6A2'
color2      = '#A0468F'
color2light = '#EA9ADB'
color3      = '#DFAE62'
color3light = '#F8D6A3'

#load data
winter_data = np.loadtxt(open("winter_data_angle_torque.csv","rb"),
    delimiter=",",skiprows=1)
scale_factor = 85/56.7

#tick positions
#tick_positions = np.arange(0,110,10)

#create figure
fig, ax = plt.subplots(1,1, figsize = (2,2))

#add lines connecting medians
markersize = 4
p0, = ax.plot(winter_data[:,3]*180/np.pi, winter_data[:,4]*scale_factor,
    linewidth=2, color=color0)
p1, = ax.plot([5, 17], [0, -60], '--' ,linewidth=2, color=color1)
p2, = ax.plot([0, 70], [10, -10], ls=(0, (2.5,2)) ,linewidth=2, color=color2)

fontsize = ax.xaxis.get_label().get_fontsize()
ax.legend((p0, p1, p2), ('Torque', 'Early Stance Spring', 'Pre-swing/Swing Spring'), 
    frameon = False, loc = (-0.3, 1), fontsize=8, handlelength=3)

ax.xaxis.set_label_text('Angle (deg)')
ax.yaxis.set_label_text('Torque (N-m)')

#set axis properties
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

ax.set_yticks(np.arange(-50, 100, 50))
ax.set_xticks(np.arange(0,100,50))

inv_data = ax.transData.inverted()
inv_axes = ax.transAxes.inverted()

try:
    ylabelpos_axes = ax.yaxis.get_label().get_position()
    ylabelpos_display = ax.transAxes.transform(ylabelpos_axes)
    ylabelpos_data = inv_data.transform(ylabelpos_display)
    ylabelpos_data[1] = (ax.get_yticks()[0] + ax.get_yticks()[-1])/2.0
    ylabelpos_display = ax.transData.transform(ylabelpos_data)
    ylabelpos_axes = inv_axes.transform(ylabelpos_display)
    ax.yaxis.get_label().set_position(ylabelpos_axes)
except:
    pass

try:
    xlabelpos_axes = ax.xaxis.get_label().get_position()
    xlabelpos_display = ax.transAxes.transform(xlabelpos_axes)
    xlabelpos_data = inv_data.transform(xlabelpos_display)
    xlabelpos_data[0] = (ax.get_xticks()[0] + ax.get_xticks()[-1])/2.0
    xlabelpos_display = ax.transData.transform(xlabelpos_data)
    xlabelpos_axes = inv_axes.transform(xlabelpos_display)
    ax.xaxis.get_label().set_position(xlabelpos_axes)
except:
    pass

filename = 'knee_torque_vs_angle.pdf'
fig.savefig(filename, bbox_inches='tight')