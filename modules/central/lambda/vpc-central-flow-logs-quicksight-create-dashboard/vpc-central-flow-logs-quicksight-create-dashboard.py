
import boto3
import os

ACCOUNT_ID = os.environ.get('ACCOUNT_ID')
ATHENA_DATASOURCE_ARN = os.environ.get('ATHENA_DATASOURCE_ARN')
DATABASE = os.environ.get('DATABASE')
QUICKSIGHT_USER_ARN = os.environ.get('QUICKSIGHT_USER_ARN')

# Quicksight client
quicksight = boto3.client('quicksight')


def create_summary_dataset():
    print("Creating Summary dataset...")
    response = quicksight.create_data_set(
        AwsAccountId=ACCOUNT_ID,
        DataSetId='vpcflathena-summary-datasetid-01',
        Name='vpc_flow_logs_summary_view',
        PhysicalTableMap={
            'VPCFlowLogsPhysicalTableMap123': {
                'RelationalTable': {
                    'DataSourceArn': ATHENA_DATASOURCE_ARN,
                    'Catalog': 'AwsDataCatalog',
                    'Schema': DATABASE,
                    'Name': 'vpc_flow_logs_summary_view',
                    'InputColumns': [
                        {
                            'Name': 'accountid',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'interfaceid',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'sourceaddress',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'destinationaddress',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'sourceport',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'destinationport',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'protocol',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'numpackets',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'numbytes',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'action',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'action_count',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'logstatus',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'log_status_count',
                            'Type': 'INTEGER'
                        },
                    ]
                },
            }
        },
        LogicalTableMap={
            'VPCFlowLogsLogicalTableMap123': {
                'Alias': 'vpc_flow_logs_summary_view',
                'DataTransforms': [
                    {
                        'ProjectOperation': {
                            'ProjectedColumns': [
                                'accountid',
                                'interfaceid',
                                'sourceaddress',
                                'destinationaddress',
                                'sourceport',
                                'destinationport',
                                'protocol',
                                'numpackets',
                                'numbytes',
                                'action',
                                'action_count',
                                'logstatus',
                                'log_status_count',
                            ]
                        },
                        'TagColumnOperation': {
                            'ColumnName': 'region',
                            'Tags': [
                                {
                                    'ColumnGeographicRole': 'STATE',
                                    'ColumnDescription': {
                                        'Text': 'string'
                                    }
                                },
                            ]
                        },
                    },
                ],
                'Source': {
                    'PhysicalTableId': 'VPCFlowLogsPhysicalTableMap123',
                }
            }
        },
        ImportMode='SPICE',
        Permissions=[
            {
                'Principal': QUICKSIGHT_USER_ARN,
                'Actions': [
                    'quicksight:UpdateDataSetPermissions',
                    'quicksight:DescribeDataSet',
                    'quicksight:DescribeDataSetPermissions',
                    'quicksight:PassDataSet',
                    'quicksight:DescribeIngestion',
                    'quicksight:ListIngestions',
                    'quicksight:UpdateDataSet',
                    'quicksight:DeleteDataSet',
                    'quicksight:CreateIngestion',
                    'quicksight:CancelIngestion',
                ]
            },
        ],
    )
    return response


def create_daily_dataset():
    print("Creating Daily dataset...")
    response = quicksight.create_data_set(
        AwsAccountId=ACCOUNT_ID,
        DataSetId='myathena-daily-datasetid-01',
        Name='vpc_flow_logs_daily_view',
        PhysicalTableMap={
            'VPCFlowLogsPhysicalTableMap123': {
                'RelationalTable': {
                    'DataSourceArn': ATHENA_DATASOURCE_ARN,
                    'Catalog': 'AwsDataCatalog',
                    'Schema': DATABASE,
                    'Name': 'vpc_flow_logs_daily_view',
                    'InputColumns': [
                        {
                            'Name': 'accountid',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'interfaceid',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'sourceaddress',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'destinationaddress',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'sourceport',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'destinationport',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'protocol',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'numpackets',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'numbytes',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'starttime',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'endtime',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'action',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'action_count',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'logstatus',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'startday',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'startmonth',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'endday',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'endmonth',
                            'Type': 'INTEGER'
                        },
                    ]
                },
            }
        },
        LogicalTableMap={
            'VPCFlowLogsLogicalTableMap123': {
                'Alias': 'vpc_flow_logs_daily_view',
                'DataTransforms': [
                    {
                        'ProjectOperation': {
                            'ProjectedColumns': [
                                'accountid',
                                'interfaceid',
                                'sourceaddress',
                                'destinationaddress',
                                'sourceport',
                                'destinationport',
                                'protocol',
                                'numpackets',
                                'numbytes',
                                'starttime',
                                'endtime',
                                'action',
                                'action_count',
                                'logstatus',
                                'startday',
                                'startmonth',
                                'endday',
                                'endmonth',
                            ]
                        },
                        'TagColumnOperation': {
                            'ColumnName': 'region',
                            'Tags': [
                                {
                                    'ColumnGeographicRole': 'STATE',
                                    'ColumnDescription': {
                                        'Text': 'string'
                                    }
                                },
                            ]
                        },
                    },
                ],
                'Source': {
                    'PhysicalTableId': 'VPCFlowLogsPhysicalTableMap123',
                }
            }
        },
        ImportMode='DIRECT_QUERY',
        Permissions=[
            {
                'Principal': QUICKSIGHT_USER_ARN,
                'Actions': [
                    'quicksight:UpdateDataSetPermissions',
                    'quicksight:DescribeDataSet',
                    'quicksight:DescribeDataSetPermissions',
                    'quicksight:PassDataSet',
                    'quicksight:DescribeIngestion',
                    'quicksight:ListIngestions',
                    'quicksight:UpdateDataSet',
                    'quicksight:DeleteDataSet',
                    'quicksight:CreateIngestion',
                    'quicksight:CancelIngestion',
                ]
            },
        ],
    )
    return response


