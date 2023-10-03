from sqlalchemy import create_engine
from sqlalchemy.sql import text
from config import DATABASE_URI

engine = create_engine(DATABASE_URI)

def init_db() -> None:
    with engine.connect() as conn:
        dt = open("./drop_db.sql")
        drop_tables = text(dt.read())
        dt.close()
        conn.execute(drop_tables)
        conn.commit()

        schema = open("./schema.sql")
        queries = text(schema.read())
        schema.close()
        conn.execute(queries)
        conn.commit()

        ingredients = [('lettuce', 'cold'), ('tomato_diced', 'cold'), ('tortilla', 'dry')]

        ingr_sql = text('INSERT INTO ingredients (name, storage_category) VALUES (:name, :strg_ctgr)')

        for ingr in ingredients:
            name = ingr[0]
            strg_ctgr = ingr[1]
            conn.execute(ingr_sql, {'name':name, 'strg_ctgr':strg_ctgr})
        conn.commit()
