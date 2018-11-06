import boto3
import re
import argparse

from tabulate import tabulate
from scipy import stats


# Read args
parser = argparse.ArgumentParser(description='Reads CloudWatch Logs and parses execution durations and more.')
parser.add_argument('functions', nargs='+', help='Name of the functions to read the info.')

args = parser.parse_args()
functionNames = args.functions

data_collected_headers = ["duration", "billed", "memused", "bootstrapRun"]

cwl = boto3.client('logs')

# Load groups
print ("Loading log groups...")
groups = cwl.describe_log_groups()
nextToken = groups["nextToken"] if 'nextToken' in groups else None
while nextToken:
	groupsBatch = cwl.describe_log_groups(nextToken=nextToken)
	nextToken = groupsBatch["nextToken"] if 'nextToken' in groupsBatch else None
	groups["logGroups"].extend(groupsBatch["logGroups"])


def load_function(functionName):
	functionInfo = {
		"name": functionName,
		"memorySize": 0
	}
	data_collected = []


	print (f"LOADING INFO FOR FUNCTION '{functionName}'")
	print ("--------------------------------------")

	# Load additional function information
	print("Loading function info...")
	lambda_client = boto3.client("lambda")
	finfo = lambda_client.get_function(FunctionName=functionName)
	functionInfo["codeSize"] = finfo["Configuration"]["CodeSize"]/1024/1024
	#functionInfo["codeSize"] = finfo["Configuration"]["MemorySize"]
	functionInfo["inVpc"] = (("VpcConfig" in finfo["Configuration"])
							and finfo["Configuration"]["VpcConfig"]["VpcId"])

	# Load logs

	logGroupName = "/aws/lambda/" + functionName
	logGroups = [g for g in groups["logGroups"] if g["logGroupName"] == logGroupName]
	if len(logGroups) == 0:
		raise Exception(f"Log group for function '{functionName}' not found.")

	logGroup = logGroups[0]


	# Read log streams
	logStreams = cwl.describe_log_streams(logGroupName=f'/aws/lambda/{functionName}')
	for logStream in logStreams["logStreams"]:

		logStreamName = logStream["logStreamName"]

		# Read the logs
		print ("Loading events...")
		logs = cwl.filter_log_events(logGroupName = f'/aws/lambda/{functionName}',
			filterPattern='"Duration: "',
			logStreamNames=[logStreamName])

		#import pdb;pdb.set_trace()

		events = logs["events"]
		print (f"{len(events)} invocations found...")

		# Parse logs
		pattern = re.compile(r"Duration: (?P<duration>\d+(\.\d+)?) ms.+Billed Duration: (?P<billed>\d+(\.\d+)?) ms.+Memory Size: (?P<memsize>\d+).+Max Memory Used: (?P<memused>\d+)",
					re.IGNORECASE | re.MULTILINE | re.DOTALL)


		first_event = True
		for evnt in events:
			message = evnt["message"]

			results = pattern.search(message)
			if not results:
				print ("Warn: the following message didn't match the pattern: " + message)
				continue;
			results.group("duration")

			bootstrapRun = False
			if first_event:
				first_event = False
				bootstrapRun = True
				functionInfo["memorySize"] = int(results.group("memsize"))

			data_collected.append([
					float(results.group("duration")),
					int(results.group("billed")),
					int(results.group("memused")),
					bootstrapRun
				])

	return (functionInfo, data_collected)


summary_headers = ["Function", "Size(MB)", "VPC", "D.Mean", "Var", "Billed Mean", "Var", "Mem Mean", "Var", "Samples"]

def get_stats(data):
	data_stats = stats.describe(data)
	data_row = [
				functionName,
				"%.02f" % functionInfo["codeSize"],
				"Yes" if functionInfo["inVpc"] else "No"
				]

	# duration mean and variance
	data_row.append(data_stats.mean[0])
	data_row.append(data_stats.variance[0])

	# billed duration mean and variance
	data_row.append(data_stats.mean[1])
	data_row.append(data_stats.variance[1])

	# mem used mean and variance
	data_row.append(data_stats.mean[2])
	data_row.append(data_stats.variance[2])

	# Samples
	data_row.append(data_stats.nobs)

	return data_row
	#print(tabulate([data_row], tablefmt="pipe", headers=summary_headers))


### LOAD ALL FUNCTIONS INFO ###

full_results_bootstrap = []
full_results_warm = []
for functionName in functionNames:
	(functionInfo, data_collected) = load_function(functionName)

	data_collected_warm = [x for x in data_collected if x[3] == False]
	data_collected_bootstrap = [x for x in data_collected if x[3] == True]

	full_results_bootstrap.append(get_stats(data_collected_bootstrap))
	full_results_warm.append(get_stats(data_collected_warm))


print ("All Done")

# RAW DATA:
print (functionInfo)
#print (data_collected_headers)
#print (data_collected)

# SUMMARY DATA:

print("FRAMEWORK BOOTSTRAP RESULS")
print("-----------------")
print(tabulate(full_results_bootstrap, tablefmt="pipe", headers=summary_headers))
#output_stats(data_collected_bootstrap)

print("WARM START RESULS")
print("-----------------")
print(tabulate(full_results_warm, tablefmt="pipe", headers=summary_headers))
#output_stats(data_collected_warm)



#https://pypi.org/project/tabulate/
#print(tabulate(df, tablefmt="markdown", headers="keys"))
#https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#tables
