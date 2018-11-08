# Serverless Performance Tests - Results BY FUNCTION SIZE

# References

__Functions:__

All functions are created using Chalice. Besides the default minimal package and extra file of 1MB, 2MB, ..., 49MB was added. This extra file does/should not change the memory usage or compile time of the function. It could affect how often the function gets recycled and the cold start time.

# Results

## Graphs

![Function time cold start](by-size-cold.png)

![Function time warm start](by-size-warm.png)
