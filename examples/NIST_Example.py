import astroquery.nist
import energyleveldiagrams
import pylab

def nist_grotrian(minwav,maxwav,savefile=None):
    Q = astroquery.nist.NISTAtomicLinesQuery()
    NIST_Table = Q.query_line_html('H I',minwav,maxwav,wavelength_unit='A',energy_level_unit='eV')

    H = energyleveldiagrams.EnergyLevelDiagram()

    for line in NIST_Table:
        if len(line['Lower LevelConf.']) > 1: 
            lower_name = line['Lower LevelConf.']+line['LowerTerm']+line['LowerJ']
            H.add_level(line['EieV'],line['Lower LevelConf.'][1],name=lower_name)
        if len(line['Upper LevelConf.']) > 1: 
            upper_name = line['Upper LevelConf.']+line['UpperTerm']+line['UpperJ']
            H.add_level(line['EkeV'],line['Upper LevelConf.'][1],name=upper_name)
        if 'nan' not in upper_name and 'nan' not in lower_name:
            H.connect_levels(upper_name,lower_name, value="%6.1f" % line['RitzWavelengthVac'],color='rand')

    H.plot_levels()
    #H._repair_text_angles()

    if savefile is not None:
        pylab.savefig(savefile,bbox_inches='tight')


if __name__ == "__main__":
    nist_grotrian(6000,7000,'Halpha_Grotrian.png')
    nist_grotrian(4000,19000,'H234_Grotrian.png')
