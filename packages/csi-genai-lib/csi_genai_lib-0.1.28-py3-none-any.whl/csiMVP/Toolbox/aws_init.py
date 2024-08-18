# ##################################################################################################
#  Copyright (c) 2022.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  Filename:  aws_init.py                                                                          #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

"""
This module attempts to abstract away the complexities of dealing with multiple types of AWS_S3-like object
store services.  Even though https://pypi.org/project/smart-open/ gives us the ability to read and write objects
and files from many types of sources, there are source-dependent quirks that have to be dealt with.

For example, although Min.io is supposed to be completely S3 compatible, it requires a username:password
combo to be passed and the S3 client must have the URL of the Minio host defined.

The other quirk is that for use internal to Caber services we can use AWS_S3 or another source, and customers
can define multiple types of hosts simultaneously.  All of these we keep track of here.

"""

import os
import json
import pytz
import boto3
from uuid import uuid4
from datetime import datetime
from time import time

from boto3 import Session
from .json_encoder import extEncoder
from urllib.parse import urlparse
from smart_open.smart_open_lib import patch_pathlib
from botocore.config import Config as boto3config
from botocore.exceptions import ClientError
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session

# THIS MODULE IS IMPORTED INTO Common.init so we cannot import CFG here!
#   NO -->  from ..Common.init import CFG

# ############# INCLUDE HERE THE NAMES OF TESTED OBJECT STORE TYPES ################ #
#   These form the possible choices for:
#          CFG.D['Object_Sources'][<host-name>]['type']
#          CFG.D["Dependencies"]["shared-storage"]["targets"][<host-name>]['type']
#
AWS_S3_SHORT_NAME = 's3aws'
AWS_S3_NAME = 's3.amazonaws.com'
SupportedS3likeStoreTypes = [AWS_S3_NAME, 'minio']
# ################################################################################## #

_ = patch_pathlib()  # replace `Path.open` with `smart_open.open`



