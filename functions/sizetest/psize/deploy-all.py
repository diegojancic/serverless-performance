import os
import time

fileNames = ["app.py", ".chalice/config.json", "create-file.sh"]

for sizeMb in range(0, 50):

    print(f"PUBLISHING APP FOR SIZE {sizeMb}MB")
    print("----------------------------------")
    for fileName in fileNames:

        # Read in the file
        with open(fileName + '.template', 'r') as file:
          filedata = file.read()

        # Replace all the variables
        sizeBytes = sizeMb * 1048576
        filedata = filedata.replace('<<APP_NAME>>', f'psize-{sizeMb}')
        filedata = filedata.replace('<<SIZE_BYTES>>', f'{sizeBytes}')

        # Write the file out again
        with open(fileName, 'w') as file:
          file.write(filedata)

    # Create random file and publish
    os.system("rm -rdf ./.chalice/deployments ./.chalice/deployed")
    os.system("sh create-file.sh")
    os.system("chalice deploy --connection-timeout 100000")

    #print("delaying 200 seconds")
    #time.sleep(200)
