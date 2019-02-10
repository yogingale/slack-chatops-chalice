# Slack + AWS Chalice + Your Python Fuctions

Slack commands integration with regular operations tasks is what your development and operations team needs. This codebase have a **Skeleton for Master and Slave Lambda functions integration using SNS service**.
You'll get some ready to use slack commands for Operations team in web development.


## Pre-requisits:
- Python 3.6+
- ```pip install chalice```
- [AWS acceess credentials](https://aws.amazon.com/blogs/security/wheres-my-secret-access-key/) in ```~/.aws/config```
- Generate [slack_API_token](https://get.slack.help/hc/en-us/articles/215770388-Create-and-regenerate-API-tokens) and [AWS SNS Topic](https://docs.aws.amazon.com/gettingstarted/latest/deploy/creating-an-sns-topic.html)
- Add above slack token and SNS topic in ```.chalice/config.json``` file as environment variables.


## Usage:
- ```git clone <this repository>```
- ```cd slack-chatops-chalice```
- Add your own python functions in ```app.py``` and ```/chalicelib/workers.py``` Or Make use of available web operation team's functions.
- ```chalice deploy```
- [Create simple Slack commands](https://api.slack.com/tutorials/easy-peasy-slash-commands) and add API Gateway links created with ```chalice deploy``` command.