def create_enhanced_dataset():
    print("Creating Enhanced dataset...")
    response = quicksight.create_data_set(
        AwsAccountId=ACCOUNT_ID,
        DataSetId='myathena-enh-datasetid-01',
        Name='vpc_flow_logs_enhanced_view',
        PhysicalTableMap={
            'VPCFlowLogsPhysicalTableMap123': {
                'RelationalTable': {
                    'DataSourceArn': ATHENA_DATASOURCE_ARN,
                    'Catalog': 'AwsDataCatalog',
                    'Schema': DATABASE,
                    'Name': 'vpc_flow_logs_enhanced_view',
                    'InputColumns': [
                        {
                            'Name': 'accountid',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'sourceaddress',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'destinationaddress',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'numpackets',
                            'Type': 'INTEGER'
                        },
                        {
                            'Name': 'numbytes',
                            'Type': 'INTEGER'
                        },
                    ]
                },
            }
        },
        LogicalTableMap={
            'VPCFlowLogsLogicalTableMap123': {
                'Alias': 'vpc_flow_logs_enhanced_view',
                'DataTransforms': [
                    {
                        'ProjectOperation': {
                            'ProjectedColumns': [
                                'accountid',
                                'sourceaddress',
                                'destinationaddress',
                                'numpackets',
                                'numbytes',
                            ]
                        },
                        'TagColumnOperation': {
                            'ColumnName': 'region',
                            'Tags': [
                                {
                                    'ColumnGeographicRole': 'STATE',
                                    'ColumnDescription': {
                                        'Text': 'string'
                                    }
                                },
                            ]
                        },
                    },
                ],
                'Source': {
                    'PhysicalTableId': 'VPCFlowLogsPhysicalTableMap123',
                }
            }
        },
        ImportMode='DIRECT_QUERY',
        Permissions=[
            {
                'Principal': QUICKSIGHT_USER_ARN,
                'Actions': [
                    'quicksight:UpdateDataSetPermissions',
                    'quicksight:DescribeDataSet',
                    'quicksight:DescribeDataSetPermissions',
                    'quicksight:PassDataSet',
                    'quicksight:DescribeIngestion',
                    'quicksight:ListIngestions',
                    'quicksight:UpdateDataSet',
                    'quicksight:DeleteDataSet',
                    'quicksight:CreateIngestion',
                    'quicksight:CancelIngestion',
                ]
            },
        ],
    )
    return response


def create_dashboard(vpc_flow_logs_summary_view_arn, vpc_flow_logs_daily_view_arn, vpc_flow_logs_enhanced_view_arn):
    print("Creating Dashboard...")
    response = quicksight.create_data_set(
        AwsAccountId=ACCOUNT_ID,
        DashboardId="vpc_flow_logs_analysis_dashboard",
        Name="VPC Flow Logs Analysis Dashboard integrated with AWS VPC Service",
        Permissions=[
            {
                'Principal': QUICKSIGHT_USER_ARN,
                'Actions': [
                    'quicksight:DescribeDashboard',
                    'quicksight:ListDashboardVersions',
                    'quicksight:UpdateDashboardPermissions',
                    'quicksight:QueryDashboard',
                    'quicksight:UpdateDashboard',
                    'quicksight:DeleteDashboard',
                    'quicksight:DescribeDashboardPermissions',
                    'quicksight:UpdateDashboardPublishedVersion',
                ]
            },
        ],
        SourceEntity={
            'SourceTemplate':{
                'DataSetReferences':[
                    {
                        'DataSetPlaceholder': 'vpc_flow_logs_summary_view',
                        'DataSetArn': vpc_flow_logs_summary_view_arn
                    },
                    {
                        'DataSetPlaceholder': 'vpc_flow_logs_daily_view',
                        'DataSetArn': vpc_flow_logs_daily_view_arn
                    },
                    {
                        'DataSetPlaceholder': 'vpc_flow_logs_enhanced_view',
                        'DataSetArn': vpc_flow_logs_enhanced_view_arn
                    },
                ],
                'Arn': 'arn:aws:quicksight:us-east-1:869004330191:template/vpc-flow-logs-analysis-enhanced-template-v7'
            }
        },
        VersionDescription='VPC Flow Logs Dashboard reInvent 2022- v7'
    )
    return response

# Function to setup the quicksight dashboard
def lambda_handler(event, context):

    summary_dataset = create_summary_dataset()
    daily_dataset = create_daily_dataset()
    enhanced_dataset = create_enhanced_dataset()

    dashboard_response = create_dashboard(summary_dataset.get("Arn"), daily_dataset.get("Arn"), enhanced_dataset.get("Arn"))
    
    return {
        "response": dashboard_response
    }