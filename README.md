# Serverless Performance Tests

Different tests to assess the performance of different serverless frameworks.

Initially it will include the most common Python frameworks, such as Zappa, Serverless Framework and AWS Chalice. Even if the purpose of each of those frameworks is different and their options are different too, this is only to add more information on Lambda cold and warm starts.

Feel free to add more tests in different languages or using other frameworks.


# References

__Columns:__

- Function: the name of the framework(s) used
- Size: the size of the code as reported by AWS Lambda
- VPC: Whether the Lambda function is inside a VPC
- D.Mean: Average (mean) duration of the invocations, as reported by Lambda in CloudWatch Logs.
- Billed Mean: Average (mean) duration of the billed duration. The billed duration is the duration rounded to the closest 100 milliseconds.
- Mem: The memory used as reported by Lambda.
- Var: Variance of the measures of the column on the left.

__Functions:__

- **zappa-django**: Django installation with all Zappa defaults. Set to Debug=False and 512mb Lambda function memory (Zappa's default).
- **zappa-flask**: Flask installation with all Zappa defaults. Using 512mb Lambda function memory (Zappa's default).
- **serverless-django**: Django installation using the Serverless framework. Set to Debug=False and 512mb Lambda function memory, with plugins serverless-wsgi and serverless-python-requirements.
- **serverless-flask**: Flask installation using the Serverless framework. Using 512mb Lambda function memory, with plugins serverless-wsgi and serverless-python-requirements.
- **chalice**: Basic Chalice example returning a basic HTML.
- **chalice-1.25mb**: Chalice package plus [5 common Python](functions/chalice-extras/website/requirements.txt) packages. Size 1.25MB.


# Results

NOTE: Results are not yet statistically accurate. Not enough samples taken (check back in a few weeks).

### Cold-start statistics


| Function         |   Size(MB) | VPC   |   D.Mean |         Var |   Billed Mean |    Var |   Mem Mean |     Var |   Samples |
|:-----------------|-----------:|:------|---------:|------------:|--------------:|-------:|-----------:|--------:|----------:|
| zappa-django |      14.11 | No    |  2271.87 | 1.00807e+06 |       2328.57 | 972381 |    59.4286 | 7.28571 |         7 |
| zappa-flask |       5.59 | No    |  753.144 | 2552.08 |           820 |  2000 |         47 |     5 |         5 |
| serverless-django |       9.88 | No    |    82.39 | 10.6617 |           100 |     0 |         49 |     3 |         3 |
| serverless-flask |       1.42 | No    |  33.9133 | 10.27 |           100 |     0 |         36 |     3 |         3 |
| chalice |       0.01 | No    |     0.62 | 0.0018 |           100 |     0 |         22 |     0 |         2 |
| chalice-1.25mb |       1.25 | No    |     0.71 |   nan |           100 |   nan |         22 |   nan |         1 |



### Warm-start statistics

| Function         |   Size(MB) | VPC   |   D.Mean |     Var |   Billed Mean |   Var |   Mem Mean |     Var |   Samples |
|:-----------------|-----------:|:------|---------:|--------:|--------------:|------:|-----------:|--------:|----------:|
| zappa-django |      14.11 | No    |  4.19663 | 21.9482 |           100 |     0 |    59.7238 | 6.76771 |       181 |
| zappa-flask |       5.59 | No    |  4.65865 | 26.103 |           100 |     0 |    47.6474 | 1.64909 |       156 |
| serverless-django |       9.88 | No    |  4.02335 | 21.8958 |           100 |     0 |     48.422 | 2.25696 |       173 |
| serverless-flask |       1.42 | No    |  3.02832 | 17.0831 |           100 |     0 |     35.422 | 2.25696 |       173 |
| chalice |       0.01 | No    |  3.01447 | 14.3451 |           100 |     0 |         22 |     0 |        47 |
| chalice-1.25mb |       1.25 | No    | 0.645882 | 0.329563 |           100 |     0 |         22 |     0 |        17 |

# License

Initially created by Diego Jancic. MIT License.
