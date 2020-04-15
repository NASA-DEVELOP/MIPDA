#Dependicies: 
#Install Anaconda
#Conda Environment (cheat sheet)
#source activate ~/py27
#Install archook (pip archook)
#Install numpy (pip numpy)

try:
		import archook #The module which locates arcgis
		archook.get_arcpy()
		import arcpy
except ImportError:
    ("Message: could not import arcpy")
import os
import shutil 
import numpy as np 
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

def main():
	step1() #good
	step2() #good
	step3() #good
	step4() #good
	step5("Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/ADS_Polygons/ADS_Subsets/BB_DTPA/DTPA_Top15prc/") #good
	# step6() #1/3rd good
	# step7() #no bueno
	step8() #good
	step9() #good

#___________________________________________________________________________________________________________________________________
#STEP 0: MOVING AND CREATING FOLDERS FROM FILENAMES

#Functions for Moving Files To Their Newly Created Folders Based on File Name:
def extractSatelliteName(filename):
	return filename[:3]

def extractDate(filename):
	return filename[3:21]

def createFolderFromFilename(workspace, filename):
	satellite = extractSatelliteName(filename)
	dateString = extractDate(filename)
	currentDir = workspace
	newFolderName = os.path.join(currentDir,satellite + dateString)
	print(newFolderName)
	if not os.path.exists(newFolderName):
		os.makedirs(newFolderName)
	return newFolderName

def functionThatMovesClippedFiles(destinationpath):
	currentFolder = destinationpath 
	for f in os.listdir(currentFolder):
		if not f.endswith("clipped.tif"):
			continue
		newFolderName = createFolderFromFilename(currentFolder,f)
		satellite = extractSatelliteName(f)
		dateString = extractDate(f)
		matchingName = satellite + dateString
		for file in os.listdir(currentFolder):
			if not file.endswith("clipped.tif"):
				continue
			satellite2 = extractSatelliteName(file)
			dateString2 = extractDate(file)
			if satellite == satellite2 and dateString == dateString2:
				originalFile = os.path.join(currentFolder,file)
				newFile = os.path.join(newFolderName,file)
				shutil.move(originalFile,newFile)


#___________________________________________________________________________________________________________________________________
#STEP 1: CLIPPING SCENES FOR LANDSAT 5, LANDSAT 7, and LANDSAT 8

def clippingLandsatScenes(curDir, studyArea, destinationpath):
  scenes = arcpy.ListWorkspaces()
  for scene in scenes:
    print(scene)
    arcpy.env.workspace = scene
    bandList = arcpy.ListRasters("*","TIF")
    for landsatBand in bandList:
      print landsatBand
      outRaster = (landsatBand.split(".")[0] + "_clipped.tif")
      studyAreaShapefile = studyArea
      if landsatBand.endswith("ndmi.tif") or landsatBand.endswith("cfmask.tif"): 
        arcpy.Clip_management(landsatBand,"#", outRaster, studyAreaShapefile, "#", "ClippingGeometry" , "NO_MAINTAIN_EXTENT") 
        source = os.listdir(scene)
        for clippedScene in source:
          if clippedScene.endswith("clipped.tif"):
            shutil.move(os.path.join(scene,clippedScene), os.path.join(destinationpath,clippedScene))

def step1():

	#Landsat5:
	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/LandsatScenes/Landsat5/RawScenes"
	destinationpath = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/LandsatScenes/Landsat5/ClippedScenes"
	studyArea = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/StudyArea_ShapeFiles/StudyArea/StudyArea_Env_4km_WGS84UTM.shp"
	curDir5 = arcpy.env.workspace
	arcpy.env.overwriteOutput = True

	clippingLandsatScenes(curDir5, studyArea, destinationpath)
	functionThatMovesClippedFiles(destinationpath)
	print("clipping Landsat5 completed")

	#Landsat7:
	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/LandsatScenes/Landsat7/RawScenes"
	destinationpath = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/LandsatScenes/Landsat7/ClippedScenes"
	studyArea = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/StudyArea_ShapeFiles/StudyArea/StudyArea_Env_4km_WGS84UTM.shp"
	curDir7 = arcpy.env.workspace
	arcpy.env.overwriteOutput = True

	clippingLandsatScenes(curDir7, studyArea, destinationpath)
	functionThatMovesClippedFiles(destinationpath)
	print("clipping Landsat7 completed")

	#Landsat8:
	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/LandsatScenes/Landsat8/RawScenes"
	destinationpath = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/LandsatScenes/Landsat8/ClippedScenes"
	studyArea = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/StudyArea_ShapeFiles/StudyArea/StudyArea_Env_4km_WGS84UTM.shp"
	curDir8 = arcpy.env.workspace
	arcpy.env.overwriteOutput = True

	clippingLandsatScenes(curDir8, studyArea, destinationpath)
	functionThatMovesClippedFiles(destinationpath)
	print("clipping Landsat8 completed")


