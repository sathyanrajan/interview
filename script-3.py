import logging
import boto3
import time
import sys
import argparse
from botocore.config import Config

logging.basicConfig(format='[%(asctime)s.%(msecs)d] %(levelname)-1s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

global client


def get_flag(state: str):
    return True if state == 'Enabled' else False


allowed_states = ['Enabled', 'Disabled']


def update_state(function_name: str, desired_state: str):
    global client
    if desired_state not in allowed_states:
        logger.error("Invalid states passed. Allowed states are {}".format(allowed_states))
        raise
    try:
        response = client.list_event_source_mappings(
            FunctionName=('%s' % function_name),
            MaxItems=10
        )
        
        for event_source_mapping in response['EventSourceMappings']:
            uuid_from_response = event_source_mapping['UUID']
            logger.info("\nProcessing for event source mapping: {}".format(event_source_mapping['EventSourceArn']))
        
            response = client.update_event_source_mapping(
                UUID=uuid_from_response,
                FunctionName=function_name,
                Enabled=get_flag(desired_state))
            logger.info("Response from the API call : {}".format(response))
        
            response_status = client.get_event_source_mapping(
                UUID=uuid_from_response
            )
        
            count = 0
            wait_in_secs = 10
            while True:
                current_state = response_status['State']
                if current_state != desired_state:
                    logger.info(
                        "Waiting on the trigger {} of function {}  to be {}. {} seconds elapsed on waiting. Current "
                        "state is {}".format(
                            uuid_from_response, function_name, desired_state, count * wait_in_secs, current_state))
                    count = count + 1
                    time.sleep(wait_in_secs)
                    response_status = client.get_event_source_mapping(
                        UUID=uuid_from_response
                    )
                else:
                    logger.info(
                        "Done waiting on the trigger {} of function {}  to be {}. {} seconds elapsed on waiting. "
                        "Current state is {}".format(
                            uuid_from_response, function_name, desired_state, count * wait_in_secs, current_state))
                    break

    except Exception as exe:
        logger.fatal()
        raise exe


def main(argv):
    session = boto3.Session()
    arg_parser = argparse.ArgumentParser()
    arg_parser.description = 'Srcipts expects AWS Region, list of lambda functions and the desired state of the trigger'
    arg_parser.add_argument('region', help='AWS Region')
    arg_parser.add_argument('list_of_functions', help='comma separated list of functions')
    arg_parser.add_argument('desired_state', help='Possible values are [Enabled, Disabled')

    args = arg_parser.parse_args()
    print(args)
    global client
    region_config = Config(region_name=args.region)
    client = session.client('lambda', config=region_config)

    for function in args.list_of_functions.split(','):
        update_state(function, args.desired_state)


if __name__ == "__main__":
    main(sys.argv[1:])
