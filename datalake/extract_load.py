import duckdb
import os
import dotenv
import httpx
from loguru import logger

dotenv.load_dotenv()


def get_settings():
    settings = {}
    settings['r2_bucket_name'] = os.getenv('OSSCI_R2_BUCKET_NAME')
    settings['r2_bucket_key'] = os.getenv('OSSCI_R2_BUCKET_KEY')
    settings['r2_bucket_secret'] = os.getenv('OSSCI_R2_BUCKET_SECRET')
    settings['r2_account_id'] = os.getenv('OSSCI_R2_ACCOUNT_ID')
    settings['r2_base_directory'] = os.getenv('OSSCI_R2_BASE_DIRECTORY','raw')
    return settings

def get_duckdb_connection():
    conn = duckdb.connect(database=':memory:')
    settings = get_settings()
    sql = f"""
    install httpfs;
    load httpfs;
    create or replace secret r2 (
        type r2,
        key_id '{settings['r2_bucket_key']}',
        secret '{settings['r2_bucket_secret']}',
        account_id '{settings['r2_account_id']}'
    )
    """
    conn.execute(sql)
    return conn

def extract_and_load_cord_dataset(conn):
    settings = get_settings()
    sql = f"""copy (
    select * 
    from 
    read_csv_auto('https://zenodo.org/records/4582776/files/CORD19_software_mentions.csv?download=1')
) to 
'r2://{settings['r2_bucket_name']}/{settings['r2_base_directory']}/czi/cord19_software_mentions.parquet' (format parquet, compression zstd);
    """
    conn.execute(sql)

def extract_and_load_softcite_v2(conn):
    settings = get_settings()
    sql = f"""
    copy (
        select unnest(documents, recursive:=true)
    from 
        read_json('https://raw.githubusercontent.com/softcite/softcite_dataset_v2/refs/heads/master/json/softcite_corpus-full.json')
    ) to
    'r2://{settings['r2_bucket_name']}/{settings['r2_base_directory']}/softcite_v2/softcite_corpus-full.parquet' (format parquet, compression zstd);
    """
    conn.execute(sql)
    
    
if __name__ == "__main__":
    conn = get_duckdb_connection()
    extract_and_load_cord_dataset(conn)
    extract_and_load_softcite_v2(conn)
    conn.close()