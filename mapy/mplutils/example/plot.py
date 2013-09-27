#
import sys
sys.path.append(r'C:\Users\dlr-regina\Dropbox\desicos\abaqus-conecyl-python\matplotlib_utils')
#
# local modules
import plot_defaults
from input_from_txt import create_fig
#
figsize = (9,5)
fig = create_fig(file_name='input.txt',
                 small=False,
                 marker=True,
                 figsize = figsize)
ax = fig.axes[0]
ax.legend( loc='upper center' , ncol=4)
#
ax.set_xlabel('imperfection amplitude / laminate thickness')
ax.xaxis.labelpad = 10
ax.xaxis.ha = 'left'
ax.set_ylabel( 'P / Pcr' )
ax.yaxis.labelpad = 10
ax.yaxis.va = 'bottom'
#
ax.set_xlim(0.0, 1.10)
ax.set_ylim(0.2, 1.4)
#
for line in ax.lines:
    line.set_zorder(100)
fig.show()
plot_defaults.savefig( fig, small=False, figsize=figsize )
