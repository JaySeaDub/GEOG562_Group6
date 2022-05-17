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

# Identify the years that we will iterate through to calclulate the means
years = range(2002, 2013, 1)

# Use a for loop to extract each applicable year from the Landsat Data, calcluate the statistics, and output to the disturb_list
for year in years:
    
    # Name the raster containing values for year of interest
    yearFileName = f'disturbance_{year}'  # Name the year's output file

    # Check to see if the current year's raster file already exists, if not, create it.
    if not arcpy.Exists(yearFileName):
        dist_year = Con(Raster(disturbance_raster) == year, year)
        dist_year.save(yearFileName) # Save the output file

    # Calculate the mean value of the Band 4 pixels that overlap with the disturbance pixel for the current year
    Zonal_Statistics = yearFileName + '_statistics_table' # Name the output file

    # Check to see if the current year's zonal statistics file already exists. If not, create it, and if yes, identify the file as the statsFile.
    if not arcpy.Exists(Zonal_Statistics):
        statsFile = arcpy.ia.ZonalStatisticsAsTable(in_zone_data= Raster(yearFileName),
                                                    zone_field="Value",
                                                    in_value_raster= Raster(landsat_raster),
                                                    out_table=Zonal_Statistics,
                                                    ignore_nodata="DATA",
                                                    statistics_type="MEAN",
                                                    process_as_multidimensional="CURRENT_SLICE",
                                                    percentile_values=[90],
                                                    percentile_interpolation_type="AUTO_DETECT")


    else:
        statsFile = Zonal_Statistics

    print(f"Completed creating the table file: {statsFile}")

    # From: https://pro.arcgis.com/en/pro-app/2.8/arcpy/mapping/table.htm
    # This is not quite working yet
    # yearTable = arcpy.mp.Table(statsFile)


    # This structure recommended by Jack to pull the mean from the statistics raster did not work:
    # mean_value = statsFile[0][4]

    # We could try to adapt the search cursor from Lab 5. This setup wants vector fields. I am
    # not sure what the table equivalent would be
    # mean_value = []
    # with arcpy.da.SearchCursor(statsFile, field_names= 'MEAN') as rows:
    #     for r in rows:  # Iterate through the features of the shapefile (i.e. rows in attribute table)
    #         mean_value.append(r[4]) # r[4] = mean

    # output_tuple = (year, mean_value)
    #
    # disturb_list.append(output_tuple)


# Compile a list of tables created during the previous for loop
# Technique from: https://gis.stackexchange.com/questions/130240/opening-table-from-file-geodatabase-in-arcpy
datasetList = arcpy.ListTables("*")

# Extract values from each table in the table list and append the values to a new  list
tableOfMeans = []
for dataset in datasetList:
     with arcpy.da.SearchCursor(dataset, "*") as cur:
          for row in cur:
             tableOfMeans.append(row)

# Show the user what the statistics outputs are
print(tableOfMeans)

#create blank list and use for loop to grab just year and mean, append them to the blank list
meanAndYear = []
for i in tableOfMeans:
    meanAndYear.append(i[1])
    meanAndYear.append(i[4])

print(meanAndYear)

#make values in meanAndYear list str
meanAndYear = [str(x) for x in meanAndYear]

#make variable as output textfile and write to that textfile using a for loop
outfilename = 'lab7textfile.txt'

# Open the new text file as writable
output_file = open(outfilename, 'w')

# Iterate through each variable in the list to write it out to the new file
for values in meanAndYear:
    output_file.write(values + "\n")

#close textfile and make a print statement saying where the file is.
output_file.close()

# Tell the user what the new file is named
print(f'The file can be found at {outfilename}')
