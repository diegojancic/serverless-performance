import boto3
import re
import argparse


# Read args
parser = argparse.ArgumentParser(description='Reads CloudWatch Logs and parses execution durations and more.')
parser.add_argument('function', help='Name of the function to read the info.')

args = parser.parse_args()

functionName = args.function

print (f"LOADING INFO FOR FUNCTION '{functionName}'")
print ("-------------------------")

cwl = boto3.client('logs')

# Load groups
print ("Loading log groups...")
groups = cwl.describe_log_groups()

logGroupName = "/aws/lambda/" + functionName
logGroups = [g for g in groups["logGroups"] if g["logGroupName"] == logGroupName]
if len(logGroups) == 0:
	raise Exception(f"Log group for function '{functionName}' not found.")

logGroup = logGroups[0]


# Read the logs
print ("Loading events...")
logs = cwl.filter_log_events(logGroupName = '/aws/lambda/zappa-django-dev', 
	filterPattern='"Duration: "', 
	interleaved=True)

events = logs["events"]
print (f"{len(events)} invocations found...")

# Parse logs
pattern = re.compile(r"Duration: (?P<duration>\d+(\.\d+)?) ms.+Billed Duration: (?P<billed>\d+(\.\d+)?) ms.+Memory Size: (?P<memsize>\d+).+Max Memory Used: (?P<memused>\d+)", 
			re.IGNORECASE | re.MULTILINE | re.DOTALL)

functionInfo = {
	"name": functionName,
	"memorySize": 0
}
data_collected_headers = ["duration", "billed", "memused"]
data_collected = []

first_event = True
for evnt in events:
	message = evnt["message"]

	results = pattern.search(message)
	if not results:
		print ("Warn: the following message didn't match the pattern: " + message)
		continue;
	results.group("duration")

	if first_event:
		first_event = False
		functionInfo["memorySize"] = int(results.group("memsize"))

	data_collected.append([
			float(results.group("duration")),
			int(results.group("billed")),
			int(results.group("memused")),
		])


print ("All Done")
print (functionInfo)
print (data_collected_headers)
print (data_collected)
