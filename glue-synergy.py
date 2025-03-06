import sys
import boto3
import gzip
import io
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize AWS Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# S3 Config
S3_BUCKET = "gsynergybucket"
S3_PREFIX = "data-folder/"
RAW_FILES = ["fact.transactions.dlm.gz", "hier.prod.dlm.gz"]

# Redshift Config (JDBC Format)
REDSHIFT_URL = "jdbc:redshift://my-redshift-cluster.carybst9wvr2.ap-south-1.redshift.amazonaws.com:5432/dev"
REDSHIFT_USER = "sam"
REDSHIFT_PASSWORD = "hiphopsm47A"
REDSHIFT_TABLE_FACT = "public.fact_transactions"
REDSHIFT_TABLE_HIER = "public.hier_prod"
IAM_ROLE = "arn:aws:iam::095342733939:role/redshifts3access"
temp_dir = "s3://my-glue-bucket-gsynergy/tmp/"

# Load from S3
def load_s3_to_df(file_name):
    s3_path = f"s3://{S3_BUCKET}/{S3_PREFIX}{file_name}"
    df = spark.read.option("delimiter", "|").csv(s3_path, header=True, inferSchema=True)
    return df

# Read data from S3
fact_transactions_df = load_s3_to_df("fact.transactions.dlm.gz")
hier_prod_df = load_s3_to_df("hier.prod.dlm.gz")

# Handle Missing Values
fact_transactions_df = fact_transactions_df.fillna({"original_order_id": 0, "original_line_id": 0})
hier_prod_df = hier_prod_df.dropna()

# Remove Duplicates
fact_transactions_df = fact_transactions_df.dropDuplicates(["order_id", "line_id"])
hier_prod_df = hier_prod_df.dropDuplicates(["sku_id"])

# Convert to Glue DynamicFrame
fact_transactions_dyf = DynamicFrame.fromDF(fact_transactions_df, glueContext, "fact_transactions")
hier_prod_dyf = DynamicFrame.fromDF(hier_prod_df, glueContext, "hier_prod")

# Write to Redshift using JDBC
datasink_fact = glueContext.write_dynamic_frame.from_options(
    frame=fact_transactions_dyf,
    connection_type="redshift",
    connection_options={
        "url": REDSHIFT_URL,
        "dbtable": REDSHIFT_TABLE_FACT,
        "user": REDSHIFT_USER,
        "password": REDSHIFT_PASSWORD,
        "aws_iam_role": IAM_ROLE,
        "redshiftTmpDir": temp_dir
    }
 )

datasink_hier = glueContext.write_dynamic_frame.from_options(
    frame=hier_prod_dyf,
    connection_type="redshift",
    connection_options={
        "url": REDSHIFT_URL,
        "dbtable": REDSHIFT_TABLE_HIER,
        "user": REDSHIFT_USER,
        "password": REDSHIFT_PASSWORD,
        "aws_iam_role": IAM_ROLE,
        "redshiftTmpDir": temp_dir
  }
)

print("Data successfully loaded into AWS Redshift!")






