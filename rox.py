import ingest
from ingest.transform import commaToPoint, nulls, nullToZero, trim
import boto3

# -----------------------------------------------------------
# ------------------        CONFIG         ------------------
# Change bucket and bucket dir to point to your S3 environment.
# Use localdir to temporary folder where S3 downloaded csv files
# are stored.
# -----------------------------------------------------------
localdir = "/tmp"
bucket = "francara-rox"
bucketdir = "script/spec"


# -----------------------------------------------
# ------------   S3 util functions   ------------
# -----------------------------------------------

def s3_download(csvFile, s3bucket=bucket, s3dir=bucketdir, downloaddir=localdir):
    """Download csvFile located at s3bucket in the s3dir path."""
    s3cli = boto3.client('s3')
    with open(f'{downloaddir}/{csvFile}', 'wb') as file:
        s3cli.download_fileobj(s3bucket, f'{s3dir}/{csvFile}', file)

def s3_upload(s3Dir, csvFile, s3bucket=bucket, downloaddir=localdir):
    """Upload csvFile located at downloaddir to s3dir path."""
    s3 = boto3.resource('s3')
    s3.Object(s3bucket, f'{s3Dir}/{csvFile}').put(Body=open(f'{downloaddir}/{csvFile}', 'rb'))

def gen_s3_upload(s3Dir):
    """Generates a curry function which calls s3_upload with s3dir already set."""
    def call_s3_upload(csvFile):
        s3_upload(s3Dir, csvFile)
    return call_s3_upload

# -----------------------------------------------------
# ------------         MAIN script         ------------
# -----------------------------------------------------

#
# Injestão de arquivos da especificação.
#

# Product ingestion.
s3_download("Production.Product.csv")
ingest.process(localdir, 'Production.Product.csv',
               # Transformations of specific fields.
               transforms={"StandardCost": [commaToPoint, nullToZero], "ListPrice": [commaToPoint, nullToZero],
                    "Weight": [commaToPoint, nullToZero], "SafetyStockLevel": [nullToZero],
                    "ReorderPoint": [nullToZero], "DaysToManufacture": [nullToZero], "ProductSubcategoryID": [nullToZero],
                    "ProductModelID": [nullToZero]},
               # Transformations applied to all fields.
               alltransforms=[nulls, trim],
               writefile=True,
               # Callback to upload the converted file
               uploadS3=gen_s3_upload("product"))

# Person.Person ingestion.
s3_download("Person.Person.csv", downloaddir=localdir)
ingest.process(localdir, 'Person.Person.csv',
               # Transformations applied to all fields.
               alltransforms=[nulls, trim],
               writefile=True,
               # Callback to upload the converted file
               uploadS3=gen_s3_upload("person"))

# SalesOrderHeader ingestion.
s3_download("Sales.Customer.csv", downloaddir=localdir)
ingest.process(localdir, 'Sales.Customer.csv',
               # Transformations of specific fields.
               transforms={"PersonID": [nullToZero], "StoreID":[nullToZero], "TerritoryID": [nullToZero]},
               # Transformations applied to all fields.
               alltransforms=[nulls, trim],
               writefile=True,
               # Callback to upload the converted file
               uploadS3=gen_s3_upload("customer"))

# SalesOrderHeader ingestion.
s3_download("Sales.SalesOrderHeader.csv", downloaddir=localdir)
ingest.process(localdir, 'Sales.SalesOrderHeader.csv',
               # Transformations of specific fields.
               transforms={"SalesPersonID":[nullToZero], "TerritoryID":[nullToZero], "BillToAddressID":[nullToZero], "ShipToAddressID":[nullToZero], "ShipMethodID":[nullToZero], "CreditCardID":[nullToZero], "CurrencyRateID": [nullToZero], "SubTotal":[commaToPoint], "TaxAmt":[commaToPoint], "Freight":[commaToPoint], "TotalDue":[commaToPoint]},
               # Transformations applied to all fields.
               alltransforms=[nulls, trim],
               writefile=True,
               # Callback to upload the converted file
               uploadS3=gen_s3_upload("sales/order"))

# Sales.SalesOrderDetail ingestion.
s3_download("Sales.SalesOrderDetail.csv", downloaddir=localdir)
ingest.process(localdir, 'Sales.SalesOrderDetail.csv',
               # Transformations of specific fields.
               transforms={"OrderQty":[nullToZero, commaToPoint], "SpecialOfferID":[nullToZero], "UnitPrice":[nullToZero, commaToPoint], "UnitPriceDiscount":[nullToZero, commaToPoint], "LineTotal":[nullToZero, commaToPoint]},
               # Transformations applied to all fields.
               alltransforms=[nulls, trim],
               writefile=True,
               # Callback to upload the converted file
               uploadS3=gen_s3_upload("sales/detail"))

# Sales.SpecialOfferProduct ingestion.
s3_download("Sales.SpecialOfferProduct.csv", downloaddir=localdir)
ingest.process(localdir, 'Sales.SpecialOfferProduct.csv',
               # Transformations of specific fields.
               transforms={"ProductID": [nullToZero]},
               # Transformations applied to all fields.
               alltransforms=[nulls, trim],
               writefile=True,
               # Callback to upload the converted file
               uploadS3=gen_s3_upload("sales/offer"))
