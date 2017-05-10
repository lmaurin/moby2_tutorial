import moby2
from matplotlib import pyplot as plt
from moby2.analysis.tod_ana import visual as v
import numpy as np
fb = moby2.scripting.get_filebase()
plt.ioff()


obs = '1447819012.1447878227.ar2'
tag_cuts = 'MR1_PA2_2015'
tag_cal = 'MR1_PA2_2015'
depot_path = '/data/actpol/depot'


# Load the TOD
filename = fb.filename_from_name(obs,single=True)
tod = moby2.scripting.get_tod(
    {'filename':filename,
     'repair_pointing':True})
moby2.tod.remove_mean(tod)
moby2.tod.detrend_tod(tod)






# Load the cuts
cuts = moby2.scripting.get_cuts(
    {'depot':depot_path,
     'tag':tag_cuts},
    tod=tod)
tod.cuts = cuts

# Check the live and dead detectors
ld = cuts.get_uncut()
plt.figure()
for d in ld[:15]:
    plt.plot(tod.ctime-tod.ctime[0], tod.data[d], alpha=0.5)
    plt.ylim(-3e6,3e6)
    plt.xlabel('Time [s]')
    plt.ylabel('Data [DAQ units]')
    plt.title('%s - Live detectors' %tod.info.name)
dd = cuts.get_cut()
plt.figure()
for d in dd[:15]:
    plt.plot(tod.ctime-tod.ctime[0], tod.data[d], alpha=0.5)
    plt.ylim(-1e5,1e5)
    plt.xlabel('Time [s]')
    plt.ylabel('Data [DAQ units]')
    plt.title('%s - Dead detectors' %tod.info.name)



# Look at the sample cuts for one live detector
plt.figure()
v.plot_with_cuts(tod, ld[0], interactive=False)
plt.title('%s - d%.4i' %(tod.info.name, ld[0]))
plt.xlabel('Time [s]')

# Apply the cuts
plt.figure()
plt.plot(tod.ctime-tod.ctime[0],tod.data[ld[0]], 'b', label='Before cuts')

moby2.tod.fill_cuts(tod)

plt.plot(tod.ctime-tod.ctime[0],tod.data[ld[0]], 'g', label='After cuts')
plt.legend(loc='best', frameon=False)


plt.figure()
plt.plot(tod.ctime-tod.ctime[0], tod.data[ld].T, 'b', alpha=0.1)
plt.title('%s - Live dets - Uncalibrated' %(tod.info.name))
plt.xlabel('Time [s]')


# Apply the calibration
cal = moby2.scripting.get_calibration(
    {'type':'depot_cal',
     'depot': depot_path,
     'tag': tag_cal},
    tod=tod)
tod.data[cal.det_uid] *= cal.cal[:,np.newaxis]

plt.figure()
plt.plot(tod.ctime-tod.ctime[0], tod.data[ld].T, 'b', alpha=0.1)
plt.title('%s - Live dets - Calibrated' %(tod.info.name))
plt.xlabel('Time [s]')




plt.show()