#___________________________________________________________________________________________________________________________________
# #STEP 2: MASKING SCENES FOR LANDSAT 5, LANDSAT 7, and LANDSAT 8

def cloudMaskingLandsatScenes(curDir, destinationpath):
	folders = arcpy.ListWorkspaces()
	for folder in folders:
		arcpy.env.workspace = folder
		rasters = arcpy.ListRasters("*", "TIF")
		selectedRasters = rasters[1:]
		cloudmask = rasters[0]
		for raster in selectedRasters:
			if raster.endswith("ndmi_clipped.tif"):
				outNulled = Con(cloudmask, raster,"", "VALUE < 4")
				outputFileName = raster.split(".")[0] + "_cloudMask.tif"
				newFolderName = createFolderFromFilename(destinationpath, outputFileName)
				outputRaster = os.path.join(destinationpath, newFolderName)
				outputMaskedRaster = os.path.join(outputRaster, outputFileName)
				outNulled.save(outputMaskedRaster)

def step2():

	#Landsat5:
	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/LandsatScenes/Landsat5/ClippedScenes"
	destinationpath = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/NDMI_CloudMasked"
	curDir5 = arcpy.env.workspace
	arcpy.env.overwriteOutput = True

	cloudMaskingLandsatScenes(curDir5, destinationpath)
	print("cloud masking Landsat5 completed")

	#Landsat7:
	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/LandsatScenes/Landsat7/ClippedScenes"
	destinationpath = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/NDMI_CloudMasked"
	curDir7 = arcpy.env.workspace
	arcpy.env.overwriteOutput = True

	cloudMaskingLandsatScenes(curDir7, destinationpath)
	print("cloud masking Landsat7 completed")

	#Landsat8:
	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/LandsatScenes/Landsat8/ClippedScenes"
	destinationpath = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/NDMI_CloudMasked"
	curDir8 = arcpy.env.workspace
	arcpy.env.overwriteOutput = True

	cloudMaskingLandsatScenes(curDir8, destinationpath)
	print("cloud masking Landsat8 completed")


#___________________________________________________________________________________________________________________________________
# #STEP 3: MOSAICING LANDSAT SCENES

#Functions for Mosaicing Scenes:
def extractYear(filename):
	return filename[9:13]

def convertListToString(inputList):
	return ';'.join(inputList)

def extractJulianDate(filename):
	return filename[13:16]

def sortJulianDates(dates_input, targetDate):
	sorted_dates = dates_input
	distance_from_target = []
	for i in range(len(sorted_dates)):
		distance_from_target.append(abs(sorted_dates[i]-targetDate))
	zipped_stuff = zip(distance_from_target,sorted_dates)
	sorted_dates = [dates_input for distance_from_target, dates_input in sorted(zipped_stuff)]
	return sorted_dates

def listMatchingYears(curDir,target_year,target_julian_date):
	list_of_julian_dates = []
	for _,folders,_ in os.walk(curDir):
		for folder in folders:
			year = extractYear(folder)
			julian_date = extractJulianDate(folder)
			list_of_julian_dates.append(int(julian_date))
	sorted_julian_dates = sortJulianDates(list_of_julian_dates,target_julian_date)
	fileList = []
	for julian_date in sorted_julian_dates:
			for _,folders,_ in os.walk(curDir):
				for folder in folders:
					year = extractYear(folder)
					julian_date2 = extractJulianDate(folder)
					if int(year) == target_year and int(julian_date2) == julian_date:
							for file in os.listdir(folder):
								if file.endswith("ndmi_clipped_cloudMask.tif"):
									absolutePathCWD = os.path.abspath(folder) + '/' + file
									absolutePath = absolutePathCWD.replace('\\','/')
									fileList = fileList + [absolutePath]
	stringFromList = convertListToString(fileList)
	return stringFromList

