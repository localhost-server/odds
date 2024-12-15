import sqlite3
import logging
import csv
import copy
import datetime
from pathlib import Path

def load_max_date(tournament, output_dir):
    filepath = Path(output_dir, f'{tournament}.csv')
    try:
        with open(filepath, 'r') as fs:
            reader = csv.reader(fs)
            data = list(reader)
            fields, values = data[0], data[1:]
            data = {h: v for h, v in zip(fields, zip(*values))}
            result = max(data['date'])
            result = datetime.datetime.strptime(result, '%Y-%m-%d').date()
            return result
    except FileNotFoundError:
        return datetime.date(1970, 1, 1)

class DB():
    def __init__(self, database):
        self.database = database
    def __enter__(self):
        self.con = sqlite3.connect(self.database)
        self.cur = self.con.cursor()
        return self.cur
    def __exit__(self, exc_type, exc_value, exc_trace):
        self.con.commit()
        self.cur.close()
        self.con.close()

def create(tournament, database, columns):
    columns = copy.deepcopy(columns)
    primary_key = columns.pop(0)
    table_name = tournament
    
    with DB(database) as cur:
        cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if not cur.fetchone():
            table_schema = [f"{primary_key} TEXT PRIMARY KEY"]
            table_schema.extend([f"{name}" for name in columns])
            table_schema = ','.join(table_schema)
            logging.info(f"Creating table '{table_name}' with primary key {primary_key} and columns: {columns}")
            cur.execute(f"CREATE TABLE {table_name} ({table_schema})")
        else:
            cur.execute(f"PRAGMA table_info({table_name})")
            table_columns = [info[1] for info in cur.fetchall()]
            new_columns = set(columns) - set(table_columns)
            if new_columns:
                for column in new_columns:
                    cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column}")
                logging.info(f"Updating table '{table_name}' with new columns: {new_columns}")
            else:
                logging.info(f"Schema of table '{table_name}' up to date.")

def export(tournament, output_dir, database, columns):
    table_name = tournament
    filepath = Path(output_dir, f'{tournament}.csv')
    
    with DB(database) as cur:
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
    
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        writer.writerows(rows)


def save(tournament, database, data, columns):
    columns = copy.deepcopy(columns)
    all_columns = columns[:]
    columns.pop(0)
    table_name = tournament
    n_cols = len(columns) + 1
    
    with DB(database) as cur:
        insert_cols = ','.join(all_columns)
        update_cols = ','.join([f'{col}=excluded.{col}' for col in columns])
        insert_into = f"INSERT INTO {table_name} ({insert_cols}) VALUES({','.join(['?'] * n_cols)}) on conflict(id) do update set {update_cols}"
        cur.executemany(insert_into, [data])
