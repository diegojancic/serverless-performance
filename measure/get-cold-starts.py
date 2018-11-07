import boto3
import json
from datetime import datetime
from datetime import timedelta
from tabulate import tabulate

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
    lambdaSegment = None
    for seg in segments:
        sd = json.loads(seg["Document"])
        if sd["origin"] == "AWS::Lambda::Function":
            functionSegment = sd
        elif sd["origin"] == "AWS::Lambda":
            lambdaSegment = sd

    functionName = ""
    functionTime = ""
    coldStartTime = ""

    if functionSegment:
        functionName = functionSegment["name"]
        functionTime = functionSegment["end_time"] - functionSegment["start_time"]
        coldStartTime = functionSegment["start_time"] - lambdaSegment["start_time"]

        functionTime = round(functionTime*1000)
        coldStartTime = round(coldStartTime*1000)
    else:
        functionName = lambdaSegment["name"]
    results.append([functionName, duration*1000, functionTime, coldStartTime])


headers = ["Function", "TotalTime (ms)", "FuncTime (ms)", "ColdStart (ms)"]

print("RESULS")
print("-----------------")
print(tabulate(results, tablefmt="pipe", headers=headers))
