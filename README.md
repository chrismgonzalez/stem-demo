# Stem Demo

This is the source code repo for a demo application that generates sensor data.  The data is sent from a simulated IoT device to AWS IoT core with a rule topic that then sends the data to AWS Timeseries.  Grafana Cloud is then used to query the timeseries database to build observability dashboards.

The `sensordata.py` file can be used deployed on IoT devices such as a RasperryPi, ESP32 device, etc.  For the purposes of this demo I am running the Python script from within an Cloud9 EC2 instances, but this can also be run from your local machine provided you have the proper AWS credentials/IAM roles attached to your identity.

Inspiration for this demo was sourced from an existing `awslabs` Github repo which you can find [here](https://github.com/awslabs/amazon-timestream-tools/tree/mainline/integrations/iot_core).  I simply modified the Python script and added the Grafana Cloud observability component.

## What is created

This demo used CloudFormation to deploy the necessary infrastructure that includes:

* An AWS Timeseries database and database table
* A an Iot topic rule
* An IAM role to allow the AWS IoT service to write data to AWS Timeseries on your behalf

## IaC deployment

* Navigate to the CloudFormation console and create a new stack through the `upload a template file` option using the provided `cfn-iot-rule-to-timestream.json` file.
* Change the dimensions and SQL of the data rule to match your use case (reference lines 19-66 of `cfn-iot-rule-to-timestream.json`)
* Specify stack details and options for your deployment and create the stack.
* Optional but not provided: use Cloudformation to also create AWS Cloud9 development machine with an attached instance role that allows writing to IoT core thing endpoint.

## Running the code

* The `sensordata.py` file is copied to your IoT device, local machine, or git cloned from this repo to your Cloud9 instance.
* Change your data points to match your use case
* Simply run `python3 sensordata.py` and watch the logs to be sure you are receiving a `200 OK` response from the IoT data service.

## Troubleshooting

* Sensor data is not being sent to IoT core
  * Check that your AWS credentials/SSO profile is correct and you have the appropriate access
  * If using a Raspi, you may have certs that need to be passed during authentication.  Be sure those certs are properly referenced in your sourcecode
* Sensor data is sending to AWS but is not arriving in the Timeseries DB
  * Make sure your message routing rule accepts a wild card for your sensors, it will probably need to look something like `dt/sensor/+`.

## Supporting documentation

* Coming soon