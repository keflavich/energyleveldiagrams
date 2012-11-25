import astroquery.nist
import energyleveldiagrams
import pylab as pl
import numpy as np

def nist_grotrian(minwav,maxwav,**kwargs):
    Q = astroquery.nist.NISTAtomicLinesQuery()
    NIST_Table = Q.query_line_html('H I',minwav,maxwav,wavelength_unit='A',energy_level_unit='eV')

    return plot_nist_grotrian(NIST_Table, **kwargs)

def plot_nist_grotrian(NIST_Table, savefile=None,
        connection='RitzWavelengthVac', lowerSelect='', upperSelect='',
        merge_fine=sum, color='rand', vformat="%6.1f"):

    H = energyleveldiagrams.EnergyLevelDiagram()
    H.axis.set_xticks([0.5,1.5,2.5,3.5])
    H.axis.set_xticklabels(['s','p','d','f'])

    if merge_fine is not None:
        unique_lines = np.unique([a+","+b for a,b in zip(NIST_Table['Lower LevelConf.'],NIST_Table['Upper LevelConf.'])])
        level_values = dict([(ln,[]) for ln in unique_lines if lowerSelect in ln and upperSelect in ln])

    for line in NIST_Table:
        if len(line['Lower LevelConf.']) > 1: 
            if merge_fine:
                lower_name = line['Lower LevelConf.']
            else:
                lower_name = line['Lower LevelConf.']+line['LowerTerm']+line['LowerJ']
            H.add_level(line['EieV'],line['Lower LevelConf.'][1],name=lower_name)
        else:
            lower_name = ''
        if len(line['Upper LevelConf.']) > 1: 
            if merge_fine:
                upper_name = line['Upper LevelConf.']
            else:
                upper_name = line['Upper LevelConf.']+line['UpperTerm']+line['UpperJ']
            H.add_level(line['EkeV'],line['Upper LevelConf.'][1],name=upper_name)
        else:
            upper_name = ''
        if upperSelect is not None and upperSelect not in upper_name:
            #print "upper skip ",lower_name,upperSelect," not in ",upper_name,
            continue
        if lowerSelect is not None and lowerSelect not in lower_name:
            #print "lower skip ",lowerSelect," not in ",lower_name,upper_name,
            continue
        if upper_name == "" or lower_name == "":
            continue
        if merge_fine is None:
            if 'nan' not in upper_name and 'nan' not in lower_name:
                H.connect_levels(upper_name,lower_name, value=vformat % line[connection],color=color)
        else:
            level_values[(lower_name+","+upper_name)].append(line[connection])

    if merge_fine:
        for name,vlist in level_values.iteritems():
            lower_name, upper_name = name.split(",")
            #print name,lower_name,upper_name,merge_fine(vlist),vlist
            if lower_name == 'na' or upper_name == 'na' or len(lower_name)<2 or len(upper_name)<2:
                continue
            value = merge_fine(vlist)
            H.connect_levels(upper_name,lower_name, value=vformat % value,color=color)

    H.plot_levels()
    #H._repair_text_angles()
    pl.xlabel("Orbital")
    pl.ylabel("Energy (eV)")

    if savefile is not None:
        pl.savefig(savefile,bbox_inches='tight')

    return NIST_Table


if __name__ == "__main__":
    NTlow = nist_grotrian(6000,7000,savefile='Halpha_Grotrian.png',merge_fine=None)
    pl.title('Halpha_Grotrian')
    NThigh = nist_grotrian(4000,19000,savefile='H234_Grotrian.png',merge_fine=None)
    pl.title('H234_Grotrian')
    plot_nist_grotrian(NThigh,savefile='H234_Grotrian_avals.png',vformat="%0.1e",connection='Akis-1')
    pl.title('H234_Grotrian_avals')
    plot_nist_grotrian(NThigh,savefile='H234_Grotrian_only2p.png',vformat="%0.1e",connection='Akis-1',lowerSelect='2p',color='k')
    pl.title('H234_Grotrian_only2p_avals')
    plot_nist_grotrian(NThigh,savefile='H234_Grotrian_only3s.png',vformat="%0.1e",connection='Akis-1',lowerSelect='3s',color='k')
    pl.title('H234_Grotrian_only3s_avals')
    plot_nist_grotrian(NThigh,savefile='H234_Grotrian_only3p.png',vformat="%0.1e",connection='Akis-1',lowerSelect='3p',color='k')
    pl.title('H234_Grotrian_only3p_avals')
    plot_nist_grotrian(NThigh,savefile='H234_Grotrian_only3d.png',vformat="%0.1e",connection='Akis-1',lowerSelect='3d',color='k')
    pl.title('H234_Grotrian_only3d_avals')

    pl.show()
