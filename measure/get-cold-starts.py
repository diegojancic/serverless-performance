import boto3
import argparse
import json
from datetime import datetime
from datetime import timedelta
from tabulate import tabulate

# Read args
parser = argparse.ArgumentParser(description='Reads CloudWatch Logs and parses execution durations and more.')
parser.add_argument('functions', nargs='+', help='Name of the functions to read the info.')

args = parser.parse_args()
functionNames = args.functions


# Load XRay traces
xray = boto3.client("xray")
summariespg = xray.get_paginator("get_trace_summaries")

print ("Loading trace list...")
summaries = summariespg.paginate(StartTime=datetime.utcnow()-timedelta(days=1),
                                EndTime=datetime.utcnow(),
                                Sampling=False)

trace_ids = [trace["Id"] for s in summaries for trace in s["TraceSummaries"]]
print (f"{len(trace_ids)} traces found.")
print ("Loading traces details...")

# The batch_get_traces Paginator support up to 5 traces, so we need to iterate
tracepg = xray.get_paginator('batch_get_traces')
traces = []
for i in range(0, len(trace_ids), 5):
    trace_range = tracepg.paginate(TraceIds=trace_ids[i:i+5])
    traces.extend([trace for p in trace_range for trace in p["Traces"]])

print (f"{len(traces)} traces loaded.")

results = []
for trace in traces:
    duration = trace["Duration"]
    segments = trace["Segments"]

    # Find the segment in the trace that has the function
    # execution time
    functionSegment = None
    for seg in segments:
        functionSegment = json.loads(seg["Document"])
        if functionSegment["origin"] == "AWS::Lambda::Function":
            break

    function_name = functionSegment["name"]
    function_time = functionSegment["end_time"] - functionSegment["start_time"]
    results.append([function_name, duration*1000, round(function_time*1000)])


headers = ["Function", "TotalTime (ms)", "FuncTime (ms)"]

print("RESULS")
print("-----------------")
print(tabulate(results, tablefmt="pipe", headers=headers))
