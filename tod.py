# TODO
# Add TOD object tour
# Add options to get_tod


import moby2
from matplotlib import pyplot as plt

# Load the filebase
# It knows where the TODs live on your system from the -moby2 configuration file
fb = moby2.scripting.get_filebase()

# Load TOD object
obs = '1435149664.1435180322.ar2'
filename = fb.filename_from_name(obs,single=True)
tod = moby2.scripting.get_tod({'filename':filename})


# Remove mean value for the TOD (no physical meaning)
# and detrend it (substract a straight line to match beginning and end point).
# Trend is coming from thermal drift; removing it helps with Fourier transforms
moby2.tod.remove_mean(tod)
moby2.tod.detrend_tod(tod)



# Useful options for get_tod:
# - 'read_data': if False, will create the TOD object and load everything except
#                for the data. Useful if you just want to access pointing for
#                example.
# - 'repair_pointing': if True, fix glitches in pointing and ctimes
# - 'fix_sign': if True, will fix the inverted detectors
# - 'det_uid': load only some detectors


# For most uses, you should always set 'repair_pointing' and 'fix_sign' to True.
tod = moby2.scripting.get_tod(
    {'filename':filename,
     'repair_pointing':True,
     'fix_sign':True})




# Plot all detectors
plt.plot(tod.data.T, 'b', alpha=0.1)


