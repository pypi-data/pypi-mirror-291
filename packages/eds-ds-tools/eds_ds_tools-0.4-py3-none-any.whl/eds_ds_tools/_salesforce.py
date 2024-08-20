__all__ = ['sf_query']

from ._imports import *
from ._config import config
#from ._cyberark import get_credential_both_method

class sf:

    conn = None

    @classmethod
    def query(cls, q):
        if cls.conn is None:
            # user, password = get_credential_both_method('salesforce')
            cls.conn = psycopg2.connect(
                dbname      =  config['salesforce']['dbname'],  
                user        = config['salesforce']['user'],
                password    = config['salesforce']['password'],               
                host        = config['salesforce']['host'], 
                port        = 5432,
                sslmode     = 'require',
                sslrootcert = config['salesforce']['sslrootcert'],
                sslcert     = config['salesforce']['sslcert'],
                sslkey      = config['salesforce']['sslkey'],            
            )
        return pd.read_sql(q, cls.conn)

def sf_query(q):
    return sf.query(q)

@atexit.register
def sf_close():
    if sf.conn:        
        sf.conn.close()