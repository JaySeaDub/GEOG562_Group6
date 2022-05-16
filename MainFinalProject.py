########################################
# This is the Main section of the code for Group 6's final project in GEOG 462
# Group Members include Matthew Sharr, Jasen White, and Juliana Wold.

# Link to the functions Python file:
import Final_Project_Functions as funct

########################################
# In this first section, the user will be asked to input the file paths for the BLUE imagery tif file followed by
# The GREEN imagery tif file. Each of these files will be converted into Numpy arrays using the function pil_to_numpy()
# and be returned to the Main function for further processing

#*#*#*#* BLUE BAND #*#*#*#*
# Solicit the file path from the user
print("The file containing the BLUE band data will be identified by a wavelength close to 490nm.")
blueBand = input(r"Please enter the file path and name for the BLUE imagery band:")

# Convert the user identified file into an array:
blueArrayOutput = funct.pil_to_numpy(blueBand)

# Check to make sure that the function worked using its T/F output. If it did, save only the array
if blueArrayOutput[0]:
    blueArray = blueArrayOutput[1]
else:
    print("Unable to convert the BLUE band tif file to a Numpy array.")


#*#*#*#* GREEN BAND #*#*#*#*
# Solicit the file path from the user
print("The file containing the GREEN band data will be identified by a wavelength close to 560nm.")
greenBand = input(r"Please enter the file path and name for the GREEN imagery band:")

# Convert the user identified file into an array:
greenArrayOutput = funct.pil_to_numpy(greenBand)

# Check to make sure that the function worked using its T/F output. If it did, save only the array
if greenArrayOutput[0]:
    greenArray = greenArrayOutput[1]
else:
    print("Unable to convert the GREEN band tif file to a Numpy array.")

print(f"\nThe blue array looks like this:\n {blueArray}")

print(f"\nThe green array looks like this: \n{greenArray}\n")

# End of section to import raster tif files as arrays.
######################################################


######################################################
# This section will conduct a band math operation on the blue and green arrays completed in the section immediately prior.

