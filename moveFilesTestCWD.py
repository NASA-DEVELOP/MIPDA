import os
import shutil

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

def functionThatActuallyMovesTheFiles(getcwd):
  currentFolder = os.getcwd()
  for f in os.listdir(currentFolder):
    if not f.endswith("tif"):
      continue
    newFolderName = createFolderFromFilename(currentFolder,f)
    satellite = extractSatelliteName(f)
    dateString = extractDate(f)
    matchingName = satellite + dateString
    for file in os.listdir(currentFolder):
      if not file.endswith("tif"):
        continue
      satellite2 = extractSatelliteName(file)
      dateString2 = extractDate(file)
      if satellite == satellite2 and dateString == dateString2:
        originalFile = os.path.join(currentFolder,file)
        newFile = os.path.join(newFolderName,file)
        shutil.move(originalFile,newFile)

functionThatActuallyMovesTheFiles(os.getcwd())