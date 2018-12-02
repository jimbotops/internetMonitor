import re
import argparse

# Create a parser to read command line args
parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', help="input file with extension")
parser.add_argument('-o', '--output', help="output file, should be csv", default="result.csv")
args = parser.parse_args()

# Read the files in to be processed
rawFile = open(args.input, "r")
processedFile = open(args.output, "w")

# Split by Regex that matches this type of string - Mon 20 Aug 22:57:01 BST 2018
# Remove the first element as this is just empty
parsedArr = re.split('([A-z]{3} [0-9]{2} [A-z]{3} [0-9]{2}:[0-9]{2}:[0-9]{2} BST [0-9]{4})', rawFile.read())[1:]

i=0
while i < len(parsedArr)-1:
    # Check for failures to connect at all
    if "Failed" not in parsedArr[i+1] and "Cannot" not in parsedArr[i+1]:
        # Extract just the download speed value
        downloadStartLocation = parsedArr[i+1].find('Download: ')
        downloadEndLocation = parsedArr[i+1].find('Mbits/s', downloadStartLocation)
        if (downloadStartLocation == -1) or (downloadEndLocation == -1):
            downloadValue =  "0"
        else:
            downloadValue = ((parsedArr[i+1])[downloadStartLocation+10:downloadEndLocation])

        # Extract just the upload speed value
        uploadStartLocation = parsedArr[i+1].find('Upload: ')
        uploadEndLocation = parsedArr[i+1].find('Mbits/s', uploadStartLocation)
        if (uploadStartLocation == -1) or (uploadEndLocation == -1):
            uploadValue =  "0"
        else:
            uploadValue = ((parsedArr[i+1])[uploadStartLocation+8:uploadEndLocation])
    # If it failed, set both values to 0
    else:
        downloadValue = "0"
        uploadValue = "0"
    print("Date:"+parsedArr[i]+"Download:" +downloadValue+"Upload:"+uploadValue)

    # Write the data into the file in the format: dateTime, download, upload
    # This makes it really easy for parsing as it's in csv
    processedFile.write(parsedArr[i]+","+downloadValue+","+uploadValue+"\n")
    i += 2

