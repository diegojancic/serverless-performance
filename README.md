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


# Results

NOTE: Results are not yet statistically accurate. Not enough samples taken (check back in a few weeks).

### Cold-start statistics


| Function         |   Size(MB) | VPC   |   D.Mean |     Var |   Billed Mean |     Var |   Mem Mean |   Var |
|:-----------------|-----------:|:------|---------:|--------:|--------------:|--------:|-----------:|------:|
| zappa-django |      14.11 | No    |  2605.81 | 12123.7 |       2666.67 | 13333.3 |         61 |     0 |
| zappa-flask |       5.59 | No    |    711.7 |   nan |           800 |   nan |         48 |   nan |



### Warm-start statistics

| Function         |   Size(MB) | VPC   |   D.Mean |     Var |   Billed Mean |   Var |   Mem Mean |     Var |
|:-----------------|-----------:|:------|---------:|--------:|--------------:|------:|-----------:|--------:|
| zappa-django |      14.11 | No    |  1.76097 | 2.65008 |           100 |     0 |    58.4839 | 9.05806 |
| zappa-flask |       5.59 | No    |     2.22 | 7.55382 |           100 |     0 |         48 |     0 |


# License

Initially created by Diego Jancic. MIT License.
