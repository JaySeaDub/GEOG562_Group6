from arcpy.sa import *
from arcpy import env

# arcpy workspace
env.workspace = r'R:\GEOG562\Students\sharrm\Lab7\Lab7_ArcProject\Group6_Lab7.gdb'

# file inputs
disturbance_raster = "forest_disturbance"
landsat_raster = "Landsat2001_Band4"

# temp input for testing
# year = '2002'

# Initiate a list to save statistics for each year
disturb_list = []

years = range(2002, 2013, 1)

for year in years:
    # create raster containing values for year of interest

    yearFileName = f'disturbance_{year}'  # Name the year's output file

    if not arcpy.Exists(yearFileName):
        dist_year = Con(Raster(disturbance_raster) == year, year)
        dist_year.save(yearFileName) # Save the output file

    # Calculate the mean value of the Band 4 pixels that overlap with the disturbance pixel for the current year
    Zonal_Statistics = yearFileName + '_statistics' # Name the output file

    if not arcpy.Exists(Zonal_Statistics):
        statsFile = ZonalStatistics(in_zone_data= Raster(yearFileName),    # From arcpy.sa
                                     zone_field="Value",
                                     in_value_raster= Raster(landsat_raster),
                                     statistics_type="MEAN",
                                     ignore_nodata="DATA",
                                     process_as_multidimensional="CURRENT_SLICE",
                                     percentile_value=90,
                                     percentile_interpolation_type="AUTO_DETECT")
        statsFile.save(Zonal_Statistics)

    else:
        statsFile = Zonal_Statistics

    # # This structure recommended by Jack to pull the mean from the statistics raster did not work:
    # mean_value = statsFile[0][4]

    # We could try to adapt the search cursor from Lab 5. This setup wants vector fields. I am
    # not sure what the raster equivalent would be
    mean_value = []
    with arcpy.da.SearchCursor(statsFile, Field) as rows:
        for r in rows:  # Iterate through the features of the shapefile (i.e. rows in attribute table)
            mean_value.append(r[4]) # r[4] = mean

    output_tuple = (year, mean_value)

   
