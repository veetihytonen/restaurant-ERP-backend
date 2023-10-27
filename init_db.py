from sqlalchemy import create_engine
from sqlalchemy.sql import text
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DATABASE_URI = getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)

drop_tables = """
DROP TABLE IF EXISTS
    ingredients,
    warehouse_replenishments,
    ingredient_replenishments,
    ingredient_stock_updates,
    users,
    products,
    product_versions,
    product_ingredient_mapping,
    purchases,
    product_sales
CASCADE;
"""

with engine.connect() as conn:
    conn.execute(text(drop_tables))
    conn.commit()

    with open("./schema.sql") as schema:
        queries = schema.read()

    conn.execute(text(queries))
    conn.commit()