def step3():
	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/NDMI_CloudMasked"
	destinationpath = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/NDMI_Mosaiced"
	arcpy.env.overwriteOuput = True
	curDir = os.getcwd() #or arcpy.env.workspace

	for year in range(2000, 2017):
		inputRasters = listMatchingYears(curDir, year, 202)
		print(inputRasters)
		outputFolder = destinationpath
		outputRaster = str(year) + "_ndmi_clipped_cloudMask_mosaiced.tif"
		if inputRasters !="":
			arcpy.MosaicToNewRaster_management(inputRasters, outputFolder, outputRaster, "#", "16_BIT_SIGNED", "30", "1", "FIRST", "#")
			source = os.listdir(curDir)
			for outputRaster in source:
				if outputRaster.endswith("ndmi_clipped_cloudMask_mosaiced.tif"):
					shutil.move(os.path.join(curDir,outputRaster), os.path.join(destinationpath,outputRaster))
	
	print("mosaicing Landsat scenes completed")


#___________________________________________________________________________________________________________________________________
# #STEP 4: CALCULATING INTERANNUAL CHANGES IN NDMI

#Functions For Obtaining dNDMI Rasters:
def extractMosaicedYear0(filename):
	return filename[0:4]

def extractMosaicedYear1(filename):
	return filename[0:4]

def chosenMosaicedYears(listoftwo):
	year0 = extractMosaicedYear0(listoftwo[0])
	year1 = extractMosaicedYear1(listoftwo[1])
	combineYears = year0 + year1
	print(combineYears)
	return combineYears

def step4():
	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/NDMI_Mosaiced"
	destinationpath = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI"
	arcpy.env.overwriteOuput = True

	yearlyMosaicedScenes = arcpy.ListRasters("*","TIF")
	print(yearlyMosaicedScenes)
	for x in range(1, len(yearlyMosaicedScenes)):
		dates = [yearlyMosaicedScenes[x-1], yearlyMosaicedScenes[x]]
		print(dates)
		followingYear = yearlyMosaicedScenes[x]
		previousYear = yearlyMosaicedScenes[x-1]
		print (followingYear)
		print (previousYear)
		dNDMI = Minus(previousYear, followingYear)
		outputName = chosenMosaicedYears(dates) + "_dndmi" + ".tif"
		print(outputName)
		chosenDirectory = os.path.join(destinationpath, outputName)
		fixedChosenDirectory = chosenDirectory.replace('\\','/')
		print(fixedChosenDirectory)
		dNDMI.save(fixedChosenDirectory)

	print("obtaining dNDMI rasters completed")


#___________________________________________________________________________________________________________________________________
# #STEP 5: SUBSETTING ADS POLYGONS TO BARK BEETLE AND TPA ATTRIBUTES

