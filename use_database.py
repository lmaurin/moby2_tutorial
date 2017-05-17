from database import Database as DB


# Load the database (a year should be provided)
db = DB(2016)


# Let's have a look at the data available in the database:
print db.describbe('tods') # Informations about tods
print db.describbe('acqs') # Informations about all acquisitions

# First, we'll load tods information
db.load_tods() # Load the tods in db.tods
# db.tods is a Pandas dataframe and can be handled as such
print db.tods.columns
# Some particularly interesting fields are:
#    - array
#    - obs_type: type of observation (planet, scan (cmb observations), stare (telescope not moving)...)
#    - obs_detail: field of observation for scan tods, name of the planet, etc
#    - name: name of the TODs (ctime_start.ctime_merged.array)
#    - pwv
#    - *_alt, *_az: coordinates in alt/az
#    - *_RA, *_DEC: coordinates in RA/DEC


# Some statistics about the TODs
db.tods.array.value_counts()
db.tods.obs_type.value_counts()
db.tods.obs_detail.value_counts()




# Then, we'll load all acqs information
db.load_acqs() # Load the tods in db.acqs
# db.acqs is a Pandas dataframe and can be handled as such
print db.acqs.columns
# Some particularly interesting fields are:
#    - array
#    - ctime
#    - suffix: acquisition type (IV, Bias Step, data, etc)
#    - id: identifier (useful to match tod name with the tods database)



# Some statistics about the acqs
db.acqs.array.value_counts()
db.suffic.array.value_counts()






# load_tods() and load_acqs() are convenient, but it would better to be able to load
# from the SQL database only the data we are interested in. This can be done by passing
# queries to the SQL database.

# First, we initiate the query selecting either tods or acqs
db.create_query('tods')

# Then we can add conditions
db.add_condition(('array', '=', 'AR2'))
db.add_condition(('PWV', '<', '3'))
db.add_condition(('obs_detail', '=', 'uranus'))
# We only want array2 observations of uranus when PWV was lower than 3mm

# Now we can make the query to the database
db.make_query()

# The data will be stored in db.data
db.data.array.value_counts()
db.data.obs_detail.value_counts()
db.data.pwv.hist()
