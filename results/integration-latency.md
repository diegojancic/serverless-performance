# Serverless Performance Tests - INTEGRATION LATENCY

Sample size: ~330 requests

__EC2 instance HTTP request time:__ 1ms average

(No HTTPS)

__EC2 instance HTTP + CloudFront HTTPS:__ 7ms average (min: 64ms, max: 21ms, std dev: 1ms)

(Same results with HTTP or HTTPS)

__Lambda+APIG HTTPS request time:__
- Total time: 23ms average (min: 14ms, max: 107ms, std dev: 11ms)
- APIG Latency: 21ms average
- APIG Integration Latency: 18ms average
- Lambda execution time: 1ms average





[Definitions:](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-metrics-and-dimensions.html)

> __Integration Latency:__ The time between when API Gateway relays a request to the back end and when it receives a > response from the back end.

> __Latency:__ The time between when API Gateway receives a request from a client and when it returns a response to the client. The latency includes the integration latency and other API Gateway overhead.
