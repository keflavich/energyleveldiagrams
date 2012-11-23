import matplotlib.pyplot as pl
import matplotlib as mpl
import numpy as np
from collections import defaultdict
import itertools

orbitals = ['s','p','d','f','g']

class EnergyLevel(object):
    def __init__(self, energy, orbital, name=None):
        self.energy = energy
        self.orbital = orbital
        if name is None:
            name = "%f%s" % (energy,orbital)
        self.name = name

class EnergyLevelDiagram(object):
    def __init__(self, figure=None):
        self.figure = pl.figure() if figure is None else figure
        self.levels = {}
        self.orbitals = []
        self.lines = []
        self.arrows = []

        self.orbital_colors = defaultdict(itertools.repeat('cyan').next,
                {'s': 'black',
                'p': 'blue',
                'd': 'red',
                'f': 'green',
                'g': 'orange'})

        self.orbital_xrange = defaultdict(itertools.repeat((0.1,0.9)).next,
                [(oo,[ii+0.1,ii+1-0.1]) for ii,oo in enumerate(orbitals)])

    @property
    def axis(self):
        return self.figure.gca()

    def add_level(self, energy, orbital, name=None):
        EL = EnergyLevel(energy,orbital,name)
        self.levels[EL.name] = EL
        #if energy in self.levels:
        #    self.levels[energy].append(orbital)
        #else:
        #    self.levels[energy] = [orbital]


        ## put energy in correct position in list
        #bisect.insort(self, levels, energy)


    def plot_levels(self):

        self.lines = [
            self.axis.plot(
                self.orbital_xrange[EL.orbital],
                [EL.energy,EL.energy], 
                color=self.orbital_colors[EL.orbital])
            for (en,EL) in self.levels.iteritems()]

        #self.axis.set_ylim(min(energy),max(energy))

    def connect_levels(self, levelname1, levelname2, value=None,
            arrowstyle='-|>,head_width=5,head_length=10',
            color='k', pad_length=0.1,
            **arrow_kwargs):
        lev1 = self.levels[levelname1]
        lev2 = self.levels[levelname2]
        x1y1 = np.array((np.mean(self.orbital_xrange[lev1.orbital]), lev1.energy))
        x2y2 = np.array((np.mean(self.orbital_xrange[lev2.orbital]), lev2.energy))
        arrow = mpl.patches.FancyArrowPatch(
                x1y1,
                x2y2,
                arrowstyle=arrowstyle,
                **arrow_kwargs)
        arrow.set_facecolor(color)
        arrow.set_edgecolor(color)
        arrow.label = value

        if value is not None:
            textpos=np.mean([x1y1,x2y2],axis=0)
            if np.any([ np.sum((T.xy-textpos)**2) < pad_length for T in self.axis.texts]):
                textpos += pad_length
            vector = (x2y2-x1y1)
            angle = np.arctan2(*vector)*180/np.pi
            # http://matplotlib.org/examples/pylab_examples/text_rotation_relative_to_line.html
            trans_angle = self.axis.transData.transform_angles(
                    np.array((angle,)), vector.reshape([1,2]))[0]
            print angle,trans_angle,value
            
            txt = self.axis.annotate(str(value), textpos,
                    color=color,
                    bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.8),
                    rotation=180+trans_angle)



        self.axis.add_patch(arrow)
        self.arrows.append(arrow)

    def energy_connect(self,levelname1,levelname2,
            xpos=0,
            arrowstyle='-|>,head_width=5,head_length=10',
            color='k', pad_length=0.1, label=None,
            textkwargs={},
            **arrow_kwargs):
        """ needs better name? """
        lev1 = self.levels[levelname1]
        lev2 = self.levels[levelname2]
        x1y1 = (xpos, lev1.energy)
        x2y2 = (xpos, lev2.energy)
        arrow = mpl.patches.FancyArrowPatch(
                x1y1,
                x2y2,
                arrowstyle=arrowstyle,
                **arrow_kwargs)
        arrow.set_facecolor(color)
        arrow.set_edgecolor(color)
        if label is None:
            arrow.label = "%f" % (lev1.energy-lev2.energy)
        else:
            arrow.label = label

        textpos=np.mean([x1y1,x2y2],axis=0)
        if np.any([ np.sum((T.xy-textpos)**2) < pad_length for T in self.axis.texts]):
            textpos += pad_length
        txt = self.axis.annotate(str(arrow.label), textpos,
                color=color,
                bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.8),
                **textkwargs)



        self.axis.add_patch(arrow)
        self.arrows.append(arrow)

    def _fix_labels(self, pad_length=1):
        return # doesn't work.  @#$!
        # need a renderer...
        pl.draw()
        for txt in self.axis.texts:
            for T in self.axis.texts:
                textcoords = txt.get_position()
                if txt.get_window_extent().count_overlaps([T.get_window_extent()]):
                    print "OVERLAP, moving text ",txt
                    txt.xy = txt.xy+pad_length
                    #txt.set_position([txt.xy[0]+pad_length, txt.xy[1]+pad_length])
                    #txt.update_positions(self.axis)
                    print "OVERLAP, moved text ",txt
                    return


