
qOrders = """\
SELECT TOP (50000) [Document Type]
      ,[Document No_]
      ,[Version No_]
      ,[Line No_]
      ,[Sell-to Customer No_]
      ,[SellCustName]
      ,[Bill-to Customer No_]
      ,[BillCustName]
      ,[No_]
      ,[ItemGrp]
      ,[Type]
      ,[Location Code]
      ,[Description]
      ,[Quantity]
      ,[Unit of Measure]
      ,[Order Date]
      ,[Posting Date]
      ,[Shipment Date]
      ,[Document Date]
      ,[External Document No_]
  FROM [EMCO].[dbo].[XXX-SalesArchive1] ORDER BY [Document No_] COLLATE SQL_Latin1_General_CP1_CI_AI
"""

cnameOrders = [
  "Document-Type"
      ,"Document-No_"
      ,"Version-No_"
      ,"Line-No_"
      ,"Sell-to-Customer-No_"
      ,"Sell-Cust-Name"
      ,"Bill-to-Customer-No_"
      ,"Bill-Cust-Name"
      ,"No_"
      ,"Item-Grp"
      ,"Type"
      ,"Location-Code"
      ,"Description"
      ,"Quantity"
      ,"Unit-of-Measure"
      ,"Order-Date"
      ,"Posting-Date"
      ,"Shipment-Date"
      ,"Document-Date"
      ,"External-Document-No_"
]

cCONN=b'VlM0X1NRTFxFUlB8RU1DT1xCcmVkYS5NYXJjZWx8Q2hhb3RpcS4xOTcwfEVNQ08='
