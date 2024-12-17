from dotenv import load_dotenv
import os

load_dotenv()


#SEFMEC
user = os.environ['ORACLE_USER']
password = os.environ['ORACLE_PASSWORD']
host = os.environ['ORACLE_HOST']
port = os.environ['ORACLE_PORT']
server_name = os.environ['ORACLE_SERVER_NAME']

DATA_CONNECTION_URI = f'oracle+oracledb://{user}:{password}@{host}:{port}/?service_name={server_name}'

#SAC
user2 = os.environ['SAC_USER']
password2 = os.environ['SAC_PASSWORD']
host2 = os.environ['SAC_HOST']
port2 = os.environ['SAC_PORT']
server_name2 = os.environ['SAC_SERVER_NAME']

DATA_CONNECTION_SAC = f'oracle+oracledb://{user2}:{password2}@{host2}:{port2}/?service_name={server_name2}'