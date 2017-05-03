This is an exercise to check our calibration using Uranus observations. To do it, you will use moby2 tools explained in previous tutorials.

## 1. Identify Uranus observations
Using the database, identify all the Uranus TODs for a given array (e.g. AR2) and a given season (e.g. 2015). Output the list to a txt file.

## 2. Load the calibration
For all these TODs, you can load the calibration factors for all detectors. To access them, you will need a depot (on PUC system, /data/actpol/depot) and a tag (you can try the Bias Step calibration 'actpol2_2015_biasstep' or the atmosphere corrected calibration 'MR1_PA2_2015').

## 3. Load the Uranus peak amplitude measurements.
 Matthew Hasselfield computed per detector and per TOD planet peak amplitudes. On PUC system, you will find the results in /data/actpol/planet_cal. Inside the directory, for each TOD, there is a .fits and a .txt file containing columns with detector uid (det_uid), planet amplitude in DAQ units (U_dac), planet amplitude in IV calibrated pW (U_pW), calibration factor from DAQ units to uK (dac_to_uK) and from pW to uK (pW_to_uK). The calibration factors to uK are computed based on the expected temperature of Uranus (model).

## 4. Relative calibration between detectors.
For an individual observation, check the dispersion between detectors. It will give you an estimation of our relative calibration.

## 5. Relative calibration between TODs.
Compare the results from one TOD to the other. This will give you the time variation of our calibration.

## 6. Correct for the atmosphere transmission.
Actually, when you compare two TODs taken with different atmospheric conditions (PWV and elevation of the telescope), you don't expect them to give you the same result, because of the atmosphere transmission. Plotting the planet amplitude vs loading (PWV/sin(alt)) should show an atenuation of the signal when the loading is high. In theory, you could model that as the atmosphere transmission. In practice, there might also be a calibration dependance on loading that is degenerated with the atmosphere transmission, so we will just fit a simple linear model through the data to be used for absolute calibration.