def step5(percentPath, percentile_subset='top15percTPA', selectionwherelist=[3,4,5]):
	#change workspace
	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/ADS_Polygons/RawADSPolygons"
	arcpy.env.overwriteOuput = True

	ADSshapes = arcpy.ListFeatureClasses(feature_type='polygon')
	yearcounter = 2000
	#change this
	field = "DCA1"
	#change this
	identifier = "barkbeetle"


	def buildWhereClauseFromList(table, field, valueList):
	    """Takes a list of values and constructs a SQL WHERE
	    clause to select those values within a given field and table."""

	    # Add DBMS-specific field delimiters
	    fieldDelimited = arcpy.AddFieldDelimiters(arcpy.Describe(table).path, field)

	    # Determine field type
	    fieldType = arcpy.ListFields(table, field)[0].type

	    # Add single-quotes for string field values
	    if str(fieldType) == 'String':
	        valueList = ["'%s'" % value for value in valueList]

	    # Format WHERE clause in the form of an IN statement
	    whereClause = "%s IN(%s)" % (fieldDelimited, ', '.join(map(str, valueList)))
	    return whereClause


	for i in range(0,len(ADSshapes)):
	    shape = ADSshapes[i]
	    arcpy.env.overwriteOuput = True
	    #change this, make new output folder before running script, name it something that makes sense based on your selection
	    outshape = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/ADS_Polygons/ADS_Subsets/BarkBeetle/" + field + identifier + str(yearcounter) + ".shp"
	    # change this to build a list of values in your desired field that you want to subset to
	    wherelist = [x for x in range(11000,11061)]+[11800,11900,11999]
	    where_clause = buildWhereClauseFromList(shape, field, wherelist)
	    arcpy.Select_analysis(shape, outshape, where_clause)
	    yearcounter += 1


	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/ADS_Polygons/ADS_Subsets/BarkBeetle"
	Shapes = arcpy.ListFeatureClasses()
	field = 'TPA1'

	#if  this is NOT done, run this, else, move on
	for shape in Shapes:
	  arcpy.AddField_management(shape, "PerRank", "Long", 3, field_is_nullable="NULLABLE")

	for shape in Shapes:
	  arr = arcpy.da.FeatureClassToNumPyArray(shape, (field))
	  arrstr = arr.astype(str)
	  recast = arrstr.astype(float)
	  
	  #to create 3 rank for example
	  print(shape)
	  p1 = np.percentile(recast, 75)
	  print p1
	  p2 = np.percentile(recast, 80)
	  print p2
	  p3 = np.percentile(recast, 85)
	  print(p3)
	  p4 = np.percentile(recast, 90)
	  print(p4)
	  p5 = np.percentile(recast, 95)
	  print(p5)
	  
	  
	  #use cursor to update the new rank field
	  with arcpy.da.UpdateCursor(shape , [field,'PerRank']) as cursor:
	    for row in cursor:
	      if row[0] < p1:
	        row[1] = 0  #rank 0
	      elif p1 <= row[0] and row[0] < p2:
	        row[1] = 1
	      elif p2 <= row[0] and row[0] < p3:
	        row[1] = 2
	      elif p3 <= row[0] and row[0] < p4:
	        row[1] = 3
	      elif p4 <= row[0] and row[0] < p5:
	        row[1] = 4  
	      else:
	        row[1] = 5

	      cursor.updateRow(row)

	yearcounter2 = 2000
	#change this
	field = "PerRank"
	#change this

	for shape in Shapes:
		arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/ADS_Polygons/ADS_Subsets/BarkBeetle"
		arcpy.env.overwriteOuput = True
		#change this, make new output folder before running script, name it something that makes sense based on your selection
		outshape = percentPath + field + percentile_subset + str(yearcounter2) + ".shp"
		# change this to build a list of values in your desired field that you want to subset to
		where_clause = buildWhereClauseFromList(shape, field, selectionwherelist)
		arcpy.Select_analysis(shape, outshape, where_clause)
		yearcounter2 += 1

	print("subsetting ADS polygons to Bark Beetle DTPA completed")

#___________________________________________________________________________________________________________________________________
#STEP 6: SUBSETTING INTERANNUAL CHANGE IN NDMI TO POLYGON TYPES (BARK BEETLE, HEALTHY FOREST, AND FIRE)

