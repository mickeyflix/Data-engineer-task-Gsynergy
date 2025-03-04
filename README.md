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



