resource "aws_quicksight_data_source" "central_flow_logs" {
  data_source_id = "vpc-central-flow-logs"
  name           = "VPCFlowLogsDataset"

  parameters {
    athena {
      work_group = "primary"
    }
  }

  type = "ATHENA"

  ssl_properties {
    disable_ssl = "false"
  }
}