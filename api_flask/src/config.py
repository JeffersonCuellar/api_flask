from dotenv import load_dotenv
import os

load_dotenv()

user = os.environ['ORACLE_USER']
password = os.environ['ORACLE_PASSWORD']
host = os.environ['ORACLE_HOST']
port = os.environ['ORACLE_PORT']
server_name = os.environ['ORACLE_SERVER_NAME']

DATA_CONNECTION_URI = f'oracle+oracledb://{user}:{password}@{host}:{port}/{server_name}'