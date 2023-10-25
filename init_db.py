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
    products
CASCADE;
"""

ingredients = [('lettuce', 'cold'), ('tomato_diced', 'cold'), ('tortilla', 'dry')]

ingr_sql = text('INSERT INTO ingredients (name, storage_category) VALUES (:name, :strg_ctgr)')

def init_db():
    with engine.connect() as conn:
        conn.execute(text(drop_tables))
        conn.commit()

        with open("./schema.sql") as schema:
            queries = schema.read()

        conn.execute(text(queries))
        conn.commit()

        for ingr in ingredients:
                name = ingr[0]
                strg_ctgr = ingr[1]
                conn.execute(ingr_sql, {'name':name, 'strg_ctgr':strg_ctgr})
        conn.commit()
