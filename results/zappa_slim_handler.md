
# Zappa slim_handler Performance Results

## Introduction

Comparison of 2 similar functions. Both function are developed using Zappa and Flask, and include an extra binary file of 46.1mb making the resulting Lambda package of 49.6mb, which is within the 50mb limit.  One Lambda is deployed with `slim_handler=True` and the other one with `slim_handler=False`.

## Packages Sizes

`slim_handler=True`:

1) Lambda function size: 10.64mb
2) Package size: 53.86mb

`slim_handler=False`:

1) Package size: 49.6mb

## Execution Times and Memory Usage

##### FRAMEWORK BOOTSTRAP RESULTS
-----------------
| Function         |   Size(MB) | VPC   |   D.Mean |      Var |   Billed Mean |      Var |   Mem Mean |      Var |   Samples |
|:-----------------|-----------:|:------|---------:|---------:|--------------:|---------:|-----------:|---------:|----------:|
| zappa-slim   |      10.64 | No    | 5882.98  | 322278   |       5936.73 | 321122   |    166.857 | 14.2083  |        49 |
| zappa-noslim |      49.59 | No    |  835.252 |  18637.4 |        884    |  18922.4 |     46.98  |  9.85673 |        50 |


##### WARM START RESULTS

-----------------
| Function         |   Size(MB) | VPC   |   D.Mean |     Var |   Billed Mean |   Var |   Mem Mean |      Var |   Samples |
|:-----------------|-----------:|:------|---------:|--------:|--------------:|------:|-----------:|---------:|----------:|
| zappa-slim   |      10.64 | No    |  3.85507 | 26.362  |           100 |     0 |   167.736  | 15.1235  |      4918 |
| zappa-noslim |      49.59 | No    |  4.1465  | 28.8056 |           100 |     0 |    49.4513 |  9.52658 |      5010 |

## Conclusions

1) Looking at both packages, the one with the slim_handler, includes `botocore`, making the packages bigger.
2) Using slim_handler increases the memory usage significantly (+118mb). Based on AWS information, the usage of additional memory leads to the Lambda functions to be recycled more often.
3) When using slim_handler, the cold starts (without including the function execution time) will be up to 660ms faster as the package is smaller. (see [Results BY FUNCTION SIZE](results/by-size.md))
4) There's no difference in time execution for warm lambdas (even though the extra memory usage could make things slower if scarce).
5) For cold-starts, the slim_start adds an extra of at least 5 seconds in execution time. If the associated package is larger than 50mb, the extra time could be even larger.
