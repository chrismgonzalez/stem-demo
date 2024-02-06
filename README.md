# Stem Demo

This is the source code repo for a demo application that generates sensor data.  The data is sent from a simulated IoT device to AWS IoT core with a rule topic that then sends the data to AWS Timeseries.  Grafana Cloud is then used to query the timeseries database to build observability dashboards.

The `sensordata.py` file can be used deployed on IoT devices such as a RasperryPi, ESP32 device, etc.  For the purposes of this demo I am running the Python script from within an Cloud9 EC2 instances, but this can also be run from your local machine provided you have the proper AWS credentials/IAM roles attached to your identity.

Inspiration for this demo was sourced from an existing `awslabs` Github repo which you can find [here](https://github.com/awslabs/amazon-timestream-tools/tree/mainline/integrations/iot_core).  I simply modified the Python script and added the Grafana Cloud observability component.

## What is created

This demo used CloudFormation to deploy the necessary infrastructure that includes:

* An AWS Timeseries database and database table.
* An Iot topic rule.
* An IAM role to allow the AWS IoT service to write data to AWS Timeseries on your behalf.

## Pre-requisites

* You have an active AWS account, you can create one [here](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all)
* Your user or IAM instance role (if you're using an EC2/Cloud9 instance) has proper IAM permissions to write to the Iot Data endpoint
  * You will need this policy:
    ```json
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iot:Connect",
                "iot:Publish",
                "iot:GetThingShadow",
                "iot:UpdateThingShadow",
            ],
            "Resource": "*"
        }
    ]
}
    ```
* Your runtime environment (the computer or device you are running this program on) has [Python3 and Pip3 installed]. If you're using a fairly new computer, you probably already have a recent version of Python installed.
  * On a mac `which python3` and `which pip3`

## IaC deployment

* Navigate to the CloudFormation console and create a new stack through the `upload a template file` option using the provided `cfn-iot-rule-to-timestream.json` file.
* Change the dimensions and SQL of the data rule to match your use case (reference lines 19-66 of `cfn-iot-rule-to-timestream.json`)
* Specify stack details and options for your deployment and create the stack.
* Optional but not provided: use Cloudformation to also create AWS Cloud9 development machine with an attached instance role that allows writing to IoT core thing endpoint.


## Installation

* After you have cloned the repository or copied the files to your device (optional) change directory into the `stem-demo` folder and run `pip3 install -r requirements.txt`

## Verify your IAM access

In order to verify that your instance profile, IAM user, or IAM role has the proper access run the following commands:

```sh
# check your authentication
aws sts get-caller-identity
# {
#     "UserId": "<access_key:<email>",
#     "Account": "<account_number",
#     "Arn": "arn:aws:sts::<account>:assumed-role/<role_details>"
# }
# make sure you can retrieve the endpoint for your IoT thing from your local machine, device, or ec2
# if you receive an error you don't have an endpoint or your IAM access is not correct

aws iot describe-endpoint
# <endpoint_id>.iot.<region>.amazonaws.com


```

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