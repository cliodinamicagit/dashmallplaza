import io, sys
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

user='dbmasteruser'
passwd='am5qtGJG)f]26wk?6c_)*Ws-<+_MdPYg'
endpoint='ls-eec11c06948e04c0ccde52508591c35b937cc89f.cxuluyjslj42.us-east-1.rds.amazonaws.com'

connection = psycopg2.connect(user = user, password = passwd,
                                  host = endpoint,
                                  port = "5432",
                                  database = "postgres")

cursor=connection.cursor()

eng_url = f'postgresql+psycopg2://{user}:{passwd}@{endpoint}:5432/postgres'
print(eng_url)

engine=create_engine(eng_url)
conn=engine.raw_connection()
cur=conn.cursor()

#op=io.StringIO()

def upload(filename, tablename):

    #if filename.endswith('.csv'):   # Franklin: construir conector XLSX, stata...

    df = pd.read_csv(filename, encoding='latin-1', delimiter=';', chunksize=10)
    #df1 = pd.read_stata(filename, encoding='latin-1', delimiter=';')

    #df=pd.read_html('http://quant.cl/blc_read')[0]
    #df.to_csv(op, sep='\t',header=False,index=False)
    #op.seek(0)
    #contents=op.getvalue()
    df.to_sql(tablename, con=engine, if_exists='replace')
    #cur.copy_from(op, tablename, null="")
    conn.commit()

clio_aws_S3 = 'https://cliodina.s3.us-east-2.amazonaws.com/'

url_s3 = clio_aws_S3 + '002_casen/Colombia/col15n.dta'
url = 'data/chl/etl_geo_datos_all.csv'

name='col_casen_2015.csv'
upload(url_s3, name)