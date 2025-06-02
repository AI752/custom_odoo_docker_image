#!/usr/bin/env python3
import argparse
import logging
import sys
import time
import psycopg2

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def wait_for_postgres(args):
    start_time = time.time()
    while True:
        try:
            conn = psycopg2.connect(
                dbname=args.db_name,
                user=args.db_user,
                password=args.db_password,
                host=args.db_host,
                port=args.db_port
            )
            conn.close()
            logger.info("PostgreSQL is ready!")
            return True
        except psycopg2.OperationalError as e:
            if time.time() - start_time > args.timeout:
                logger.error("Timeout waiting for PostgreSQL")
                return False
            logger.info("PostgreSQL is unavailable - sleeping")
            time.sleep(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_host', default='db')
    parser.add_argument('--db_port', default='5432')
    parser.add_argument('--db_user', default='odoo')
    parser.add_argument('--db_password', default='odoo')
    parser.add_argument('--db_name', default='postgres')
    parser.add_argument('--timeout', type=int, default=30)
    args = parser.parse_args()

    if not wait_for_postgres(args):
        sys.exit(1)

if __name__ == '__main__':
    main() 