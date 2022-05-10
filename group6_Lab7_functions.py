from arcpy.sa import *
from arcpy import env

# arcpy workspace
env.workspace = r'R:\GEOG562\Students\sharrm\Lab7\Lab7_ArcProject\Group6_Lab7.gdb'

# file inputs
disturbance_raster = "forest_disturbance"
landsat_raster = "LE7046049_2001_2007_corvsubset_Band_4"

# temp input for testing
# year = '2006'

# Initiate a list to save statistics for each year
disturb_list = []

years = range(2002, 2013, 1)

for year in years:
    # create raster containing values for year of interest
    dist_year = Con(Raster(disturbance_raster) == year, year)
    yearFileName = f'disturbance_{year}' # Name the output file
    dist_year.save(yearFileName) # Save the output file
    
    # Calculate the mean value of the Band 4 pixels that overlap with the disturbance pixel for the current year
    Zonal_Statistics = yearFileName + '_statistics' # Name the output file

    statsFile  = ZonalStatistics(in_zone_data= yearFileName,    # From arcpy.sa
                                 zone_field="Value",
                                 in_value_raster= landsat_raster,
                                 statistics_type="MEAN",
                                 ignore_nodata="DATA",
                                 process_as_multidimensional="CURRENT_SLICE",
                                 percentile_value=90,
                                 percentile_interpolation_type="AUTO_DETECT")
    statsFile.save(Zonal_Statistics)
    
    mean_value = statsFile[0][4]

    output_tuple = (year, mean_value)

    disturb_list.append(output_tuple)
    
print(disturb_list)
    
