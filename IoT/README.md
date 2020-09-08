[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/CiscoDevNet/scc-ckc-api-examples)

# Cisco Kinetic for Cities API Examples
The Smart+Connected Digital Platform is now Cisco Kinetic for Cities. It’s a new name but the same platform that delivers a set of tools and guidelines for creating a smart city framework. This repo contains short example scripts that demonstrate and explain aspects of the Cisco Kinetic for Cities APIs.

Examples
There are currently three example Python scripts in this repo:

[CKC101_python_example.py](./CKC101_python_example.py) - Authentication and API Requests

This sample script demonstrates logging into the Cisco Kinetic for Cities Platform and making a request. All Cisco Kinetic for Cities APIs (except authentication) require an access token. In this example, the access token is obtained through the `/token` API and used to make another API request.

[CKC102_python_example.py](./CKC102_python_example.py) - Retrieving Information from the Cisco Kinetic for Cities Platform

This sample script demonstrates making several Cisco Kinetic for Cities API calls. In this example, additional information about the locations available to the current user and about the capabilities of the Cisco Kinetic for Cities instance itself are retrieved.

[CKC103_python_example.py](./CKC103_python_example.py) - Requesting Real Time Data from the Cisco Kinetic for Cities Platform

This sample script demonstrates getting Real Time Data from the Cisco Kinetic for Cities Platform. In this example, real time device information for lighting is retrieved and visualized as a simple pie chart.
