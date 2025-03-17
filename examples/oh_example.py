"""Example of creating an energy level diagram for OH molecule with hyperfine structure."""

import energyleveldiagrams
import numpy as np
import matplotlib.pyplot as plt
from astroquery.lamda import Lamda
from astropy import units as u


def parse_j_value(j_str):
    """Parse the J quantum number from the LAMDA format string.
    
    Args:
        j_str: String in format like '1.5_-_1' where the first number is the J value
        
    Returns:
        float: The J quantum number
    """
    return float(j_str.split('_')[0])


def main():
    # Query OH data from LAMDA database
    coll, trans, levs = Lamda.query('oh')
    
    # Create energy level diagram
    oh_eld = energyleveldiagrams.EnergyLevelDiagram()
    
    # Add energy levels with hyperfine splitting
    # We'll use the J value for the main level and F for hyperfine splitting
    for lev in levs:
        # Parse the J quantum number
        j_value = parse_j_value(lev['J'])
        
        # Convert energy from cm^-1 to GHz using astropy's spectral equivalencies
        energy_ghz = (lev['Energy'] * u.cm**-1).to(u.GHz, equivalencies=u.spectral()).value
        
        # Main rotational level
        oh_eld.add_level(
            energy=energy_ghz,
            orbital='s',  # Main rotational level
            name=f"J{j_value}"
        )
        
        # Add hyperfine levels (F = J ± 1/2)
        # We'll offset these horizontally
        f_levels = [j_value - 0.5, j_value + 0.5]
        for i, f in enumerate(f_levels):
            oh_eld.add_level(
                energy=energy_ghz,
                orbital='p',  # Use 'p' for hyperfine levels
                name=f"F{f}"
            )
    
    # Plot the levels
    oh_eld.plot_levels()
    
    # Connect the levels to show hyperfine structure
    for lev in levs:
        j_value = parse_j_value(lev['J'])
        j_level = f"J{j_value}"
        f_levels = [f"F{j_value - 0.5}", f"F{j_value + 0.5}"]
        
        # Connect main level to hyperfine levels
        for f_level in f_levels:
            oh_eld.connect_levels(
                j_level,
                f_level,
                value=f"F={f_level[1:]}",  # Show F value
                color='blue',
                arrowstyle='->'  # Simpler arrow style for hyperfine transitions
            )
    
    # Calculate max energy for axis limits
    max_energy_ghz = max((lev['Energy'] * u.cm**-1).to(u.GHz, equivalencies=u.spectral()).value for lev in levs)
    
    # Set axis limits and labels
    plt.axis([-0.1, 3, -2000, max_energy_ghz + 2000])  # Add some padding
    plt.xlabel("Orbital")
    oh_eld.axis.set_xticks([0.5, 1.5, 2.5])
    oh_eld.axis.set_xticklabels(['s', 'p', 'd'])
    plt.ylabel("Energy (GHz)")
    
    # Add title
    plt.title("OH Energy Levels with Hyperfine Structure")
    
    # Show the plot
    plt.show()


if __name__ == '__main__':
    main()
# 
# #hydrogen.connect_levels('4d','2s',value=)
# A4d2p = (2.0625e+07+1.7188e+07)
# A4d3p = (1.1729e+06+7.0376e+06+5.8647e+06)
# A4s2p = (8.5941e+05+1.7190e+06)
# A4p2s = (9.6680e+06+9.6683e+06)
# A4s3s = (3.0650e+06+3.0652e+06)
# A4p3d = (3.4754e+04+3.1280e+05+3.4759e+05)
# avals = A4d2p, A4d3p, A4s2p, A4p2s, A4s3s, A4p3d
# logavals = np.log10(avals)
# linewidths = ((logavals-logavals.min())/logavals.ptp()+1)
# print avals,np.log10(avals)
# 
# 
# hydrogen.connect_levels('4d','2p',linewidth=(np.log10(A4d2p)-np.min(logavals)+1)/logavals.ptp()*3, value="%e" % A4d2p)
# hydrogen.connect_levels('4d','3p',linewidth=(np.log10(A4d3p)-np.min(logavals)+1)/logavals.ptp()*3, value="%e" % A4d3p,color='r')
# hydrogen.connect_levels('4s','2p',linewidth=(np.log10(A4s2p)-np.min(logavals)+1)/logavals.ptp()*3,value="%e" % A4s2p)
# hydrogen.connect_levels('4p','2s',linewidth=(np.log10(A4p2s)-np.min(logavals)+1)/logavals.ptp()*3,value="%e" % A4p2s,color='b')
# hydrogen.connect_levels('4p','3s',linewidth=(np.log10(A4s3s)-np.min(logavals)+1)/logavals.ptp()*3,value="%e" % A4s3s,color='r')
# hydrogen.connect_levels('4p','3d',linewidth=(np.log10(A4p3d)-np.min(logavals)+1)/logavals.ptp()*3,value="%e" % A4p3d,color='g')
# hydrogen.energy_connect('4s','3s',label='Paschen $\\alpha$')
# hydrogen.energy_connect('4s','2s',xpos=2.95,label='Balmer $\\beta$', textkwargs={'ha':'right'})
# pl.axis([-0.1,3,-3.6,-0.6])
# pl.xlabel("Orbital")
# hydrogen.axis.set_xticks([0.5,1.5,2.5])
# hydrogen.axis.set_xticklabels(['s','p','d'])
# pl.ylabel("Energy (eV)")
# #hydrogen._fix_labels()
# 
# # NIST-based test...
# 
# 
# 
# 