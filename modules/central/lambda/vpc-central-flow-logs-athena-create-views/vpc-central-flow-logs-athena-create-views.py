
import boto3
import os
import datetime
import time
import re

database = os.environ.get('DATABASE')
s3_output = f"s3://{os.environ.get('S3_OUTPUT')}/query_output/"
vpc_table_name = os.environ.get('TABLE_NAME')

# S3 and Athena client
s3 = boto3.client('s3')
athena = boto3.client('athena')

#Executing the athena query:
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
        
        execution_id=query_response['QueryExecutionId']
        state = 'RUNNING'
        while (state in ['RUNNING', 'QUEUED']):
            response = athena.get_query_execution(QueryExecutionId=execution_id)
            if 'QueryExecution' in response and 'Status' in response['QueryExecution'] and 'State' in \
                    response['QueryExecution']['Status']:
                state = response['QueryExecution']['Status']['State']
                if state == 'FAILED':
                    print(response)
                    print("state == FAILED")
                    print('Execution ID: ' + query_response['QueryExecutionId'])
                    return False
                elif state == 'SUCCEEDED':
                    s3_path = response['QueryExecution']['ResultConfiguration']['OutputLocation']
                    filename = re.findall('.*\/(.*)', s3_path)[0]
                    return filename
            time.sleep(1)
    except Exception as e:
        print("Query Exception:- ", e)

    return query_response

#Function to get the regions and run the query on the captured regions
def lambda_handler(event, context):
    errs = None
    status = "SUCCESS"

    if event.get("RequestType") == 'Delete':
        status = "SUCCESS"
        # cfnresponse.send(event, context, status, errs, event["LogicalResourceId"])
        return {
            "status": status
        }
    else:
        try:
            ## Enable below prints for debugging ##
            # print("*" * 10, "START",  "*" * 10) # -- for debug
            summary_query = summary_view_query(vpc_table_name)
            daily_query = daily_view_query(vpc_table_name)
            enh_query = enhanced_view_query(vpc_table_name)
            print(summary_query) # -- for debug
            print(daily_query) # -- for debug
            print(enh_query) # -- for debug
            #print(database) # -- for debug
            #print(s3_output) # -- for debug
            query_result=run_query(summary_query, database, s3_output)
            # print(query_result) # -- for debug
            query_result=run_query(daily_query, database, s3_output)
            # print(query_result) # -- for debug
            query_result=run_query(enh_query, database, s3_output)
            # print(query_result) # -- for debug
            # print("*" * 10, "END",  "*" * 10) # -- for debug
            status = "SUCCESS"
        except Exception as e:
            print("Query Exception:- ", e)
            errs = e
            status = "FAILED"
        finally:
            status = "SUCCESS"
            if event.get("RequestType") != None: 
                # cfnresponse.send(event, context, status, {}, event.get("LogicalResourceId"))
                return {
                    "status": status
                }

def summary_view_query(vpc_table_name):
    query = str("CREATE OR REPLACE VIEW vpc_flow_logs_summary_view AS SELECT"
            + " \"account_id\" \"accountid\" "
            + ", \"interface_id\" \"interfaceid\" "
            + ", \"src_addr\" \"sourceaddress\" "
            + ", \"dst_addr\" \"destinationaddress\" "
            + ", \"src_port\" \"sourceport\" "
            + ", \"dst_port\" \"destinationport\" "
            + ", \"protocol\" \"protocol\" "
            + ", \"sum\"(\"packets\") \"numpackets\" "
            + ", \"sum\"(\"bytes\") \"numbytes\" "
            + ", \"action\" \"action\" "
            + ", \"count\"(\"action\") \"action_count\" "
            + ", \"log_status\" \"logstatus\" "
            + ", \"count\"(\"log_status\") \"log_status_count\" "
            + "FROM " + vpc_table_name
            + " WHERE (((year = format_datetime(current_timestamp, 'YYYY')) AND (month = format_datetime(current_timestamp, 'MM'))) OR ((year = format_datetime((date_trunc('month', current_timestamp) - INTERVAL  '1' MONTH), 'YYYY')) AND (month = format_datetime((date_trunc('month', current_timestamp) - INTERVAL  '1' MONTH), 'MM')))) "
            + "GROUP BY account_id, interface_id, src_addr, dst_addr, src_port, dst_port, protocol, action, log_status;")
    return query
    
def daily_view_query(vpc_table_name):
    query = str("CREATE OR REPLACE VIEW vpc_flow_logs_daily_view AS "
                + "   SELECT "
                + "     \"account_id\" \"accountid\" "
                + "   , \"interface_id\" \"interfaceid\" "
                + "   , \"src_addr\" \"sourceaddress\" "
                + "   , \"dst_addr\" \"destinationaddress\" "
                + "   , \"src_port\" \"sourceport\" "
                + "   , \"dst_port\" \"destinationport\" "
                + "   , \"protocol\" \"protocol\" "
                + "   , \"sum\"(\"packets\") \"numpackets\" "
                + "   , \"sum\"(\"bytes\") \"numbytes\" "
                + "   , \"start\" \"starttime\" "
                + "   , \"end\" \"endtime\" "
                + "   , \"action\" \"action\" "
                + "   , \"count\"(\"action\") \"action_count\" "
                + "   , \"log_status\" \"logstatus\" "
                + "   , CAST(\"date_format\"(\"from_unixtime\"(\"start\"), '%d') AS integer) \"startday\" "
                + "   , CAST(\"date_format\"(\"from_unixtime\"(\"start\"), '%m') AS integer) \"startmonth\" "
                + "   , CAST(\"date_format\"(\"from_unixtime\"(\"end\"), '%d') AS integer) \"endday\" "
                + "   , CAST(\"date_format\"(\"from_unixtime\"(\"end\"), '%m') AS integer) \"endmonth\" "
                + "   FROM " + vpc_table_name
                + " WHERE (((year = format_datetime(current_timestamp, 'YYYY')) AND (month = format_datetime(current_timestamp, 'MM'))) OR ((year = format_datetime((date_trunc('month', current_timestamp) - INTERVAL  '1' MONTH), 'YYYY')) AND (month = format_datetime((date_trunc('month', current_timestamp) - INTERVAL  '1' MONTH), 'MM')))) "
                + "GROUP BY \"account_id\", \"interface_id\", \"src_addr\", \"dst_addr\", \"src_port\", \"dst_port\", \"protocol\", \"start\", \"end\", \"action\", \"log_status\" ORDER BY startmonth ASC, startday ASC;")
    return query
    
def enhanced_view_query(vpc_table_name):
    query =str("CREATE OR REPLACE VIEW vpc_flow_logs_enhanced_view AS "
                    + " SELECT "
                    + "   \"account_id\" \"accountid\" "
                    + " , \"src_addr\" \"sourceaddress\" "
                    + " , \"dst_addr\" \"destinationaddress\" "
                    + " , \"sum\"(\"packets\") \"numpackets\" "
                    + " , \"sum\"(\"bytes\") \"numbytes\" "
                    + " FROM " + vpc_table_name
                    + " WHERE (((((year = format_datetime(current_timestamp, 'YYYY')) AND (month = format_datetime(current_timestamp, 'MM'))) OR ((year = format_datetime((date_trunc('month', current_timestamp) - INTERVAL  '1' MONTH), 'YYYY')) AND (month = format_datetime((date_trunc('month', current_timestamp) - INTERVAL  '1' MONTH), 'MM')))))) "
                    + " GROUP BY \"account_id\", \"src_addr\", \"dst_addr\", \"dst_port\", \"protocol\";")
    return query

