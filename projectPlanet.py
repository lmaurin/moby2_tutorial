import moby2
import os, sys, time
import moby2.scripting.products as products
import numpy as np
import pylab
import moby2.mapping.fits_map as fits_map
from moby2.instruments import actpol
from moby2.util.database import TODList
import warnings
warnings.simplefilter('ignore', np.RankWarning)

db = actpol.TODDatabase()
fb = moby2.scripting.products.get_filebase()

pf = sys.argv[1]
params = moby2.util.MobyDict.from_file(pf)

if ~os.path.isdir(params["outPath"]): os.makedirs(params["outPath"])

todFile = '/data/actpol/season1/merlin/13821/1382157635.1382157700.ar1'

removeCommonMode=True
removePoly=True

params_loadtod = {
    'filename':todFile,
    'fix_sign':True,
    'repair_pointing':True
    }
tod = moby2.scripting.get_tod(params_loadtod)

# Cuts
depot = moby2.util.Depot( params['tod_cuts']['depot']['path'] )
cuts = depot.read_object( moby2.TODCuts, tag=params['tod_cuts']['tag'], tod=tod )
all_det_uid = tod.info.array_data.select_outer()
tod.cuts = cuts.copy( det_uid=tod.det_uid )
live_dets = tod.cuts.get_uncut()
moby2.tod.fill_cuts( tod )
#detector offsets
fp = moby2.scripting.products.get_focal_plane(params['pointing'], det_uid=all_det_uid, 
						tod_info=tod.info, tod=tod)
tod.fplane = fp

moby2.tod.ops.detrend_tod( tod )
moby2.tod.remove_mean( tod )

tau = products.get_time_constants(params['time_constants'], tod.info)
taus = tau.get_property('tau', tod.det_uid, default=0.)[1]
moby2.tod.prefilter_tod(tod, time_constants=taus)

ld = live_dets
## Calibration
# Calibration to pW (atmospheric calib)
cal_vect = products.get_calibration( params['calibration'], tod.info )
tod.data[ld] *= cal_vect.cal[ld][:,None]
# Absolute calib to uK
f = open( '/home/radio/depot/TODAbsCal/todcal_140130_c4_cal1.txt', 'r' )
lines = f.readlines()
f.close()
tods = np.array( [l.split()[0] for l in lines if l[0] != '#'] )
abscal = np.array( [l.split()[1] for l in lines if l[0] != '#'],
				         dtype = np.float64 )
tod.data *= abscal[tods==tod.info.basename]
	
#moby2.tod.filters.sine2lowPass( tod, fc=80., nsamps=tod.nsamps )

dark_dets = np.where( tod.info.array_data['det_type'] == 'dark_squid' )[0]
#remove common mode
if removeCommonMode:
	cm = moby2.tod.data_mean_axis0( tod.data, live_dets )
	dcm = moby2.tod.data_mean_axis0( tod.data, dark_dets )
	coef = np.dot( tod.data, cm )/np.dot( cm, cm )
	dcoef = np.dot( tod.data, dcm )/np.dot( dcm, dcm )
	for d in live_dets:
		tod.data[d] -= cm*coef[d]
		tod.data[d] -= dcm*dcoef[d]

#detect turnarounds, fit poly in segments, remove them
if removePoly:
	daz = 0.2*np.pi/180
	maxAz = tod.az.max() - daz
	minAz = tod.az.min() + daz
	cutArray = ( tod.az > minAz )*( tod.az < maxAz )
	idx = np.where( cutArray )
	segIdx = np.array_split( idx[0], np.where( np.diff(idx[0]) != 1)[0]+1 )

	for seg in segIdx:
		for d in live_dets:
			z = np.polyfit( tod.ctime[seg], tod.data[d][seg], 3 )
			p = np.poly1d( z )
			tod.data[d][seg] -= p( tod.ctime[seg] )

#Find position of the source
ra, dec = moby2.ephem.get_source_coords( 'uranus', tod.ctime.mean() )
print 'uranus at', ra, dec
# Changed the ephem output, apparently!
#wand = moby2.pointing.ArrayWand.for_tod_source_coords( tod, ref_coord=(ra[0],dec[0]), 
#			scan_coords=True, polarized=True )
wand = moby2.pointing.ArrayWand.for_tod_source_coords( tod, ref_coord=(ra,dec), 
			scan_coords=True, polarized=True )

s = tod.fplane.mask
x0, y0 = wand.fcenter.x[0], wand.fcenter.y[0]
x, y = tod.fplane.x[s] - x0, tod.fplane.y[s] - y0
			
r_max = np.max(x**2 + y**2)**.5 * 1.05
theta = np.arange(0., 2*np.pi, 20)
cplane = moby2.pointing.FocalPlane(x=r_max*np.cos(theta)+x0,
                                   y=r_max*np.sin(theta)+y0, 
                                   det_uid=all_det_uid)
x, y = wand.get_coords(cplane)[:2]
x, y = x * 180./np.pi, y * 180./np.pi
map_params = params["maps"][0][1]
map_lims = [(x.min(), x.max()), (y.min(), y.max())]
base_map = products.map_from_spec(map_params, map_lims)
grid = moby2.pointing.GridPixelization.forFitsMap( base_map )
proj_gen = moby2.pointing.WandProjector(wand, grid, tod.fplane)
#intensity map
proj_gen.project_to_map( tod.data, output=base_map.data, 
			 weights_output=base_map.weight, cuts=tod.cuts )
base_map.write( '%s/%s.fits'%(params["outPath"], tod.info.basename), force=True )