if __name__ == "__main__":

    hydrogen = EnergyLevelDiagram()
    rydberg = 13.6056925330

    for nn  in xrange(1,10):
        for oo,orb in enumerate(orbitals):
            if oo >= nn:
                continue
            hydrogen.add_level(-rydberg/nn**2, orb, name="%i%s" % (nn,orb))

    hydrogen.plot_levels()

    #hydrogen.connect_levels('4d','2s',value=)
    A4d2p = (2.0625e+07+1.7188e+07)
    A4d3p = (1.1729e+06+7.0376e+06+5.8647e+06)
    A4s2p = (8.5941e+05+1.7190e+06)
    A4p2s = (9.6680e+06+9.6683e+06)
    A4s3s = (3.0650e+06+3.0652e+06)
    A4p3d = (3.4754e+04+3.1280e+05+3.4759e+05)
    avals = A4d2p, A4d3p, A4s2p, A4p2s, A4s3s, A4p3d
    logavals = np.log10(avals)
    linewidths = ((logavals-logavals.min())/logavals.ptp()+1)
    print avals,np.log10(avals)


    hydrogen.connect_levels('4d','2p',linewidth=(np.log10(A4d2p)-np.min(logavals)+1)/logavals.ptp()*3, value="%e" % A4d2p)
    hydrogen.connect_levels('4d','3p',linewidth=(np.log10(A4d3p)-np.min(logavals)+1)/logavals.ptp()*3, value="%e" % A4d3p,color='r')
    hydrogen.connect_levels('4s','2p',linewidth=(np.log10(A4s2p)-np.min(logavals)+1)/logavals.ptp()*3,value="%e" % A4s2p)
    hydrogen.connect_levels('4p','2s',linewidth=(np.log10(A4p2s)-np.min(logavals)+1)/logavals.ptp()*3,value="%e" % A4p2s,color='b')
    hydrogen.connect_levels('4p','3s',linewidth=(np.log10(A4s3s)-np.min(logavals)+1)/logavals.ptp()*3,value="%e" % A4s3s,color='r')
    hydrogen.connect_levels('4p','3d',linewidth=(np.log10(A4p3d)-np.min(logavals)+1)/logavals.ptp()*3,value="%e" % A4p3d,color='g')
    hydrogen.energy_connect('4s','3s',label='Paschen $\\alpha$')
    hydrogen.energy_connect('4s','2s',xpos=2.95,label='Balmer $\\beta$', textkwargs={'ha':'right'})
    pl.axis([-0.1,3,-3.6,-0.6])
    pl.xlabel("Orbital")
    hydrogen.axis.set_xticks([0.5,1.5,2.5])
    hydrogen.axis.set_xticklabels(['s','p','d'])
    pl.ylabel("Energy (eV)")
    #hydrogen._fix_labels()

    # NIST-based test...
    

