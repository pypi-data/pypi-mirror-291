import os
import yaml
import pymysql
from pathlib import Path
from dbutils.pooled_db import PooledDB
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def load_config(config):
    """
    Load the database configuration from a YAML file.
    Args: project dir path
    Returns:
        dict: Database configuration for the development environment.
    """
    config_file = os.path.join(config,'config', 'database.yml')
    
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config['development']

def create_database_if_not_exists(connection, database_name):
    """
    Create the database if it does not already exist.
    
    Args:
        connection (pymysql.connections.Connection): Connection to the MySQL server.
        database_name (str): Name of the database to create.
    """
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    logging.info(f"Database '{database_name}' created or already exists.")
    cursor.close()

def initialize_database(config):
    """
    Initialize the database connection pool.
    
    Args:
        config (dict): Database configuration.
    
    Returns:
        PooledDB: Database connection pool.
    """
    pool = PooledDB(
        creator=pymysql,
        host=config['host'],
        port=config['port'],
        user=config['username'],
        password=config['password'],
        database=config['database'],
        autocommit=config['autocommit'],
        blocking=config['blocking'],
        maxconnections=config['maxconnections'],
    )
    logging.info(f"Database connection pool created for '{config['database']}'.")
    return pool

def execute_sql_file(connection, file_path):
    """
    Execute a SQL file on the database.
    
    Args:
        connection (pymysql.connections.Connection): Connection to the database.
        file_path (str): Path to the SQL file.
    """
    cursor = connection.cursor()
    with open(file_path, 'r') as file:
        queries = file.read().split(';\n')
        for query in queries:
            if query.strip():
                cursor.execute(query)
    connection.commit()
    cursor.close()
    logging.info(f"Executed SQL file: {file_path}")

def setup_database(config_dir):
    """
    Args project dir path
    Setup the database by creating the database, initializing the connection pool, 
    and executing the schema and seed SQL files.
    """
    logging.info("Loading configuration...")
    
    config = load_config(config_dir)
    
    logging.info("Connecting to MySQL server...")
    temp_connection = pymysql.connect(
        host=config['host'],
        user=config['username'],
        password=config['password'],
        port=config['port'],
    )
    
    logging.info("Creating database if not exists...")
    create_database_if_not_exists(temp_connection, config['database'])
    temp_connection.close()
    
    logging.info("Initializing database connection pool...")
    pool = initialize_database(config)
    connection = pool.connection()
    
    logging.info("Executing schema SQL file...")
    schema_file_path = os.path.join(config_dir, 'config', 'schema.sql')
    execute_sql_file(connection, schema_file_path)
    
    logging.info("Executing seed SQL file...")
    seed_file_path = os.path.join(config_dir, 'config', 'seed.sql')
    execute_sql_file(connection, seed_file_path)
    
    connection.close()
    logging.info("Database setup completed successfully.")