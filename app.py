import json
from chalice import Chalice, Cron
from urllib.parse import parse_qs
import boto3
from slacker import Slacker
import os
from chalicelib.helpers import get_ssl_information, get_domain_nameServers,\
    get_A_record, get_CNAME_record, get_domain_type


app = Chalice(app_name='chatops1')
app.debug = True


@app.route('/ssl-info', methods=['POST'], content_types=['application/json',
                                                         'application/x-www-form-urlencoded'])
def ssl_info():
    parsed = parse_qs(app.current_request.raw_body.decode())
    domain = parsed.get('text')
    #domain = 'google.com'
    if domain is None:
        message = '*Domain name* can not be *blank*! \n Usage: `/ssl-info domain.com`'
        return {
            'statusCode': 200,
            'response_type': 'ephemeral',
            'text': message
        }
    else:
        domain = domain[0]
        message = '*Domain* \t *Issued to* \t *Valid till* \n'
        info = get_ssl_information(domain)
        issued_to = info['Issued to']
        validity = info['Valid till']
        message += f'{domain} \t {issued_to} \t {validity} \n'

        return {
            'statusCode': 200,
            'response_type': 'ephemeral',
            'text': message
        }


@app.route('/ssl-info-list', methods=['POST'], content_types=['application/json',
                                                              'application/x-www-form-urlencoded'])
def ssl_info_list():
    parsed = parse_qs(app.current_request.raw_body.decode())
    domains = parsed.get("text")
    user_id = parsed.get("user_id")
    channel_name = parsed.get("channel_name")

    if domains is None:
        message = '*Domain names* can not be *blank*! \n Usage: `/ssl-info domain.com,google.com,www.facebook.com`'
        return {
            'statusCode': 200,
            'response_type': 'ephemeral',
            'text': message
        }
    else:
        data = {'user_id': user_id[0], 'channel_name': channel_name[0],
                'function': 'ssl_info_list', 'domains': domains[0]}
        sns_client = boto3.client('sns')

        sns_client.publish(
            TopicArn=os.getenv('TopicArn'),
            MessageStructure='json',
            Message=json.dumps({'default': json.dumps(data)})
        )
        return {
            'statusCode': 200,
            'response_type': 'ephemeral',
            'text': '*Hold Tight!!* _I\'m Working on your request_ :robot_face: :popcorn:'
        }


@app.route('/dns-check', methods=['POST'], content_types=['application/json',
                                                          'application/x-www-form-urlencoded'])
def dns_check():
    parsed = parse_qs(app.current_request.raw_body.decode())
    domain = parsed.get('text')
    #domain = 'google.com'
    if domain is None:
        message = '*Domain name* can not be *blank*! \n Usage: `/dns-check domain.com`'
        return {
            'statusCode': 200,
            'response_type': 'ephemeral',
            'text': message
        }
    else:
        domain = domain[0]
        message = '*Domain* \t *A record* \t *CNAME record* \t *NameServers* \n'
        data = {}
        data[domain] = [get_A_record(domain), get_CNAME_record(
            domain), get_domain_nameServers(domain)]

        for d, values in data.items():
            a_record = values[0]['A record']
            cname_record = values[1]['CNAME record']
            ns = values[2]['Nameservers']
            message += f'{domain} \t {a_record} \t {cname_record} \t {ns}\n'

        return {
            'statusCode': 200,
            'response_type': 'ephemeral',
            'text': message
        }


@app.route('/dns-check-list', methods=['POST'], content_types=['application/json',
                                                               'application/x-www-form-urlencoded'])
def dns_check_list():
    parsed = parse_qs(app.current_request.raw_body.decode())
    domains = parsed.get("text")
    user_id = parsed.get("user_id")
    channel_name = parsed.get("channel_name")

    if domains is None:
        message = '*Domain names* can not be *blank*! \n Usage: `/dns-check-list google.com,www.domain.com`'
        return {
            'statusCode': 200,
            'response_type': 'ephemeral',
            'text': message
        }
    else:
        data = {'user_id': user_id[0], 'channel_name': channel_name[0],
                'function': 'dns_check_list', 'domains': domains[0]}
        sns_client = boto3.client('sns')

        sns_client.publish(
            TopicArn=os.getenv('TopicArn'),
            MessageStructure='json',
            Message=json.dumps({'default': json.dumps(data)})
        )
        return {
            'statusCode': 200,
            'response_type': 'ephemeral',
            'text': '*Hold Tight!!* _I\'m Working on your request_ :robot_face: :popcorn:'
        }