def step6():

	#Subsetting to Bark Beetle Polygons:
	def subsetToBarkBeetle(BB_DTPA_workspace, dNDMI_workspace, shapepath, destinationpath):
		arcpy.env.overwriteOuput = True
		arcpy.env.workspace = BB_DTPA_Polygons 
		#lists bark beetle shapefiles, excludes first shapefile (e.g: shapefiles = 2000-2016, would exclude 2000) Matches ADS shapefiles to second raster year in interannual period
		shapefiles = arcpy.ListFeatureClasses("*")

		arcpy.env.overwriteOuput = True
		#sets workspace to rasters folder
		arcpy.env.workspace = dndmiRasters 
		curDir = arcpy.env.workspace
		#Lists rasters in folder
		rasters = arcpy.ListRasters("*", "tif")
		for i in range(0, len(rasters)):
			out_raster =  rasters[i].split(".")[0] + "_subset_BB_DTPA" + ".tif"
			print(out_raster)
			targetr = rasters[i]
			print(targetr)
			targets = shapepath + shapefiles[i]
			print(targets)
			clippingNDMI_BB = arcpy.Clip_management(targetr, "#", out_raster, targets, "#", "ClippingGeometry","NO_MAINTAIN_EXTENT")
			source = os.listdir(curDir)
			for clippingNDMI_BB in source:
				if clippingNDMI_BB.endswith("BB_DTPA.tif"):
					shutil.move(os.path.join(curDir,clippingNDMI_BB), os.path.join(destinationpath,clippingNDMI_BB))

	BB_DTPA_Polygons = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/ADS_Polygons/ADS_Subsets/BB_DTPA/DTPA_Top15prc" #Change before running, Z:/Glacier/ADS_Polygons/ADS_Subsets/BB_DTPA/DTPA_SubsetToPercent_Top10prc
	dndmiRasters = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI" #Change before running, Z:/Glacier/NDMI/dNDMI
	shapepath_BB = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/ADS_Polygons/ADS_Subsets/BB_DTPA/DTPA_Top15prc/" #Change before running, Z:/Glacier/ADS_Polygons/ADS_Subsets/BB_DTPA/DTPA_SubsetToPercent_Top10prc/
	destinationpath_BB = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI_Subsets/dNDMI_BB/" #Change before running, Z:/Glacier/NDMI/dNDMI_Subsets/dNDMI_BB
	
	subsetToBarkBeetle(BB_DTPA_Polygons, dndmiRasters, shapepath_BB, destinationpath_BB)
	print("subsetting dNDMI to Bark Beetle Polygons completed")

	
	#Subsetting to Healthy Forest Polygons:
	def subsetToHealthyForest(HF_workspace, dNDMI_workspace, shapepath, destinationpath):
		arcpy.env.overwriteOuput = True
		arcpy.env.workspace = HF_Polygons
		#lists Healthy Forest shapefiles
		shapefiles = arcpy.ListFeatureClasses("*")

		arcpy.env.overwriteOuput = True
		#sets workspace to rasters folder
		arcpy.env.workspace = dndmiRasters
		curDir = arcpy.env.workspace
		#Lists rasters in folder
		rasters = arcpy.ListRasters("*", "tif")
		for i in range(0, len(rasters)):
			out_raster = rasters[i].split(".")[0] + "_subset_HF" + ".tif" 
			targetr = rasters[i]
			targets = shapepath + shapefiles[i]
			clippingNDMI_HF = arcpy.Clip_management(targetr, "#", out_raster, targets, "#", "ClippingGeometry","NO_MAINTAIN_EXTENT")
			source = os.listdir(curDir)
			for clippingNDMI_HF in source:
				if clippingNDMI_HF.endswith("subset_HF.tif"):
					shutil.move(os.path.join(curDir,clippingNDMI_HF), os.path.join(destinationpath,clippingNDMI_HF))

	HF_Polygons = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/HealthyForest_Polygons"
	dndmiRasters = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI"
	shapepath_HF = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/HealthyForest_Polygons/" #Change before running
	destinationpath_HF = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI_Subsets/dNDMI_HF" #Change before running

	subsetToHealthyForest(HF_Polygons, dndmiRasters, shapepath_HF, destinationpath_HF)
	print("subsetting dNDMI to Healthy Forest Polygons completed")
	

	#Subsetting to Fire Polygons:
	def subsetToFire(Fire_workspace, dNDMI_workspace, shapepath, destinationpath):
		arcpy.env.overwriteOuput = True
		arcpy.env.workspace = Fire_Polygons #Change before running
		#lists Fire shapefiles
		shapefiles = arcpy.ListFeatureClasses("*")

		arcpy.env.overwriteOuput = True
		#sets workspace to rasters folder
		arcpy.env.workspace = dndmiRasters
		curDir = arcpy.env.workspace
		#Lists rasters in folder
		rasters = arcpy.ListRasters("*", "tif")
		for i in range(0, len(rasters)):
			out_raster = rasters[0].split(".")[0] + "_subset_fire" + ".tif"
			targetr = rasters[i]
			targets = shapepath + shapefiles[i]
			clippingNDMI_Fire = arcpy.Clip_management(targetr, "#", out_raster, targets, "#", "ClippingGeometry","NO_MAINTAIN_EXTENT")
			source = os.listdir(curDir)
			for clippingNDMI_Fire in source:
				if clippingNDMI_Fire.endswith("_fire.tif"):
					shutil.move(os.path.join(curDir,clippingNDMI_Fire), os.path.join(destinationpath,clippingNDMI_Fire))
	
	Fire_Polygons = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/Fire_Polygons"
	dndmiRasters = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI"
	shapepath_Fire = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/Fire_Polygons/" #Change before running
	destinationpath_Fire = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI_Subsets/dNDMI_Fire" #Change before running

	subsetToFire(Fire_Polygons, dndmiRasters, shapepath_Fire, destinationpath_Fire)
	print("subsetting dNDMI to Fire Polygons completed")


#___________________________________________________________________________________________________________________________________
# #STEP 7: THRESHOLD RECLASSIFICATION (CREATING HISTOGRAMS)


#___________________________________________________________________________________________________________________________________
# #STEP 8: CREATING CLASSIFICATION MAPS

