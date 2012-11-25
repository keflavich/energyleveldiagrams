import matplotlib.pyplot as pl
import matplotlib as mpl
import numpy as np
from collections import defaultdict
import itertools


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
        self.orbitals = ['s','p','d','f','g']
        self.lines = []
        self.arrows = []
        self.connections = []

        self.orbital_colors = defaultdict(itertools.repeat('cyan').next,
                {'s': 'black',
                'p': 'blue',
                'd': 'red',
                'f': 'green',
                'g': 'orange'})

        self.orbital_xrange = defaultdict(itertools.repeat((0.1,0.9)).next,
                [(oo,[ii+0.1,ii+1-0.1]) for ii,oo in enumerate(self.orbitals)])

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
            randomness=0.1,
            **arrow_kwargs):
        lev1 = self.levels[levelname1]
        lev2 = self.levels[levelname2]
        x1y1 = np.array((np.mean(self.orbital_xrange[lev1.orbital]), lev1.energy))
        x2y2 = np.array((np.mean(self.orbital_xrange[lev2.orbital]), lev2.energy))
        if randomness is not None:
            x1y1[0] += np.random.randn()*randomness
            x2y2[0] += np.random.randn()*randomness
        arrow = mpl.patches.FancyArrowPatch(
                x1y1,
                x2y2,
                arrowstyle=arrowstyle,
                **arrow_kwargs)
        if color == 'rand':
            color = np.random.rand(3)
        arrow.set_facecolor(color)
        arrow.set_edgecolor(color)
        arrow.label = value

        vector = (x2y2-x1y1)
        angle = np.arctan2((vector[1]),vector[0])*180/np.pi
        angle = 180+angle if angle < 0 else angle
        if angle > 90:
            angle += 180
        self.connections.append([arrow,vector,angle])

        if value is not None:
            if randomness is not None:
                textpos = x1y1 + np.random.rand() * vector
            else:
                textpos=np.mean([x1y1,x2y2],axis=0)
            if np.any([ np.sum((T.xy-textpos)**2) < pad_length for T in self.axis.texts]):
                textpos += pad_length*vector
            # http://matplotlib.org/examples/pylab_examples/text_rotation_relative_to_line.html
            trans_angle = self.axis.transData.transform_angles(
                    np.array((angle,)), vector.reshape([1,2]))[0]
            
            txt = self.axis.annotate(str(value), textpos,
                    color=color,
                    bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.8),
                    ha='center',
                    va='center',
                    rotation=trans_angle)
            self.connections[-1].append(txt)

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

    def _repair_text_angles(self):
        for (arrow,vector,angle,txt) in self.connections:
            trans_angle = self.axis.transData.transform_angles(
                    np.array((angle,)), vector.reshape([1,2]))[0]
            txt.set_rotation(trans_angle)

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

