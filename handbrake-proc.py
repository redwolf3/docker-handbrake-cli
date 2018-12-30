import os
import subprocess
import sys
import time

# Program Information
print("----------------------------------------------------------------")
print("-- Handbrake Processing Tool                                  --")
print("----------------------------------------------------------------")
print("-- Version: 0.0.1                                             --")
print("-- Author: Steven West <steve@steven-west.com>                --")
print("-- Github: https://github.com/redwolf3/docker-handbrake-cli   --")
print("----------------------------------------------------------------")
print("")

# Base Parameters
inputPathRoot = "/input"
outputPathRoot = "/output"
presetsPathRoot = "/presets"

# Override Base Parameters (for testing / debugging)
if (len(sys.argv) > 1) and (sys.argv[1] == "DEBUG"):
	inputPathRoot = "/Volumes/Videos/MKV_Ripping"
	outputPathRoot = "/Volumes/Videos/HandrakeTest"
	presetsPathRoot = "/Users/swest/Projects/docker-handbrake-cli/presets"

# Output Base Parameters
print("Input Root: " + inputPathRoot)
print("Output Root: " + outputPathRoot)
print("Presets Path Root: " + presetsPathRoot)
print("")

# Search for input files
print("Searching for input files to process...")
inputFiles = []
print("   Searching for input files under: " + inputPathRoot)
for path, subdirs, files in os.walk(inputPathRoot):
	for filename in files:
		#print("Checking for files under " + path + "...")
		if filename.lower().endswith(".mkv"):
			inputFilePath = os.path.join(path,filename)
			print("   Found: " + inputFilePath)
			# TODO: Add a check to see if the file is in use
			# TODO: One solution is to scan the files 'X' times with a delay and see if the size, last modified date, or hash has changed
			# TODO: Alternatively, see if there is an easy way to check if the MKV file is "complete"
			inputFiles.append(inputFilePath)
print("Found " + str(len(inputFiles)) + " input file(s) to process.")
print("Searching for input files to process...Done!")
print("")

# Execute Handbrake Against Each File
for inputFile in inputFiles:
	print("Processing: " + os.path.basename(inputFile) + "...")

	currMedium = os.path.basename(os.path.dirname(os.path.dirname(inputFile)))
	# print("   Medium: " + currMedium)

	currFormat = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(inputFile))))
	# print("   Format: " + currFormat)

	currVideoType = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(inputFile)))))
	# print("   Type: " + currVideoType)

	presetFile = currFormat + "-" + currMedium + ".json"
	presetFilePath = os.path.join(presetsPathRoot, presetFile)
	presetFileExists = os.path.exists(presetFilePath)
	print("   Preset file: " + presetFile + " (Exists: " + str(presetFileExists) + ")")
	if not presetFileExists:
		print("   Preset file doesn't exist, skipping file...")
		continue

	currOutputFilename = os.path.basename(os.path.dirname(inputFile))
	currOutputFilename = currOutputFilename + ".mkv"
	print("   Output filename: " + currOutputFilename)

	currOutputFolder = os.path.basename(os.path.dirname(inputFile))
	if currOutputFolder.endswith(" - 3D"):
		currOutputFolder = currOutputFolder[0:currOutputFolder.find(" - 3D")]
	if currOutputFolder.endswith(" - 2D"):
		currOutputFolder = currOutputFolder[0:currOutputFolder.find(" - 2D")]
	currOutputFolderPath = os.path.join(outputPathRoot, currVideoType, currFormat, currOutputFolder)
	currOutputFolderExists = os.path.exists(currOutputFolderPath)
	print("   Output Folder: " + currOutputFolder + " (Exists: " + str(currOutputFolderExists) + ")")
	print("   Output folder path: " + currOutputFolderPath + " (Exists: " + str(currOutputFolderExists) + ")")

	currOutputFilePath = os.path.join(currOutputFolderPath, currOutputFilename)
	currOutputFileExists = os.path.exists(currOutputFilePath)
	print("   Output file path: " + currOutputFilePath + " (Exists: " + str(currOutputFileExists) + ")")

	if not os.path.exists(currOutputFolderPath):
		print("   Creating output folder '" + currOutputFolderPath + "'...")
		os.makedirs(currOutputFolderPath)
		print("   Creating output folder '" + currOutputFolderPath + "'...Done!")
	else:
		print("   Output folder '" + currOutputFolderPath + "' already exists!")

	if os.path.exists(currOutputFilePath):
		print("   Output file '" + currOutputFilePath + "' already exists!")
		print("   Skipping file...")
		continue

	hbCommand = "HandBrakeCLI --preset-import-file " + presetFilePath + " -i " + inputFile + " -o " + currOutputFilePath
	#print("   Handbrake Command: " + hbCommand)
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
