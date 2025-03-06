# ER Diagram Schema and Documentation

## Task 1:-  Creation of ER Diagram and building the relationship between the schema 

1) Firstly, we unzipped the files of the data folder and we have found that there are data which are divided into two categories Hierarchy tables and Fact tables .
2) In Hierarchy table there are 8 data set hier.invstatus.dlm.gz,hier.hldy.dlm.gz,hier.possite.dlm.gz,hier.invloc.dlm.gz,hier.pricestate.dlm.gz,hier.rtlloc.dlm.gz,hier.prod.dlm.gz, hier.clnd.dlm.gz
3) In the Fact table, there are 2 datasets set fact.averagecosts.dlm.gz, fact.transactions.dlm.gz
4) Fact Tables – Store measurable transactional data.
5) Hierarchy (Dimension) Tables – Contain descriptive attributes for categorization and lookup.
6) After analyzing all the tables, I have come to below points
   * fact_transactions:- Stores details of sales transactions.
   * Foreign Keys:
       * pos_site_id → hier_possite.site_id (Point-of-sale location)
       * ku_id → hier_prod.sku_id (Product details)
       * fscldt_id → hier_clnd.fscldt_id (Date of transaction)
   * Key Attributes: sales_units, sales_dollars, discount_dollars
   * fact_averagecosts:- Tracks average costs for each product per fiscal date.
   * Foreign Keys:
       * fscldt_id → hier_clnd.fscldt_id
       * sku_id → hier_prod.sku_id
  * Key Attributes: average_unit_standardcost, average_unit_landedcost
  * hier_prod :- Organizes products under multiple levels: style, subcategory, category, and department.
  * Primary Key: sku_id
  * Hierarchy: sku_id → stylclr_id → styl_id → subcat_id → cat_id → dept_id
  * hier_possite :- Categorizes sales locations by subchannel and channel.
  * Primary Key: site_id
  * Hierarchy: site_id → subchnl_id → chnl_id
  * hier_clnd :-Defines fiscal calendar hierarchy.
  * Primary Key: fscldt_id
  * Hierarchy: fscldt_id → fsclwk_id → fsclmth_id → fsclqrtr_id → fsclyr_id
  * hier_invstatus:- Tracks inventory status by bucket and ownership.
  * Primary Key: code_id
  * Hierarchy: code_id → bckt_id → ownrshp_id
  * hier_hldy :-Identifies special holidays.
  * Primary Key: hldy_id
  * hier_invloc :- Defines types of inventory locations.
  * Primary Key: loc
  * Hierarchy: loc → loctype
  * hier_pricestate :-Groups pricing under substates and states.
  * Primary Key: substate_id
  * Hierarchy: substate_id → state_id
  * hier_rtlloc :-Organizes retail locations by district and region.
  * Primary Key: str
  * Hierarchy: str → dstr → rgn
7) ER SQL SCHEMA

Table fact_transactions {
  order_id varchar [primary key]
  line_id int [primary key]
  type varchar
  dt datetime
  pos_site_id varchar [ref: > hier_possite.site_id] 
  sku_id varchar [ref: > hier_prod.sku_id] 
  fscldt_id int [ref: > hier_clnd.fscldt_id] 
  price_substate_id varchar
  sales_units int
  sales_dollars decimal
  discount_dollars decimal
  original_order_id varchar
  original_line_id int
}

Table fact_averagecosts {
  fscldt_id int [ref: > hier_clnd.fscldt_id] 
  sku_id varchar [ref: > hier_prod.sku_id] 
  average_unit_standardcost decimal
  average_unit_landedcost decimal
}

Table hier_prod {
  sku_id varchar [primary key]
  sku_label varchar
  stylclr_id varchar
  stylclr_label varchar
  styl_id varchar
  styl_label varchar
  subcat_id varchar
  subcat_label varchar
  cat_id varchar
  cat_label varchar
  dept_id varchar
  dept_label varchar
  issvc boolean
  isasmbly boolean
  isnfs boolean
}

Table hier_possite {
  site_id varchar [primary key]
  site_label varchar
  subchnl_id varchar
  subchnl_label varchar
  chnl_id varchar
  chnl_label varchar
}

