# from __future__ import division, print_function
# import os,sys
# sys.path.insert(0,'/Users/mandy/g2full/GSASII')
# import GSASIIscriptable as G2sc
#
# data = "./test/peaklist"
# PathWrap = lambda fil: os.path.join(data,fil)
# gpx = G2sc.G2Project(newgpx=PathWrap('pk.gpx'))
# hist = gpx.add_powder_histogram(PathWrap('MnO2_Unmilled_Air_InitialScan.xrdml'),
#                                 PathWrap('NC_Empyrean.prm'),
#                                 fmthint='GSAS powder')



from __future__ import division, print_function
import os,sys
sys.path.insert(0,'/Users/mandy/g2full/GSASII') # needed to "find" GSAS-II modules
import GSASIIscriptable as G2sc
datadir = "./test/peaklist"
PathWrap = lambda fil: os.path.join(datadir,fil)
gpx = G2sc.G2Project(newgpx=PathWrap('pkfit.gpx'))
hist = gpx.add_powder_histogram(PathWrap('FAP.XRA'), PathWrap('INST_XRY.PRM'),
                                fmthint='GSAS powder')
hist.set_refinements({'Limits': [16.,24.],
      'Background': {"no. coeffs": 2,'type': 'chebyschev-1', 'refine': True}
                     })
peak1 = hist.add_peak(1, ttheta=16.8)
peak2 = hist.add_peak(1, ttheta=18.9)
peak3 = hist.add_peak(1, ttheta=21.8)
peak4 = hist.add_peak(1, ttheta=22.9)
hist.set_peakFlags(area=True)
hist.refine_peaks()
hist.set_peakFlags(area=True,pos=True)
hist.refine_peaks()
hist.set_peakFlags(area=True, pos=True, sig=True, gam=True)
res = hist.refine_peaks()
print('peak positions: ',[i[0] for i in hist.PeakList])
for i in range(len(hist.Peaks['peaks'])):
    print('peak',i,'pos=',hist.Peaks['peaks'][i][0],'sig=',hist.Peaks['sigDict']['pos'+str(i)])
hist.Export_peaks('pkfit.txt')
#gpx.save()  # gpx file is not written without this