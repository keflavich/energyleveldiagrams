import astroquery.nist

Q = astroquery.nist.NISTAtomicLinesQuery()
NIST_Table = Q.query_line_html('H I',4000,7000,wavelength_unit='A',energy_level_unit='eV')

H = EnergyLevelDiagram()

for line in NIST_Table:
    if len(line['Lower LevelConf.']) > 1: 
        H.add_level(line['EieV'],line['Lower LevelConf.'][1],name=line['Lower LevelConf.']+line['LowerTerm']+line['LowerJ'])
    if len(line['Upper LevelConf.']) > 1: 
        H.add_level(line['EkeV'],line['Upper LevelConf.'][1],name=line['Upper LevelConf.']+line['UpperTerm']+line['UpperJ'])

