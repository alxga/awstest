import os
import subprocess

__author__ = "Alex Ganin"


pbDataDir = "/home/alxga/data/mbta-TripUpdates"
csvDataDir = "/home/alxga/data/csv-mbta-TripUpdates"
gtfsToCsv = "/home/alxga/src/gtfsToCsv/gtfsToCSV"
gtfsToCsvEnv = {"LD_LIBRARY_PATH": "/usr/local/lib"}

if not os.path.exists(csvDataDir):
  os.makedirs(csvDataDir)

for entry in os.listdir(pbDataDir):
  pbPath = os.path.join(pbDataDir, entry)
  if os.path.isfile(pbPath):
    csvName = os.path.splitext(os.path.basename(pbPath))[0] + ".csv"
    csvPath = os.path.join(csvDataDir, csvName)
    if os.path.exists(csvPath):
      continue
    myinput = open(pbPath, 'rb')
    myoutput = open(csvPath, 'wb')
    p = subprocess.Popen(gtfsToCsv, stdin=myinput, stdout=myoutput,
                         env=gtfsToCsvEnv)
    p.wait()
    myoutput.flush()
    print("%s" % csvName)
