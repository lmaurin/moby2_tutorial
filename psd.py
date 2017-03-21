import moby2
import numpy as np
from moby2.analysis.tod_ana import tools, visual
from matplotlib import pyplot as plt


fb = moby2.scripting.get_filebase()
# Load TOD object
obs = '1435149664.1435180322.ar2'
filename = fb.filename_from_name(obs,single=True)

tod = moby2.scripting.get_tod(
    {'filename':filename,
     'repair_pointing':True,
     'fix_sign':True})

moby2.tod.remove_mean(tod)
moby2.tod.detrend_tod(tod)
 

# Compute and plot the PSD for detector 1
ps, nu, w = tools.power(tod.data[1], dt=np.diff(tod.ctime).mean())
plt.loglog(nu, ps)


# Waterfall plot of PSD for the whole array
wf = visual.freqSpaceWaterfall(todfmin=0.001,fmax=100)
wf.plot()
# For better visualization, you might want to apply calibration and/or cuts

# The frequency bins are stroed in wf.matfreqs and the PSDs in wf.mat
# Note that plotting loglog(wf.matfreqs, wf.mat[1]) should be equivalent
# to using the tools.power() if binning is matched






# Waterfall 
