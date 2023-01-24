import boto3
import datetime
import time
import re
import os
import sys

# S3 and Athena client
s3 = boto3.client('s3')
athena = boto3.client('athena')

# Get Year, Month, Day for partition
date = datetime.datetime.now()
athena_year = str(date.year)
athena_month = str(date.month).rjust(2, '0')
athena_day = str(date.day).rjust(2, '0')

# Parameters for S3 log location and Athena table (Fill this carefully)
s3_bucket_flow_log = os.environ.get('S3_BUCKET_FLOW_LOG')  # '<s3 bucket name where flow logs will be stored>'
# '<prefix for VPC flow logs that comes after bucket name>' e.g. 'vpc-flow-logs'
s3_account_prefix = "AWSLogs/" if os.environ.get('S3_ACCOUNT_PREFIX') == "" else os.environ.get('S3_ACCOUNT_PREFIX') + "/AWSLogs/"
s3_ouput = f"s3://{os.environ.get('S3_OUTPUT')}/query_output/"
# e.g. 's3://aws-athena-query-results-us-east-1-<account number>'
table_name = os.environ.get('TABLE_NAME')  # '<Athena table name for VPC flow logs>'
database = os.environ.get('DATABASE')
frequency = os.environ.get('FREQUENCY')

# Executing the athena query:
def run_query(query, database, s3_output):
    try:
        query_response = athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': database
            },
            ResultConfiguration={
                'OutputLocation': s3_output,
            }
        )

        execution_id = query_response['QueryExecutionId']
        state = 'RUNNING'
        while (state in ['RUNNING', 'QUEUED']):
            response = athena.get_query_execution(
                QueryExecutionId=execution_id)
            if 'QueryExecution' in response and 'Status' in response['QueryExecution'] and 'State' in \
                    response['QueryExecution']['Status']:
                state = response['QueryExecution']['Status']['State']
                if state == 'FAILED':
                    print(response)
                    print("state == FAILED")
                    print('Execution ID: ' +
                          query_response['QueryExecutionId'])
                    return False
                elif state == 'SUCCEEDED':
                    s3_path = response['QueryExecution']['ResultConfiguration']['OutputLocation']
                    filename = re.findall('.*\/(.*)', s3_path)[0]
                    return filename
            time.sleep(1)
    except Exception as e:
        print("Query Exception:- ", e)

    return query_response


# Function to get the regions and run the query on the captured regions
def lambda_handler(event, context):
    errs = None
    status = "SUCCESS"
    account_id = None
    region = None

    account_result = s3.list_objects(
        Bucket=s3_bucket_flow_log, Prefix=s3_account_prefix, Delimiter='/')
    print(account_result)

    if event.get("RequestType") == 'Delete':
        status = "SUCCESS"
        return {
            "status": status
        }
        # cfnresponse.send(event, context, status, errs,
        #                  event["LogicalResourceId"])
    else:
        try:
            for accounts in account_result.get('CommonPrefixes'):
                get_account = (accounts.get('Prefix', '').replace(
                    s3_account_prefix, '').replace('/', ''))
                print(f"Account:  {get_account}")
                if get_account.find("=") > 0:
                    account_id = get_account.split("=")[1]
                else:
                    account_id = get_account
                    
                s3_prefix = s3_account_prefix + get_account + '/vpcflowlogs/'
                s3_input = 's3://' + s3_bucket_flow_log + '/' + s3_prefix

                result = s3.list_objects(
                    Bucket=s3_bucket_flow_log, Prefix=s3_prefix, Delimiter='/')
                print(result)

                for regions in result.get('CommonPrefixes'):
                    get_region = (regions.get('Prefix', '').replace(
                        s3_prefix, '').replace('/', ''))
                    print(f"Region:  {get_region}")
                    if get_region.find("=") > 0:
                        region = get_region.split("=")[1]
                    else: 
                        region = get_region
                    print(f"Region2:  {region}")
                    print(f"database:  {database}")
                    print(f"table_name:  {table_name}")
                    print(f"account_id:  {account_id}")
                    print(f"athena_year:  {athena_year}")
                    print(f"athena_month:  {athena_month}")
                    print(f"athena_day:  {athena_day}")
                    
                    query = str("ALTER TABLE " + database + "." + table_name + " ADD PARTITION (`aws-account-id`=\""
                                + account_id + "\", `aws-service`=\"vpcflowlogs\", `aws-region`=\""
                                + region + "\", year=\""
                                + athena_year + "\", month=\""
                                + athena_month + "\", day=\""
                                + athena_day + "\"")
                    if frequency == "Hourly":
                        query += ", hour=\"00\")"
                    else:
                        query += ")"
                    query += " location '" + s3_input + get_region + "/" + \
                        athena_year + "/" + athena_month + "/" + athena_day
                    if frequency == "Hourly":
                        query += "/00';"
                    else:
                        query += "';"
                    ## Enable below prints for debugging ##
                    print("*" * 10, "START",  "*" * 10)  # -- for debug
                    print(get_region)  # -- for debug
                    print(query)  # -- for debug
                    print("*" * 10, "START",  "*" * 10)  # -- for debug
                    print(database)  # -- for debug
                    print(s3_ouput)  # -- for debug

                    query_result = run_query(query, database, s3_ouput)

                    print(query_result)  # -- for debug
                    print("*" * 10, "END",  "*" * 10)  # -- for debug
                status = "SUCCESS"
        except Exception as e:
            print("lambda_handler Exception:- ", e)
            errs = e
            status = "FAILED"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        finally:
            if event.get("RequestType") != None:
                return {
                    "status": status
                }
                # cfnresponse.send(event, context, status,
                #                  {}, event.get("LogicalResourceId"))
