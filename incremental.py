import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import pyspark.sql.functions as F

# Initialize Glue Job
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# 🔹 Redshift Connection Details
REDSHIFT_URL = "jdbc:redshift://my-redshift-cluster.carybst9wvr2.ap-south-1.redshift.amazonaws.com:5432/dev"
REDSHIFT_USER = "sam"
REDSHIFT_PASSWORD = "hiphopsm47A"
REDSHIFT_TABLE_FACT = "public.fact_transactions"
REDSHIFT_TABLE_HIER = "public.hier_prod"
IAM_ROLE = "arn:aws:iam::095342733939:role/redshifts3access"
temp_dir = "s3://my-glue-bucket-gsynergy/tmp/"

# 🔹 Read New Fact Data from Redshift (Incremental Data)
fact_df = glueContext.read.format("jdbc").option("url", REDSHIFT_URL)\
    .option("dbtable", "staging.fact_transactions_delta")\
    .option("user", REDSHIFT_USER)\
    .option("password", REDSHIFT_PASSWORD)\
    .option("tempdir", temp_dir)\
    .option("driver", "com.amazon.redshift.jdbc.Driver")\
    .load()

# 🔹 Aggregate to Match `mview_weekly_sales`
fact_agg_df = fact_df.groupBy("pos_site_id", "sku_id", "fscldt_id", "price_substate_id", "type")\
    .agg(
        F.sum("sales_units").alias("total_sales_units"),
        F.sum("sales_dollars").alias("total_sales_dollars"),
        F.sum("discount_dollars").alias("total_discount_dollars")
    )

# 🔹 Merge into `mview_weekly_sales`
fact_agg_df.write \
    .format("jdbc") \
    .option("url", REDSHIFT_URL) \
    .option("dbtable", "mview_weekly_sales") \
    .option("user", REDSHIFT_USER) \
    .option("password", REDSHIFT_PASSWORD) \
    .option("tempdir", temp_dir) \
    .option("driver", "com.amazon.redshift.jdbc.Driver") \
    .mode("append") \
    .save()

print("Incremental transformation completed successfully!")
job.commit()
