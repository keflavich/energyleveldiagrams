import astroquery.nist
import energyleveldiagrams

Q = astroquery.nist.NISTAtomicLinesQuery()
NIST_Table = Q.query_line_html('H I',4000,7000,wavelength_unit='A',energy_level_unit='eV')

H = energyleveldiagrams.EnergyLevelDiagram()

for line in NIST_Table:
    if len(line['Lower LevelConf.']) > 1: 
        lower_name = line['Lower LevelConf.']+line['LowerTerm']+line['LowerJ']
        H.add_level(line['EieV'],line['Lower LevelConf.'][1],name=lower_name)
    if len(line['Upper LevelConf.']) > 1: 
        upper_name = line['Upper LevelConf.']+line['UpperTerm']+line['UpperJ']
        H.add_level(line['EkeV'],line['Upper LevelConf.'][1],name=upper_name)
    if 'nan' not in upper_name and 'nan' not in lower_name:
        H.connect_levels(upper_name,lower_name, value="%6.1f" % line['RitzWavelengthVac'])

H.plot_levels()

import pylab
pylab.show()

#hydrogen.connect_levels('4d','2p',linewidth=(np.log10(A4d2p)-np.min(logavals)+1)/logavals.ptp()*3, value="%e" % A4d2p)
