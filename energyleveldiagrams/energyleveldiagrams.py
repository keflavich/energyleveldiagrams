"""Energy Level Diagram (Grotrian Diagram) plotting module.

This module provides functionality to create and plot energy level diagrams,
commonly used in atomic physics and spectroscopy.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from collections import defaultdict
import itertools


class EnergyLevel:
    """Represents a single energy level in the diagram.
    
    Attributes:
        energy: The energy value of the level
        orbital: The orbital type (s, p, d, f, g)
        name: Optional name for the level
    """
    
    def __init__(self, energy, orbital, name=None):
        self.energy = energy
        self.orbital = orbital
        if name is None:
            name = f"{energy}{orbital}"
        self.name = name


class EnergyLevelDiagram:
    """Main class for creating and plotting energy level diagrams.
    
    This class handles the creation and manipulation of energy level diagrams,
    including adding levels, connecting them with transitions, and plotting.
    """
    
    def __init__(self, figure=None):
        """Initialize the energy level diagram.
        
        Args:
            figure: Optional matplotlib figure to use. If None, creates a new one.
        """
        self.figure = plt.figure() if figure is None else figure
        self.levels = {}
        self.orbitals = ['s', 'p', 'd', 'f', 'g']
        self.lines = []
        self.arrows = []
        self.connections = []

        self.orbital_colors = defaultdict(
            lambda: 'cyan',
            {'s': 'black',
             'p': 'blue',
             'd': 'red',
             'f': 'green',
             'g': 'orange'}
        )

        self.orbital_xrange = defaultdict(
            lambda: (0.1, 0.9),
            [(oo, [ii+0.1, ii+1-0.1]) for ii, oo in enumerate(self.orbitals)]
        )

    @property
    def axis(self):
        """Get the current matplotlib axis."""
        return self.figure.gca()

    def add_level(self, energy, orbital, name=None):
        """Add a new energy level to the diagram.
        
        Args:
            energy: The energy value of the level
            orbital: The orbital type (s, p, d, f, g)
            name: Optional name for the level
        """
        el = EnergyLevel(energy, orbital, name)
        self.levels[el.name] = el

    def plot_levels(self):
        """Plot all energy levels as horizontal lines."""
        self.lines = [
            self.axis.plot(
                self.orbital_xrange[el.orbital],
                [el.energy, el.energy],
                color=self.orbital_colors[el.orbital]
            )
            for (_, el) in self.levels.items()
        ]

    def connect_levels(
        self,
        levelname1,
        levelname2,
        value=None,
        arrowstyle='-|>,head_width=5,head_length=10',
        color='k',
        pad_length=0.1,
        randomness=0.1,
        **arrow_kwargs
    ):
        """Connect two energy levels with an arrow representing a transition.
        
        Args:
            levelname1: Name of the first level
            levelname2: Name of the second level
            value: Optional value to display along the transition
            arrowstyle: Style of the arrow
            color: Color of the arrow
            pad_length: Padding for text placement
            randomness: Amount of random offset for arrow endpoints
            **arrow_kwargs: Additional arguments for arrow styling
        """
        lev1 = self.levels[levelname1]
        lev2 = self.levels[levelname2]
        x1y1 = np.array((np.mean(self.orbital_xrange[lev1.orbital]), lev1.energy))
        x2y2 = np.array((np.mean(self.orbital_xrange[lev2.orbital]), lev2.energy))
        
        if randomness is not None:
            x1y1[0] += np.random.randn() * randomness
            x2y2[0] += np.random.randn() * randomness
            
        arrow = mpl.patches.FancyArrowPatch(
            x1y1,
            x2y2,
            arrowstyle=arrowstyle,
            **arrow_kwargs
        )
        
        if color == 'rand':
            color = np.random.rand(3)
            
        arrow.set_facecolor(color)
        arrow.set_edgecolor(color)
        arrow.label = value

        vector = (x2y2 - x1y1)
        angle = np.arctan2(vector[1], vector[0]) * 180 / np.pi
        angle = 180 + angle if angle < 0 else angle
        if angle > 90:
            angle += 180
            
        self.connections.append([arrow, vector, angle])

        if value is not None:
            if randomness is not None:
                textpos = x1y1 + np.random.rand() * vector
            else:
                textpos = np.mean([x1y1, x2y2], axis=0)
                
            if any(np.sum((T.xy - textpos)**2) < pad_length for T in self.axis.texts):
                textpos += pad_length * vector
                
            trans_angle = self.axis.transData.transform_angles(
                np.array((angle,)), vector.reshape([1, 2]))[0]
            
            txt = self.axis.annotate(
                str(value),
                textpos,
                color=color,
                bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.8),
                ha='center',
                va='center',
                rotation=trans_angle
            )
            self.connections[-1].append(txt)

        self.axis.add_patch(arrow)
        self.arrows.append(arrow)

    def energy_connect(
        self,
        levelname1,
        levelname2,
        xpos=0,
        arrowstyle='-|>,head_width=5,head_length=10',
        color='k',
        pad_length=0.1,
        label=None,
        textkwargs=None,
        **arrow_kwargs
    ):
        """Connect two energy levels with a vertical energy transition.
        
        Args:
            levelname1: Name of the first level
            levelname2: Name of the second level
            xpos: X-position for the vertical transition
            arrowstyle: Style of the arrow
            color: Color of the arrow
            pad_length: Padding for text placement
            label: Optional label for the transition
            textkwargs: Additional arguments for text styling
            **arrow_kwargs: Additional arguments for arrow styling
        """
        if textkwargs is None:
            textkwargs = {}
            
        lev1 = self.levels[levelname1]
        lev2 = self.levels[levelname2]
        x1y1 = (xpos, lev1.energy)
        x2y2 = (xpos, lev2.energy)
        
        arrow = mpl.patches.FancyArrowPatch(
            x1y1,
            x2y2,
            arrowstyle=arrowstyle,
            **arrow_kwargs
        )
        
        arrow.set_facecolor(color)
        arrow.set_edgecolor(color)
        
        if label is None:
            arrow.label = f"{lev1.energy - lev2.energy:.3f}"
        else:
            arrow.label = label

        textpos = np.mean([x1y1, x2y2], axis=0)
        if any(np.sum((T.xy - textpos)**2) < pad_length for T in self.axis.texts):
            textpos += pad_length
            
        txt = self.axis.annotate(
            str(arrow.label),
            textpos,
            color=color,
            bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.8),
            **textkwargs
        )

        self.axis.add_patch(arrow)
        self.arrows.append(arrow)

    def _repair_text_angles(self):
        """Repair text angles after figure resizing."""
        for (arrow, vector, angle, txt) in self.connections:
            trans_angle = self.axis.transData.transform_angles(
                np.array((angle,)), vector.reshape([1, 2]))[0]
            txt.set_rotation(trans_angle)

    def _fix_labels(self, pad_length=1):
        """Fix overlapping labels (currently not implemented)."""
        # TODO: Implement label overlap fixing
        pass