class RefreshableBotoSession:
    """
    From https://stackoverflow.com/questions/63724485/how-to-refresh-the-boto3-credentials-when-python-script-is-running-indefinitely
    Boto Helper class which lets us create a refreshable session so that we can cache the client or resource.

    Usage
    -----
    session = RefreshableBotoSession().refreshable_session()

    client = session.client("s3") # we now can cache this client object without worrying about expiring credentials
    """

    def __init__(
        self,
        region_name: str = None,
        profile_name: str = None,
        access_key: str = None,
        secret_key: str = None,
        sts_arn: str = None,
        session_name: str = None,
        session_ttl: int = 1500
    ):
        """
        Initialize `RefreshableBotoSession`

        Parameters
        ----------
        region_name : str (optional)
            Default region when creating a new connection.

        profile_name : str (optional)
            The name of a profile to use.

        sts_arn : str (optional)
            The role arn to sts before creating a session.

        session_name : str (optional)
            An identifier for the assumed role session. (required when `sts_arn` is given)

        session_ttl : int (optional)
            An integer number to set the TTL for each session. Beyond this session, it will renew the token.
            25 minutes by default which is before the default role expiration of 1 hour
        """

        self.region_name = region_name
        self.profile_name = profile_name
        self.sts_arn = os.getenv('CSI_TENANT_ROLE_ARN')
        self.ext_id = os.getenv('CSI_ROLE_EXTERNAL_ID')
        self.session_name = session_name or uuid4().hex
        self.session_ttl = session_ttl
        self.access_key = os.environ.get('CSI_AWS_ACCESS_KEY')
        self.secret_key = os.environ.get('CSI_AWS_SECRET_KEY')
        self.session = None

    def __get_new_session(self):
        """
        Get session credentials
        """
        if self.profile_name:
            print(f"RefreshableBotoSession: Using session credentials from profile {self.profile_name}")
            self.session = Session(region_name=self.region_name, profile_name=self.profile_name)
        elif self.access_key and self.secret_key:
            print(f"RefreshableBotoSession: Using session credentials from environment variables")
            self.session = Session(region_name=self.region_name, aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        else:
            print(f"RefreshableBotoSession: Using default session credentials")
            self.session = Session(region_name=self.region_name)

    def __get_session_credentials(self):
        if not self.session:
            self.__get_new_session()
        credentials = {}
        response = {}
        # if sts_arn is given, get credential by assuming the given role
        if self.sts_arn:
            print(f"RefreshableBotoSession: Assuming role from environment variables")
            try:
                sts_client = self.session.client(service_name="sts", config=aws_session_config)
                assumed_role_object = sts_client.assume_role(
                    RoleArn=self.sts_arn,
                    ExternalId=self.ext_id,
                    RoleSessionName=self.session_name,
                    DurationSeconds=self.session_ttl,
                )
                response = assumed_role_object.get("Credentials")
            except ClientError as err:
                print(f"[WARNING] assume_customer_role: Exception assuming Cross Account Role ${err}")
            else:
                credentials = {
                    "access_key": response.get("AccessKeyId"),
                    "secret_key": response.get("SecretAccessKey"),
                    "token": response.get("SessionToken"),
                    "expiry_time": response.get("Expiration").isoformat(),
                }
                print(f"RefreshableBotoSession: Assuming role successful. Session expiration: {credentials['expiry_time']}")

        if not credentials:
            session_credentials = self.session.get_credentials().get_frozen_credentials()
            credentials = {
                "access_key": session_credentials.access_key,
                "secret_key": session_credentials.secret_key,
                "token": session_credentials.token,
                "expiry_time": datetime.fromtimestamp(time() + self.session_ttl).replace(tzinfo=pytz.utc).isoformat(),
            }
            print(f"RefreshableBotoSession: Assuming role failed. Using base role for session. Session expiration: {credentials['expiry_time']}")

        os.environ['AWS_ACCESS_KEY_ID'] = credentials.get("access_key")
        os.environ['AWS_SECRET_ACCESS_KEY'] = credentials.get("secret_key")
        os.environ['AWS_SESSION_TOKEN'] = credentials.get("token")
        return credentials

    def refreshable_session(self) -> Session:
        """
        Get refreshable boto3 session.
        """
        # Get refreshable credentials
        initial_credentials = self.__get_session_credentials()
        refreshable_credentials = RefreshableCredentials.create_from_metadata(
            metadata=initial_credentials,
            refresh_using=self.__get_session_credentials,
            method="auto",
        )

        # attach refreshable credentials current session
        autorefresh_session = boto3.Session()
        autorefresh_session._session.set_credentials(refreshable_credentials)
        autorefresh_session._session.set_config_variable("region", self.region_name)
        autorefresh_session._session.set_config_variable("user_agent", user_agent)

        return autorefresh_session


def get_aws_regions():
    global AWS_REGIONS

    if AWS_REGIONS is None:
        client = new_aws_client('ec2')
        try:
            AWS_REGIONS = [region['RegionName'] for region in client.describe_regions()['Regions']]
        except ClientError as err:
            print(f"Using default for AWS Regions list. Add 'ec2:DescribeRegions' permissions.")
            AWS_REGIONS = ['ap-south-1', 'eu-north-1', 'eu-west-3', 'eu-west-2', 'eu-west-1',
                           'ap-northeast-3', 'ap-northeast-2', 'ap-northeast-1', 'ca-central-1',
                           'sa-east-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-central-1',
                           'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    return AWS_REGIONS


def check_s3_name(name):
    if 's3-scanner' in name or 's3_scanner' in name:
        return name
    s3list = ['s3', AWS_S3_SHORT_NAME, 'awss3', 'amazonawss3', 'amazons3', AWS_S3_NAME]
    if isinstance(name, str) and name.lower() in s3list or any([1 for x in s3list if x in name.lower()]):
        return AWS_S3_NAME
    else:
        return name


def url_to_from_arn(cfg, name, acct=None, region=None):
    fs = name.find('/')
    nc = name[:fs].count(':')
    if fs > 0 and nc == 1:   # One colon before first slash means it's a URL
        if acct is None:
            acct = aws_account_id
        if region is None:
            region = AWS.region_name
        url = urlparse(name)
        obj_type = cfg.D["Object_Sources"].get(check_s3_name(url.hostname), {}).get('type', '')
        arn = f"arn:{obj_type}:{url.scheme}:{region}:{acct}:{url.path}"
        return arn
    elif nc == 5:
        arn = name.split(':', 5)
        url = arn[2] + '://' + arn[-1]
        return url
    else:
        return name


notification_bucket_policy = '{"Version": "2012-10-17", "Statement": [{"Sid": "AWSCloudTrailAclCheck20150319", "Effect": "Allow", "Principal": {"Service": "cloudtrail.amazonaws.com"}, "Action": "s3:GetBucketAcl", "Resource": "%bk_arn%"}, {"Sid": "AWSCloudTrailWrite20150319", "Effect": "Allow", "Principal": {"Service": "cloudtrail.amazonaws.com"}, "Action": "s3:PutObject", "Resource": "%ct_arn%", "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}}, {"Sid": "AWSLogDeliveryWrite", "Effect": "Allow", "Principal": {"Service": "delivery.logs.amazonaws.com"}, "Action": "s3:PutObject", "Resource": "%cw_arn%", "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}}, {"Sid": "AWSLogDeliveryAclCheck", "Effect": "Allow", "Principal": {"Service": "delivery.logs.amazonaws.com"}, "Action": "s3:GetBucketAcl", "Resource": "%bk_arn%"}]}'
notification_topic_policy = '{"Version": "2008-10-17", "Id": "__default_policy_ID", "Statement": [{"Sid": "__default_statement_ID", "Effect": "Allow", "Principal": {"AWS": "*"}, "Action": ["SNS:GetTopicAttributes", "SNS:SetTopicAttributes", "SNS:AddPermission", "SNS:RemovePermission", "SNS:DeleteTopic", "SNS:Subscribe", "SNS:ListSubscriptionsByTopic", "SNS:Publish", "SNS:Receive"], "Resource": "%topic_arn%", "Condition": {"StringEquals": {"AWS:SourceOwner": "%aws_id%"}}}, {"Sid": "AWSCloudTrailSNSPolicy20150319", "Effect": "Allow", "Principal": {"Service": "cloudtrail.amazonaws.com"}, "Action": "SNS:Publish", "Resource": "%topic_arn%"}]}'
event_queue_policy_sns = '{"Version": "2008-10-17", "Id": "__default_policy_ID", "Statement": [{"Sid": "__owner_statement", "Effect": "Allow"," Principal": {"AWS":"*"},"Action": "SQS:*", "Resource": "%queue_arn%"}, {"Sid": "topic-subscription-%topic_arn%", "Effect": "Allow", "Principal": {"AWS":"*"}, "Action": "SQS:*", "Resource": "%queue_arn%", "Condition": {"ArnLike": {"aws:SourceArn": "%topic_arn%"}}}]}'
event_queue_policy = '{"Version": "2008-10-17", "Id": "__default_policy_ID", "Statement": [{"Sid": "__owner_statement", "Effect": "Allow"," Principal": {"AWS":"*"},"Action": "SQS:*", "Resource": "%queue_arn%"}]}'


def create_event_notification_bucket(cfg, event_bkt="csi-cloudtrail-events-"):
    if event_bkt.endswith('-'):
        event_bkt += aws_credentials.access_key

    evb = "create_new_bucket(cfg, event_bkt)"

    bk_arn = f"arn:aws:s3:::{event_bkt}"
    ct_arn = f"arn:aws:s3:::{event_bkt}/AWSLogs/{aws_account_id}/*"
    cw_arn = f"arn:aws:s3:::{event_bkt}/flow-logs/AWSLogs/{aws_account_id}/*"

    nb_policy = notification_bucket_policy.replace('%bk_arn%', bk_arn)\
                                          .replace('%ct_arn%', ct_arn)\
                                          .replace('%cw_arn%', cw_arn)

    resp = S3C.put_bucket_policy(Bucket=event_bkt, Policy=nb_policy)
    print(f"Added bucket policy to: {event_bkt}")
    return event_bkt


def create_sns_notification_topic(event_sns="csi-new-logfile-event-"):
    if event_sns.endswith('-'):
        event_sns += aws_credentials.access_key

    topic_arn = f"arn:aws:sns:{AWS.region_name}:{aws_account_id}:{event_sns}"
    lg_policy = notification_topic_policy.replace('%topic_arn%', topic_arn)\
                                         .replace('%aws_id%', aws_account_id)

    sns = new_aws_client('sns')

    try:
        sns_attr = sns.get_topic_attributes(TopicArn=topic_arn)
        sqs_q_name = create_sqs_q(sns_topic_arn=topic_arn)
    except Exception as err:
        sns_resp = sns.create_topic(Name=event_sns,
                                    Attributes={'Policy': lg_policy})
        sns_attr = sns.get_topic_attributes(TopicArn=topic_arn)
        sqs_q_name = create_sqs_q(sns_topic_arn=topic_arn)
        print(f"Created SNS topic: {event_sns}")
        return topic_arn
    else:
        return topic_arn


def create_sqs_q(sqs_queue="csi-s3-data-events-", sns_topic_arn=None):
    if sqs_queue.endswith('-'):
        sqs_queue += aws_credentials.access_key

    queue_arn = f"arn:aws:sqs:{AWS.region_name}:{aws_account_id}:{sqs_queue}"
    if sns_topic_arn is None:
        sq_policy = event_queue_policy.replace('%queue_arn%', queue_arn) \
                                      .replace('%aws_id%', aws_account_id)
    else:
        sq_policy = event_queue_policy_sns.replace('%queue_arn%', queue_arn) \
                                          .replace('%topic_arn%', sns_topic_arn)\
                                          .replace('%aws_id%', aws_account_id)

    sqs = new_aws_client('sqs')

    try:
        sqs_resp = sqs.set_queue_attributes(QueueName=sqs_queue,
                                            Attributes={'Policy': sq_policy})
    except Exception as err:
        sqs_resp = sqs.create_queue(QueueName=sqs_queue,
                                    Attributes={'Policy': sq_policy})
        sqs_attr = sqs.get_queue_attributes(QueueName=sqs_queue)
        print(f"Created SQS queue: {sqs_queue}")
        return sqs_queue
    else:
        return sqs_queue



from datetime import datetime, timezone


def post_status_to_cloudwatch(status):
    """
    Post a message to the specified AWS CloudWatch log group.

    Example Usage
    response = post_status_to_cloudwatch("This is a test message", "TestLogGroup")
    print(response)

    FORMAT_STRING: '[CSI-STATUS] {"group": "codebuild", "stage": "%s.%s", "message": "%s %s"}\n'

    :param status: The message to post
    """
    log_group = os.environ.get("CSI_STATUS_LOG_GROUP")

    if not log_group:
        # print(f"[WARNING] post_status_to_cloudwatch: Failed 'CSI_STATUS_LOG_GROUP' not set.")
        return False

    message = status.copy()

    sequence_token = None
    external_id = os.getenv('CSI_ROLE_EXTERNAL_ID')

    # timestamp the message
    timestamp = int(datetime.now(tz=timezone.utc).timestamp() * 1000)  # AWS uses milliseconds

    if isinstance(message, dict):
        message |= {'timestamp': timestamp, 'external_id': external_id}
        message = f"[CSI-STATUS] {json.dumps(message, cls=extEncoder)}"
        event = {'timestamp': timestamp, 'message': message}
    else:
        event = {'timestamp': timestamp, 'message': message}

    # Try to get the log streams
    try:
        streams = LOGS.describe_log_streams(logGroupName=log_group, limit=1)
    except LOGS.exceptions.ResourceNotFoundException:
        # If log group not found, create it and retry
        LOGS.create_log_group(logGroupName=log_group)
        streams = LOGS.describe_log_streams(logGroupName=log_group, limit=1)

    # If there are no streams, or the last stream is full, create a new stream
    if not streams['logStreams'] or 'uploadSequenceToken' not in streams['logStreams'][0]:
        stream_name = f'status-{int(datetime.now(tz=timezone.utc).timestamp())}'
        LOGS.create_log_stream(logGroupName=log_group, logStreamName=stream_name)
    else:
        # Use the existing stream
        stream = streams['logStreams'][0]
        stream_name = stream['logStreamName']
        sequence_token = stream.get('uploadSequenceToken')

    if sequence_token:
        # If sequence token exists, include it in the put request
        response = LOGS.put_log_events(
            logGroupName=log_group,
            logStreamName=stream_name,
            logEvents=[event],
            sequenceToken=sequence_token
        )
    else:
        # If not, exclude the sequence token
        response = LOGS.put_log_events(
            logGroupName=log_group,
            logStreamName=stream_name,
            logEvents=[event]
        )

    return response


'''
aws cloudtrail create-trail — name log-archive-trail — s3-bucket-name $s3_bucket_name — region $TARGET_REGION
aws cloudtrail put-event-selectors — trail-name log-archive-trail — region $TARGET_REGION — event-selectors ‘[{“ReadWriteType”: “All”,”IncludeManagementEvents”: true,”DataResources”: [{“Type”:”AWS::S3::Object”, “Values”: [“arn:aws:s3:::”]}]}]’
aws cloudtrail start-logging — name log-archive-trail
'''


def create_s3_cloudtrail(cfg, buckets, event_bkt="csi-cloudtrail-events-", event_sns="csi-new-logfile-event-"):

    ev_bkt_name = create_event_notification_bucket(cfg, event_bkt)
    sns_topic_arn = create_sns_notification_topic(event_sns)

    ct = new_aws_client('cloudtrail')
    trail_name = f'csi-s3-trail-{aws_credentials.access_key}'

    trail = ct.create_trail(Name=trail_name,
                            S3BucketName=ev_bkt_name,
                            SnsTopicName=sns_topic_arn,
                            IncludeGlobalServiceEvents=False,
                            IsMultiRegionTrail=True,
                            EnableLogFileValidation=False)

    ct_event_selectors = '[{"ReadWriteType":"All", "IncludeManagementEvents":false, "DataResources": [{"Type": "AWS::S3::Object", "Values": %bkt_arns%}], "ExcludeManagementEventSources":[]}]'

    bkt_arns = []
    for bkt in buckets:
        if bkt.count('arn'):
            if bkt.endswith('/'):
                bkt_arns.append(bkt)
            else:
                bkt_arns.append(bkt + '/')
        else:
            if bkt.endswith('/'):
                bkt_arns.append(f"arn:aws:s3:::{bkt}")
            else:
                bkt_arns.append(f"arn:aws:s3:::{bkt}/")

    if bkt_arns:
        bkts = json.dumps(bkt_arns)
        ct_event_selectors.replace('%bkt_arns%', bkts)
        ct.put_event_selectors(TrailName=trail_name, EventSelectors=json.loads(ct_event_selectors))
        ct.start_logging(Name=trail_name)

    return


def assume_customer_role():
    global AWS
    global aws_credentials
    global aws_account_id

    # Fetch the credentials from environment variables
    access_key = os.environ.get('CSI_AWS_ACCESS_KEY')
    secret_key = os.environ.get('CSI_AWS_SECRET_KEY')

    if not access_key or not secret_key:
        print(f"[WARNING] assume_customer_role: Failed 'CSI_AWS_ACCESS_KEY' and/or 'CSI_AWS_SECRET_KEY' not set.")
        return False

    try:
        # Create an STS client using the credentials from SecretsManager
        sts_client = boto3.client(
            'sts',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
    except ClientError as err:
        print(f"[WARNING] assume_customer_role: Exception creating sts_client ${err}")
        return False

    cross_account_role_arn = os.environ.get('CSI_TENANT_ROLE_ARN')
    cross_account_role_external_id = os.environ.get('CSI_ROLE_EXTERNAL_ID')
    if not cross_account_role_arn or not cross_account_role_external_id:
        print(f"[WARNING] assume_customer_role: Failed 'CSI_TENANT_ROLE_ARN' and/or 'CSI_ROLE_EXTERNAL_ID' not set.")
        return False

    try:
        assumed_role_object = sts_client.assume_role(
            RoleArn=cross_account_role_arn,
            RoleSessionName="CrossAccountAssumptionSession",
            ExternalId=cross_account_role_external_id
        )
    except ClientError as err:
        print(f"[WARNING] assume_customer_role: Exception assuming Cross Account Role ${err}")
        return False

    # Credentials from the assumed role
    assumed_credentials = assumed_role_object.get('Credentials', {})
    if not {'AccessKeyId', 'SecretAccessKey', 'SessionToken'}.intersection(assumed_credentials.keys()):
        print(f"[WARNING] assume_customer_role: STS returned incomplete credentials when assuming the Cross Account Role")
        return False

    os.environ['AWS_ACCESS_KEY_ID'] = assumed_credentials['AccessKeyId']
    os.environ['AWS_SECRET_ACCESS_KEY'] = assumed_credentials['SecretAccessKey']
    os.environ['AWS_SESSION_TOKEN'] = assumed_credentials['SessionToken']

    try:
        AWS = boto3.session.Session()
        aws_credentials = AWS.get_credentials()
        aws_account_id = AWS.client('sts').get_caller_identity().get('Account', '')
    except Exception as err:
        print(f"[WARNING] assume_customer_role: After assuming cross account role sts.get_caller_identity() failed")
        return False

    return True


#
# TRY TO ASSUME THE CUSOMTER ROLE AN IF THAT FAILS TRY TO USE WHATEVER CREDENTIALS ARE AVAILABLE
# INHERITED FROM THE CONTAINER OR THE INSTANCE IT RUNS ON.
#
AWS = None
aws_credentials = {}
aws_account_id = ''

try:
    AWS = RefreshableBotoSession().refreshable_session()  # boto3.session.Session()
    aws_credentials = AWS.get_credentials()
    aws_account_id = AWS.client('sts').get_caller_identity().get('Account', '')
except Exception as err:
    print(f"[WARNING] aws_init: RefreshableBotoSession Failed. Falling back to assume_customer_role")
    if not assume_customer_role():
        print(f"[WARNING] aws_init: assume_customer_role Failed. Falling back to boto3.session.Session()")
        try:
            AWS = boto3.session.Session()
            aws_credentials = AWS.get_credentials()
            aws_account_id = AWS.client('sts').get_caller_identity().get('Account', '')
        except Exception as err:
            print(f"[WARNING] aws_init: Exception on initial call to sts.get_caller_identity and failed to assume customer role.  This is bad...\n{err} ")
            aws_account_id = ''

user_agent = f"csi.{__package__}.{aws_credentials.access_key}"
aws_session_config = boto3config(
    user_agent=user_agent,
    connect_timeout=7,
    read_timeout=20
)

if os.getenv("AWS_ACCESS_KEY_ID", None) is None:
    os.environ["AWS_ACCESS_KEY_ID"] = aws_credentials.access_key

if os.getenv("AWS_SECRET_ACCESS_KEY", None) is None:
    os.environ["AWS_SECRET_ACCESS_KEY"] = aws_credentials.secret_key

if os.getenv("AWS_ACCOUNT_ID", None) is None:
    os.environ["AWS_ACCOUNT_ID"] = aws_account_id

if os.getenv("AWS_DEFAULT_REGION", None) is None:
    if AWS.region_name is not None:
        os.environ["AWS_DEFAULT_REGION"] = AWS.region_name
    else:
        os.environ["AWS_DEFAULT_REGION"] = 'us-west-1'


def new_aws_client(name='s3'):
    return AWS.client(name, config=aws_session_config)


def new_aws_resource(name='s3'):
    return AWS.resource(name, config=aws_session_config)


S3C = new_aws_client()
S3R = new_aws_resource()
LOGS = new_aws_client('logs')

Default_S3 = {"type": "s3",
              "url": "https://s3.amazonaws.com",
              "smartOpenPfx": "s3://",
              "id_prefix": "s3aws",
              "client": S3C,
              "transport_params": None}

AWS_REGIONS = None