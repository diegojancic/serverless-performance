from urllib.request import urlopen
import argparse
import time
import boto3


ping_count = 400
ping_delay_mins = 5

# Read args
parser = argparse.ArgumentParser(description='Pings an URL during a few days to get information about it\'s execution times')
parser.add_argument('function', help='Name of the function to read the info.')

args = parser.parse_args()
functionName = args.function

print ("Loading API Gateway information...")

# Read API Gateway information
ag = boto3.client("apigateway")
functions = ag.get_rest_apis()
functionGateway = [x for x in functions["items"] if x["name"] == functionName]

if len(functionGateway) == 0:
	raise Exception("Function not found.")

api_id = functionGateway[0]["id"]
stages = ag.get_stages(restApiId=api_id)
stage_name = stages["item"][0]["stageName"]

#stage = ag.get_stage(restApiId=api_id, stageName=stage_name)
url = f"https://{api_id}.execute-api.us-east-1.amazonaws.com/{stage_name}"
print(f"Using URL: {url}")


for i in range(1, ping_count):
	print(time.strftime("%x %X") + f": Pinging {url}")
	resp = urlopen(url)
	resp.read()
	time.sleep(ping_delay_mins*60)

print(f"All done! {ping_count} pings done.")

