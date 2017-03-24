# TODO
# Add TOD object tour
# Add options to get_tod

import numpy as np
import moby2
from matplotlib import pyplot as plt

# Load the filebase
# It knows where the TODs live on your system from the -moby2 configuration file
fb = moby2.scripting.get_filebase()

# Load TOD object
obs = '1447819012.1447878227.ar2'
# obs = '1435149664.1435180322.ar2'
filename = fb.filename_from_name(obs,single=True)
tod = moby2.scripting.get_tod({'filename':filename})


print ""
print "Let's look at the fields in the TOD object:"
print " - tod.nsamps contains the number of samples (int) :",
print tod.nsamps
print " - tod.ctime contains the ctimes of all samples (Nsamp array)"
print " - tod.alt, tod.az contains the pointing of the telescope (Nsamp arrays)"
plt.figure()
plt.subplot(311)
plt.plot(tod.ctime)
plt.title(tod.info.name)
plt.ylabel('ctime [s]')
plt.subplot(312)
plt.plot(tod.alt*180/np.pi)
plt.ylabel('Altitude [deg]')
plt.subplot(313)
plt.plot(tod.az*180/np.pi)
plt.ylabel('Azimuth [deg]')
plt.show()
print ""
print "There is a glitch in the ctime, altitude and azimuth from readout. You can repair these using the opting 'repair_pointing' when loading the TOD."
raw_input("Press Enter to reload the TOD fixing the glitch")

tod = moby2.scripting.get_tod({'filename':filename,
                               'repair_pointing':True})
plt.clf()
plt.subplot(311)
plt.plot(tod.ctime)
plt.ylabel('ctime [s]')
plt.title(tod.info.name)
plt.subplot(312)
plt.plot(tod.alt*180/np.pi)
plt.ylabel('Altitude [deg]')
plt.subplot(313)
plt.plot(tod.az*180/np.pi)
plt.ylabel('Azimuth [deg]')
plt.xlabel('Sample #')
plt.draw()
print ""
raw_input("Press Enter to look at the data for a few detectors")

plt.clf()
for d in tod.det_uid[:16]:
    plt.plot(tod.ctime-tod.ctime[0],tod.data[d], alpha=0.5)
# plt.ylim(-5e5,5e5)
plt.title(tod.info.name) 
plt.xlabel('Time [s]')
plt.ylabel('Data [DAQ units]')
plt.draw()
print "The DC level of the TOD is different for each detector, but doesn't have any physical meaning, let's remove it with moby2.tod.remove_tod()"
raw_input("Press Enter to continue...")

moby2.tod.remove_mean(tod)
plt.clf()
for d in tod.det_uid[:16]:
    plt.plot(tod.ctime-tod.ctime[0],tod.data[d], alpha=0.5)
plt.ylim(-5e5,5e5)
plt.xlabel('Time [s]')
plt.ylabel('Data [DAQ units]')
plt.draw()
print ""
print "Some detectors are inverted. This is due to hardware reasons; if you want to correct for that, you can provide the argument 'fix_sign' when loading the TOD (let's do it)"
raw_input("Press Enter to continue...")


tod = moby2.scripting.get_tod(
    {'filename':filename,
     'repair_pointing':True,
     'fix_sign':True})
moby2.tod.remove_mean(tod)
plt.clf()
for d in tod.det_uid[:16]:
    plt.plot(tod.ctime-tod.ctime[0],tod.data[d], alpha=0.5)
plt.ylim(-5e5,5e5)
plt.title(tod.info.name) 
plt.xlabel('Time [s]')
plt.ylabel('Data [DAQ units]')
plt.draw()
print ""
print "Some detectors have a small amplitude and don't see the same signal as the others. Let's check what they are. tod.info.array_data contains many information about all detectors in the array (uid, position, orientation, etc) and in particular the type of detectors."
raw_input("Press Enter to continue...")

plt.clf()
for i,d in enumerate(tod.det_uid[:16]):
    plt.subplot(4,4,i+1)
    plt.plot(tod.ctime-tod.ctime[0],tod.data[d])
    plt.title( tod.info.array_data['det_type'][d] )
    plt.ylim(-5e5,5e5)
    plt.xticks([])
    plt.yticks([])
plt.draw()
print "Most of the bad looking detectors are dark detectors, they don't see the sky."
print "Let's just look at the tes detectors."
raw_input("Press Enter to continue...")

tes = tod.info.array_data['det_uid'][tod.info.array_data['det_type']=='tes']
plt.clf()
for d in tes[:16]:
    plt.plot(tod.ctime-tod.ctime[0],tod.data[d], alpha=0.5)
plt.ylim(-5e5,5e5)
plt.title(tod.info.name) 
plt.xlabel('Time [s]')
plt.ylabel('Data [DAQ units]')
plt.draw()
print ""
print "Some detectors see a strong slow drift. This is mostly due to thermal contamination. The information contained in the 1st mode (straight line) is not really relevant and it prevents from performing Fourier transform on the data. You can remove it using the moby2.tod.detrend_tod() function."
raw_input("Press Enter to detrend...")

moby2.tod.detrend_tod(tod)
plt.clf()
for d in tes[:16]:
    plt.plot(tod.ctime-tod.ctime[0],tod.data[d], alpha=0.5)
plt.ylim(-5e5,5e5)
plt.title(tod.info.name) 
plt.xlabel('Time [s]')
plt.ylabel('Data [DAQ units]')
plt.draw()


print "Still, some detectors look like they are not working. We also see glitches in some detectors and the amplitude varies a lot from one detector to another. You might want to check the cuts and cal tutorial."
print ""
print "Before that, let's look at"
raw_input("Press Enter to continue...")

plt.close('all')
