import pylab
import os
import _small
import _big
def _get_defaults( small=True ):
    if small:
        return _small.defaults
    else:
        return _big.defaults

def _get_params( small=True ):
    if small:
        return _small.params
    else:
        return _big.params

def _cycle_defaults( number, small=True ):
    defaults = _get_defaults( small )
    curr_defaults  = {}
    for param, values in defaults.iteritems():
        if type( values ) == list:
            curr_defaults[ param ] = values[ number % len(values) ]
        else:
            curr_defaults[ param ] = values

    return curr_defaults

def _figname( x_label,y_label ):
    replace_dict = { '/':'',
                     '/':'',
                     '\\':'',
                     '\\':'',
                     '$':'',
                     '$':'',
                     '{':'',
                     '{':'',
                     '}':'',
                     '}':'',
                     '|':'',
                     ' ':'_',
                   }
    for k, v in replace_dict.items():
        x_label = x_label.replace(k, v)
        y_label = y_label.replace(k, v)
    ans = 'fig'+x_label[:5]+y_label[:5]+'_000.png'
    while True:
        if ans in os.listdir('.'):
            tmp = ans.split('_')
            ans = '_'.join( tmp[:-1] )
            num = tmp[-1]
            num = int(num[:-4])
            num += 1
            ans += '_%03d.png' % num
        else:
            break
    return ans

def savefig( fig, small=True, **kwargs ):
    ax = fig.axes[0]
    kwargs['bbox_inches'] = 'tight'
    kwargs['format'] = 'png'
    fname = kwargs.get('fname')
    if not fname:
        x_label = ax.get_xlabel()
        y_label = ax.get_ylabel()
        fname = _figname( x_label, y_label )
    figsize = kwargs.get('figsize')
    if not figsize:
        params = _get_params( small )
        kwargs['figsize'] = params['figure.figsize']
    else:
        fig.set_size_inches(figsize)
    pylab.savefig( fname, **kwargs )

def myfig( fig, small=True, add_marker=False, add_color=False,
        add_linestyle=True, marker=None, color=None, linestyle=None ):
    params = _get_params( small )
    defaults = _get_defaults( small )
    if marker:
        add_marker=True
        defaults['marker_marker'] = marker
    if linestyle:
        add_linestyle=True
        defaults['linestyle_linestyle'] = linestyle
    if color:
        add_color=True
        defaults['color_color'] = color
    pylab.rcParams.update( params )
    pylab.rc('font', **defaults[ 'font' ])
    for i, line in enumerate( fig.axes[0].lines ):
        curr_defaults = _cycle_defaults( i )
        keys = curr_defaults.keys()
        keys.sort()
        for k in keys:
            k2=k

            #TODO improve these extra options
            if '_marker' in k:
                if add_marker:
                    k2 = k[:-7]
                else:
                    continue
            if '_linestyle' in k:
                if add_linestyle:
                    k2 = k[:-10]
                else:
                    continue
            if '_color' in k:
                if add_color:
                    k2 = k[:-6]
                else:
                    continue
            #

            attr = getattr( line, 'set_' + k2, 'NOTFOUND' )
            if attr == 'NOTFOUND':
                continue
            attr( curr_defaults[ k ] )
    leg = fig.axes[0].legend()
    if leg <> None:
        leg.set_visible(True)
    pylab.ion()
    return fig

def myplot( xs, ys, x_label='', y_label='',
            defaults=None,
            fig=None,
            label=None,
            defaults_number=0,
            small = True):
    if small:
        params = _small.params
    else:
        params = _big.params
    if fig==None:
        fig = pylab.figure()
    if defaults == None:
        curr_defaults = _cycle_defaults( defaults_number )
    xmin = 1.e6
    xmax = -1.e6
    ymin = 1.e6
    ymax = -1.e6
    pylab.rcParams.update( params )
    pylab.rc('font', **defaults[ 'font' ])
    pylab.plot( xs, ys,
                color           = curr_defaults[ 'color'     ],
                label           = label,
                linewidth       = curr_defaults[ 'linewidth' ],
                linestyle       = curr_defaults[ 'linestyle' ],
                marker          = curr_defaults[ 'marker'    ],
                markerfacecolor = curr_defaults[ 'markerfacecolor' ],
                markeredgecolor = curr_defaults[ 'markeredgecolor' ],
                markeredgewidth = curr_defaults[ 'markeredgewidth' ],
                markersize      = curr_defaults[ 'markersize' ]       )
    pylab.axis('scaled')
    pylab.legend( loc='upper right' , ncol=2)
    pylab.xlabel( x_label, labelpad = 10, ha = 'left')
    pylab.ylabel( y_label, labelpad = 10, va='bottom')
    # in case we want to rescale the axes
    xmin = min(xmin, min( xs ))
    xmax = max(xmax, max( xs ))
    ymin = min(ymin, min( ys ))
    ymax = max(ymax, max( ys ))
    pylab.xlim(xmin,xmax*1.002)
    pylab.ylim(ymin,ymax*1.002)
    figsize = params['figure.figsize']
    pylab.savefig( _figname(x_label,y_label),
                   bbox_inches='tight',
                   figsize=figsize )
    return fig