@app.route('/domain-type', methods=['POST'], content_types=['application/json',
                                                            'application/x-www-form-urlencoded'])
def domain_type():
    parsed = parse_qs(app.current_request.raw_body.decode())
    domain = parsed.get('text')
    #domain = 'google.com'
    if domain is None:
        message = '*Domain name* can not be *blank*! \n Usage: `/domain-type domain.com`'
        return {
            'statusCode': 200,
            'response_type': 'ephemeral',
            'text': message
        }
    else:
        domain = domain[0]
        message = '*Domain* \t *Domain type* \n'

        info = get_domain_type(domain)
        domain_type = info['Domain type']
        message += f'{domain} \t {domain_type} \n'

        return {
            'statusCode': 200,
            'response_type': 'ephemeral',
            'text': message
        }


@app.route('/domain-type-list', methods=['POST'], content_types=['application/json',
                                                                 'application/x-www-form-urlencoded'])
def domain_type_list():
    parsed = parse_qs(app.current_request.raw_body.decode())
    domains = parsed.get("text")
    user_id = parsed.get("user_id")
    channel_name = parsed.get("channel_name")
    if domains is None:
        message = '*Domain names* can not be *blank*! \n Usage: `/domain-type-list google.com,www.domain.com`'
        return {
            'statusCode': 200,
            'response_type': 'ephemeral',
            'text': message
        }
    else:
        data = {'user_id': user_id[0], 'channel_name': channel_name[0],
                'function': 'domain_type_list', 'domains': domains[0]}
        sns_client = boto3.client('sns')

        sns_client.publish(
            TopicArn=os.getenv('TopicArn'),
            MessageStructure='json',
            Message=json.dumps({'default': json.dumps(data)})
        )
        return {
            'statusCode': 200,
            'response_type': 'ephemeral',
            'text': '*Hold Tight!!* _I\'m Working on your request_ :robot_face: :popcorn:'
        }


@app.on_sns_message(topic='chatops-lambda-invoker')
def slave_lambda(event):
    #app.log.debug("Received message with message: %s",event.message)
    #app.log.debug(f"Response URL is: {event.to_dict()}")

    slack = Slacker(os.getenv('slack_API_token'))

    data = json.loads(event.message)
    user_id = data.get('user_id', 'Not Found')
    channel_name = data.get('channel_name', 'Not Found')
    domains = data.get('domains', 'Not Found')

    def domain_type_list():
        domains1 = [domain.strip() for domain in domains.split(',')]
        message = '*Domain* \t *Domain type* \n'
        for domain in domains1:
            data = {}
            data[domain] = [get_domain_type(domain)]

            for d, values in data.items():
                domain_type = values[0]['Domain type']
                message += f'{d} \t {domain_type}\n'

        slack.chat.post_ephemeral(channel_name, message, user_id)

    def dns_check_list():
        domains1 = [domain.strip() for domain in domains.split(',')]
        message = '*Domain* \t *A record* \t *CNAME record* \t *NameServers* \n'
        for domain in domains1:
            data = {}
            data[domain] = [get_A_record(domain), get_CNAME_record(
                domain), get_domain_nameServers(domain)]

            for d, values in data.items():
                a_record = values[0]['A record']
                cname_record = values[1]['CNAME record']
                ns = values[2]['Nameservers']
                message += f'{d} \t {a_record} \t {cname_record} \t {ns}\n'

        slack.chat.post_ephemeral(channel_name, message, user_id)

    def ssl_info_list():
        domains1 = [domain.strip() for domain in domains.split(',')]
        message = '*Domain* \t *Issued to* \t *Valid till* \n'
        for domain in domains1:
            info = get_ssl_information(domain)
            issued_to = info['Issued to']
            validity = info['Valid till']
            message += f'{domain} \t {issued_to} \t {validity} \n'

        slack.chat.post_ephemeral(channel_name, message, user_id)

    exec(data['function'] + '()')