import os
import subprocess
import sys
import time

# Program Information
print("----------------------------------------------------------------")
print("-- Handbrake Processing Tool                                  --")
print("----------------------------------------------------------------")
print("-- Version: 1.0                                               --")
print("-- Author: Steven West <steve@steven-west.com>                --")
print("-- Github: https://github.com/redwolf3/docker-handbrake-cli   --")
print("----------------------------------------------------------------")
print("")

# Base Parameters
inputPathRoot = "/input"
outputPathRoot = "/output"
presetsPathRoot = "/presets"

# Override Base Parameters (for testing)
if (len(sys.argv) > 1) and (sys.argv[1] == "DEBUG"):
	inputPathRoot = "/Volumes/Videos/MKV_Ripping"
	outputPathRoot = "/Volumes/Videos"
	presetsPathRoot = "/Users/swest/Projects/docker-handbrake-cli/presets"

# Output Base Parameters
print("Input Root: " + inputPathRoot)
print("Output Root: " + outputPathRoot)
print("Presets Path Root: " + presetsPathRoot)
print("")

# Search for input files
print("Searching for input files under " + inputPathRoot + "...")
inputFiles = []
for path, subdirs, files in os.walk(inputPathRoot):
	for filename in files:
		if filename.lower().endswith(".mkv"):
			inputFilePath = os.path.join(path,filename)
			print("   Found: " + inputFilePath)
			inputFiles.append(inputFilePath)
print("Finished searching for input files!")
print("")

# Execute Handbrake Against Each File
for inputFile in inputFiles:
	print("Processing: " + os.path.basename(inputFile) + "...")
	currOutputFilename = os.path.basename(os.path.dirname(inputFile))
	currOutputFolder = currOutputFilename
	currOutputFilename = currOutputFilename + ".mkv"
	if currOutputFolder.endswith(" - 3D"):
		currOutputFolder = currOutputFolder[0:currOutputFolder.find(" - 3D")]
	if currOutputFolder.endswith(" - 2D"):
		currOutputFolder = currOutputFolder[0:currOutputFolder.find(" - 2D")]
	currMedium = os.path.basename(os.path.dirname(os.path.dirname(inputFile)))
	currFormat = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(inputFile))))
	currVideoType = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(inputFile)))))
	currOutputFolderPath = os.path.join(outputPathRoot, currVideoType, currFormat, currOutputFolder)
	currOutputFilePath = os.path.join(currOutputFolderPath, currOutputFilename)
	presetFile = currFormat + "-" + currMedium + ".json"
	presetFilePath = os.path.join(presetsPathRoot, presetFile)
	print("   Input File Path: " + inputFile)
	print("   Output File Path: " + currOutputFilePath)
#	print("   Output Filename: " + currOutputFilename)
#	print("   Output Folder: " + currOutputFolder)
#	print("   Medium: " + currMedium)
#	print("   Format: " + currFormat)
#	print("   Type: " + currVideoType)
	print("   Preset File: " + presetFile + " (Exists: " + str(os.path.exists(presetFilePath)) + ")")

	if not os.path.exists(currOutputFolderPath):
		os.makedirs(currOutputFolderPath)
		print("   Created Output Folder: " + currOutputFolderPath)

	hbCommand = "HandBrakeCLI --preset-import-file " + presetFilePath + " -i " + inputFile + " -o " + currOutputFilePath
	print("   Handbrake Command: " + hbCommand)
	print("   Executing HandBrake...")
	try:
		retCode = subprocess.call(args=["HandBrakeCLI", "--preset-import-file", presetFilePath, "-i", inputFile, "-o", currOutputFilePath], stdout=sys.stdout, stderr=sys.stderr)
		if retCode < 0:
			print("HandBrakeCLI was terminated by signal.", -retcode, file=sys.stderr)
		elif retCode == 0:
			print("HandBrakeCLI completed successfully!")
		else:
			print("HandBrakeCLI encountered an error.", retcode, file=sys.stderr)
	except OSError as e:
		print("Execution failed: ", e, file=sys.stderr)

	print("")


print("")
print("Goodbye!")