def step8():
	#Sets destination path and workspace 
	destinationpath = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI_ReClassified/ReClassified_UnMasked" #Change before running, Z:/Glacier/NDMI/ReClassified_dNDMI/ReClassified_UnMasked
	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI" #Change before running
	#turns overwrite on
	arcpy.env.overwriteOuput = True
	#lists rasters
	rasters = arcpy.ListRasters("*", "tif")
	print rasters
	for i in range(0, len(rasters)):
		in_raster = rasters[i]
		reclass_field = "VALUE"

		#Sets remap ranges
		remap = RemapRange([[-30000,-4000,1],[-4000,-1500,2],[-1500,0,3],[0,500,4],[500,30000,5]]) #change values of thresholds before running
		#Runs Reclassify 
		OutReclass = arcpy.sa.Reclassify(in_raster, reclass_field, remap, "DATA")
		#Saves output rasters to destination path
		OutReclass.save(os.path.join(destinationpath, "reclass_unmasked_" + rasters[i].split(".")[0] + ".tif")) #change if you want different file name

	
	#Masking Out Neighboring Towns not within Study Area:
	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/StudyArea_ShapeFiles/Mask_Elevation_Towns/Mask" #Change before running, 
	mask_path = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/StudyArea_ShapeFiles/Mask_Elevation_Towns/Mask/" #Change before running, 
	destination_path = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI_ReClassified/ReClassified_Masked" #Change before running, 
	arcpy.env.overwriteOuput = True

	#lists mask file
	shapes = arcpy.ListFeatureClasses("*")
	mask = shapes[0]
	print mask

	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI_ReClassified/ReClassified_UnMasked" #Change before running, 
	ReclassRasters = arcpy.ListRasters("*")
	print (ReclassRasters)
	for i in range(0, len(ReclassRasters)):
		in_raster = ReclassRasters[i]
		#print (in_raster)
		in_mask_data = mask_path + mask
		#print in_mask_data
		OutExtract = arcpy.sa.ExtractByMask(in_raster, in_mask_data)

		OutExtract.save(os.path.join(destination_path, "AllMask_" + in_raster.split(".")[0] + ".tif"))

	print("Classification Maps Completed")

#___________________________________________________________________________________________________________________________________
# #STEP 9: CREATING FREQUENCY MAPS

def step9():

	arcpy.env.overwriteOuput = True
	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI_ReClassified/ReClassified_Masked"

	rasters = arcpy.ListRasters("*")

	# uncomment to remap values
	for raster in rasters:
		reclassField = "Value"
		remap = RemapValue([[1, 0], [2, 0],[3, 1],[4, 0],[5, 0]])

		# Check out the ArcGIS Spatial Analyst extension license
		arcpy.CheckOutExtension("Spatial")

		#Run this if the frequency rasters arent made yet, if not, bypass this (OR FIND A WAY TO OVERWRITE PREVIOUS FILES)
		# Execute Reclassify
		outReclassify = Reclassify(raster, reclassField, remap, "NODATA")

		outfile = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI_Persistence/BinaryClass_ModerateDisturbance/" + raster.split(".")[0] + ".tif"

		# Save the output 
		outReclassify.save(outfile)

	#change list slice
	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI_Persistence/BinaryClass_ModerateDisturbance"
	brasters = arcpy.ListRasters("*")
	addable = brasters
	counter= 0
	while counter < 10:
		sum = CellStatistics([addable[0],addable[1],addable[2],addable[3],addable[4]], "SUM", "NODATA")

		#change name
		rastername = addable[0].split(".")[0]+"_"+addable[4]
		print rastername
		sum.save(os.path.join("Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI_Persistence/PersistenceMaps/UnMasked/", rastername))
		addable = addable[1:]
		#print(addable)
		counter += 1
		#the binary files are named such that the first year number in the file name refers to the second year of the interannual period. 
		#to make the output maps make intuitive sense to the viewer, change the lower bound for the frequency map in all naming conventions
		#to be the first year of the first interannual period.
	arcpy.env.workspace = "Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI_Persistence/PersistenceMaps/UnMasked"
	frasters = arcpy.ListRasters("*")
	for raster in frasters:
		outSetNull = SetNull(raster, raster, "VALUE < 1")
		outSetNull.save("Z:/Fall2016_GlacierNationalParkClimate/GlacierAutomation/NDMI/dNDMI_Persistence/PersistenceMaps/Masked"+raster)

	print("Frequency Maps Completed")

if __name__ == '__main__':
	main()
