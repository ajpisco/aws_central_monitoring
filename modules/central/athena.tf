resource "aws_athena_database" "central_flow_logs" {
  name   = "vpc_central_flow_logs_db"
  bucket = var.s3_bucket_name
}

resource "aws_glue_catalog_table" "central_flow_logs" {
  name          = "vpc_central_flow_logs_table"
  database_name = aws_athena_database.central_flow_logs.name

  table_type = "EXTERNAL_TABLE"

  partition_keys {
    name = "aws-account-id"
    type = "string"
  }
  partition_keys {
    name = "aws-service"
    type = "string"
  }
  partition_keys {
    name = "aws-region"
    type = "string"
  }
  partition_keys {
    name = "year"
    type = "string"
  }
  partition_keys {
    name = "month"
    type = "string"
  }
  partition_keys {
    name = "day"
    type = "string"
  }

  storage_descriptor {
    location      = "s3://${var.s3_bucket_name}/AWSLogs"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "skip.header.line.count" = "1"
        EXTERNAL : "true"
        "field.delim" : " "
        "serialization.format" : " "
      }
    }

    columns {
      name = "account_id"
      type = "string"
    }
    columns {
      name = "action"
      type = "string"
    }
    columns {
      name = "interface_id"
      type = "string"
    }
    columns {
      name = "src_addr"
      type = "string"
    }
    columns {
      name = "dst_addr"
      type = "string"
    }
    columns {
      name = "src_port"
      type = "int"
    }
    columns {
      name = "dst_port"
      type = "int"
    }
    columns {
      name = "protocol"
      type = "bigint"
    }
    columns {
      name = "packets"
      type = "bigint"
    }
    columns {
      name = "bytes"
      type = "bigint"
    }
    columns {
      name = "start"
      type = "bigint"
    }
    columns {
      name = "end"
      type = "bigint"
    }
    columns {
      name = "latency"
      type = "string"
    }
    columns {
      name = "log_status"
      type = "string"
    }
  }
}