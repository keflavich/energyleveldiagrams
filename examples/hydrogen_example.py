import energyleveldiagrams
import numpy as np
import pylab as pl

hydrogen = energyleveldiagrams.EnergyLevelDiagram()
rydberg = 13.6056925330

for nn  in xrange(1,10):
    for oo,orb in enumerate(hydrogen.orbitals):
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


