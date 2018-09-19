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

- zappa-django: Django installation with all Zappa defaults. Set to Debug=False and 512mb Lambda function memory (Zappa's default).
- zappa-flask: Flask installation with all Zappa defaults. Using 512mb Lambda function memory (Zappa's default).
- chalice: Basic Chalice example returning a basic HTML.


# Results

NOTE: Results are not yet statistically accurate. Not enough samples taken (check back in a few weeks).

### Cold-start statistics


| Function         |   Size(MB) | VPC   |   D.Mean |         Var |   Billed Mean |    Var |   Mem Mean |     Var |   Samples |
|:-----------------|-----------:|:------|---------:|------------:|--------------:|-------:|-----------:|--------:|----------:|
| zappa-django |      14.11 | No    |  2271.87 | 1.00807e+06 |       2328.57 | 972381 |    59.4286 | 7.28571 |         7 |
| zappa-flask |       5.59 | No    |  753.144 | 2552.08 |           820 |  2000 |         47 |     5 |         5 |
| chalice |       0.01 | No   |     0.62 |   nan |           100 |   nan |         22 |   nan |         1 |




### Warm-start statistics

| Function         |   Size(MB) | VPC   |   D.Mean |     Var |   Billed Mean |   Var |   Mem Mean |     Var |   Samples |
|:-----------------|-----------:|:------|---------:|--------:|--------------:|------:|-----------:|--------:|----------:|
| zappa-django |      14.11 | No    |  4.19663 | 21.9482 |           100 |     0 |    59.7238 | 6.76771 |       181 |
| zappa-flask |       5.59 | No    |  4.65865 | 26.103 |           100 |     0 |    47.6474 | 1.64909 |       156 |
| chalice |       0.01 | No   |  2.21538 | 17.5225 |           100 |     0 |         22 |     0 |        13 |



# License

Initially created by Diego Jancic. MIT License.
