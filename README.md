# Stem Demo

This is the source code repo for a demo application that generates sensor data.  The data is sent from a simulated IoT device to AWS IoT core with a rule topic that then sends the data to AWS Timeseries.  Grafana Cloud is then used to query the timeseries database to build observability dashboards.