import boto3
import time


enable = True

tracingConfig = 'Active' if enable else 'PassThrough'

print ('Loading Lambda functions...')

# Read all functions
lda = boto3.client('lambda')
iam = boto3.client('iam')
paginator = lda.get_paginator('list_functions')

funcs = [fn for page in paginator.paginate() for fn in page['Functions']]
print (f'{len(funcs)} functions found. Updating tracing...')

policyArn = 'arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess'

# UPDATE ALL FUNCTIONS
for fn in funcs:
    # Do nothing if in same mode as requested
    if fn["TracingConfig"]["Mode"] == tracingConfig: continue;

    print (f'Updating function {fn["FunctionName"]}.', end="", flush=True)

    roleArn = fn['Role']
    roleName = roleArn[roleArn.find('/')+1:]

    # Update the role to allow XRay access if needed
    if enable:
        response = iam.attach_role_policy(
            PolicyArn=policyArn,
            RoleName=roleName
        )
        # Permissions usually take a little bit to take effect
        time.sleep(1)
    else:
        response = iam.detach_role_policy(
            PolicyArn=policyArn,
            RoleName=roleName
        )

    retry = True
    while retry:
        retry = False
        try:
            lda.update_function_configuration(
                FunctionName=fn['FunctionArn'],
                Timeout=30,
                MemorySize=512,
                TracingConfig={'Mode': tracingConfig}
            )
            print("")   # add new line
        except Exception as ex:
            if 'permissions to call PutTraceSegments on XRAY' in str(ex):
                print(".", end="", flush=True)
                retry = True
                time.sleep(1)
                continue
            raise ex


print(f'All functions updated!')
