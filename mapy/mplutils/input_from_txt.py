import pylab
from numpy import ndarray
# local modules
import plot_defaults
def _input_from_txt(file_name, small = True):
    defaults = plot_defaults._get_defaults(small)
    with open(file_name) as f:
        lines = [l.strip() for l in f.readlines()]
    curves = {}
    index = -1
    append_x = False
    append_y = False
    number = -1
    index = -1
    while True:
        index += 1
        if index > len(lines)-1:
            break
        line = lines[ index ]
        if len(line) > 0:
            if line[0] == '#':
                continue
        #TODO remove this brute force check
        try:
            line = float(line)
        except:
            line = line.lower()
        if line in defaults.keys():
            index += 1
            curves[name][line] = lines[ index ].lower()
        if line == 'label':
            append_x = False
            append_y = False
            number += 1
            index += 1
            line = lines[ index ]
            name = '%02d_' % number + line
            curves[ name ] = { 'x':[], 'y':[] }
            continue
        if line == "":
            append_x = False
            append_y = False
        if line == 'x':
            append_x = True
            append_y = False
            continue
        if line == 'y':
            append_x = False
            append_y = True
            continue
        if append_x:
            curves[name]['x'].append( float(line) )
        if append_y:
            curves[name]['y'].append( float(line) )
    return curves

def create_fig( file_name,
                small=True,
                marker=False,
                figsize=None,
                nrows=1,
                ncols=1,
                sharex=False,
                sharey=False ):
    if not isinstance( file_name, list ):
        file_name = [file_name]
    defaults = plot_defaults._get_defaults(small)
    params = plot_defaults._get_params( small )
    pylab.rcParams.update( params )
    pylab.rc('font', **defaults[ 'font' ])
    if figsize:
        fig, axs = pylab.subplots( nrows=nrows, ncols=ncols,
                                   sharex=sharex, sharey=sharey,
                                   figsize=figsize)
    else:
        fig, axs = pylab.subplots( nrows=nrows, ncols=ncols,
                                   sharex=sharex, sharey=sharey )
    if not isinstance(axs, list) and not isinstance(axs, ndarray):
        axs = [axs]
    for i, f_name in enumerate(file_name):
        curves = _input_from_txt(file_name = f_name, small=False)
        labels = curves.keys()
        labels.sort()
        for label in labels:
            curve = curves[ label ]
            number = label.split('_')[0]
            label  = '_'.join( label.split('_')[1:] )
            number = int(number)
            curr_defaults = plot_defaults._cycle_defaults( number, small=False )
            def current_default( key ):
                if key in curve.keys():
                    return curve[ key ]
                else:
                    if key in curr_defaults.keys():
                        return curr_defaults[key]
                    else:
                        if marker:
                            key += '_marker'
                            if key in curr_defaults.keys():
                                return curr_defaults[key]
                            else:
                                return None
            axs[i].plot( curve['x'], curve['y'],
                  color           = current_default( 'color'     ),
                  label           = label,
                  linewidth       = current_default( 'linewidth' ),
                  linestyle       = current_default( 'linestyle' ),
                  marker          = current_default( 'marker'    ),
                  markerfacecolor = current_default( 'markerfacecolor' ),
                  markeredgecolor = current_default( 'markeredgecolor' ),
                  markeredgewidth = current_default( 'markeredgewidth' ),
                  markersize      = current_default( 'markersize' )       )

    return fig

