# Clouder
Testing harness in multi-cloud environment with light approach for API and data testing


Project goal is to experiement with main purpose cloud platforms (AWS, GCP, Azure) to 1) create abstraction layer for testing 2) make tests highly reusable across clouds, yet have them dynamic thru data parametrization and simple API interactions 3) enable in-production testing (safe and simple)

Demonstrates:
- client abstraction for key cloud operations for testers (invoke cloud specific function and pass result, upload/download file to/from cloud storage, create/query/update/delete noSQL data items of corresponding cloud)
- ability to work with AWS, GCP and Azure in one test case context. E.g. of test case:
1) Run GCP function, obtain its result and save the result into AWS dynamodb.
2) Verify inserted data equals to GCP function output
- How to make it all withing pytest and unittest
- Coming soon  - feature flagging on different clouds, additional cloud features like monitoring and telemetry for NFR testing, muti-threading support for load&perf testing of main cloud operations