Table hier_clnd {
  fscldt_id int [primary key]
  fscldt_label varchar
  fsclwk_id int
  fsclwk_label varchar
  fsclmth_id int
  fsclmth_label varchar
  fsclqrtr_id int
  fsclqrtr_label varchar
  fsclyr_id int
  fsclyr_label varchar
  ssn_id varchar
  ssn_label varchar
  ly_fscldt_id int
  lly_fscldt_id int
  fscldow int
  fscldom int
  fscldoq int
  fscldoy int
  fsclwoy int
  fsclmoy int
  fsclqoy int
  date date
}

Table hier_invstatus {
  code_id varchar [primary key]
  code_label varchar
  bckt_id varchar
  bckt_label varchar
  ownrshp_id varchar
  ownrshp_label varchar
}

Table hier_hldy {
  hldy_id varchar [primary key]
  hldy_label varchar
}

Table hier_invloc {
  loc varchar [primary key]
  loc_label varchar
  loctype varchar
  loctype_label varchar
}

Table hier_pricestate {
  substate_id varchar [primary key]
  substate_label varchar
  state_id varchar
  state_label varchar
}

Table hier_rtlloc {
  str varchar [primary key]
  str_label varchar
  dstr varchar
  dstr_label varchar
  rgn varchar
  rgn_label varchar
}

8) For Creting the ER Digaram we have use the dbdigarm.io editor to generate the diagram.
   
![Untitled](https://github.com/user-attachments/assets/c11c74dc-2135-4b5d-a1cc-59fefc85ba97)


## TASK 2:- Pipeline Building

### Loads this raw data into the data warehouse from external storage such
as Azure Blobs, AWS S3 or the like. You must write basic checks such as
non-null, uniqueness of primary key, data types. Also check for foreign
key constraints between fact and dimension tables. Do it for at least one
hier (dimension), and one fact table.

1) For this loading of the data, we are gonna use AWS S3 for storing the data, AWS Glue for the ETL purpose, and AWS Redshift as our data warehouse
2) So, for this first we create the IAM role and User which has access to AWS S3, AWS Redshift, AWS Glue
3) For redshift purpose IAM role we created the IAM role with the name of redshift s3 access which has the access of all functionality for AWS S3, AWS Redshift, AWS Glue
4) Same for AWS Glue as well we did the same
5) Now we load our data in S3 bucket. We are taking two dataset one is fact_transcation and other is hier_prod
6) After loading the data in AWS S3 we will now start with the creation of Glue job where we start our loading part
7) I have attached the python script in GitHub with the name of glue-synergy.py
8) On this glue job I am loading the S3 data and then doing the transformation like handling null values and removing duplicates
9) Before running the Job we have to create the Redshift cluster as well with the correct config  and IAM
10) After setting up the Redshift cluster connection we can add those config in our glue job and run those job that will load those table in redshift.
11) Please see the below image for more info.
12) ![image](https://github.com/user-attachments/assets/35c719e2-d19e-4779-b603-ecbc85bfe8ae)

### Create a staging schema where the hierarchy table has been normalized
into a table for each level and the staged fact table has foreign key
relationships with those tables.

1) For the above query, I am going to attach the SQL query of creating the staging schema and normalizing the table into different foreign key
2) It is with the name of staging.sql
3) you can refer the below image
   ![image](https://github.com/user-attachments/assets/6d53f939-3144-40ea-a88b-9a8086fcc08e)


### Create a refined table called mview_weekly_sales which totals sales_units,
sales_dollars, and discount_dollars by pos_site_id, sku_id, fsclwk_id,
price_substate_id and type.

1) Same for this one, I'm going to attach the SQL query of creating the mview_weekly_sales
2) it is the name of weekly.sql
3) You can refer to the below image
   ![image](https://github.com/user-attachments/assets/1d5fbdaf-5240-48de-ae6b-625f18f228a1)

### BONUS: write transformation logic that will incrementally calculate all the
totals in the above table for partially loaded data.
1) For this, we have created one more glue job that incrementally calculates all the totals in the above table or partially loaded data. \
2) It is with the name of incremental.py
3) First, we have to create a new table with the name of staging.fact_transactions_delta, which is used to fetch new data from Redshift used for incremental refresh
4) CREATE TABLE staging.fact_transactions_delta AS 
SELECT * FROM public.fact_transactions WHERE fscldt_id = (SELECT MAX(fscldt_id) FROM public.fact_transactions);
5) After applying the above query, we will create our incremental glue job.


   






