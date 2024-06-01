import argparse
import json
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib import asynccontextmanager
import logging
from confz import FileSource

from src.app.config import APIConfig
from src.app.database.models import *
from src.app.database.database import Base, sessionmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def row_to_dict(row):
    return dict(row._mapping)

async def dump_db_state(session: AsyncSession, file_path: str):
    db_data = {}
    for table in Base.metadata.tables.values():
        table_name = table.name
        result = await session.execute(select(table))
        db_data[table_name] = [row_to_dict(row) for row in result]

    with open(file_path, 'w') as file:
        json.dump(db_data, file, indent=4, default=str)
    logger.info(f"Database state dumped to {file_path}")


async def load_db_state(session: AsyncSession, file_path: str):
    with open(file_path, 'r') as file:
        db_data = json.load(file)

    async with session.begin():
        for table in Base.metadata.sorted_tables:
            table_name = table.name
            if table_name in db_data:
                for row_data in db_data[table_name]:
                    # attempt to convert to datetime objects
                    for k, v in row_data.items():
                        try:
                            row_data[k] = datetime.fromisoformat(v)
                        except Exception:
                            pass
                    await session.execute(table.insert().values(**row_data))

    await session.commit()
    logger.info(f"Database state loaded from {file_path}")


async def main(action: str, file_path: str):
    config = APIConfig(config_sources=FileSource(file='config.yml'))
    sessionmanager.init(config.db.get_connection_string().get_secret_value())
    async with sessionmanager.session() as session:
        if action == 'dump':
            await dump_db_state(session, file_path)
        elif action == 'load':
            await load_db_state(session, file_path)
        else:
            logger.error(f"Unknown action: {action}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Database State Management")
    parser.add_argument('action', choices=['dump', 'load'], help="Action to perform: dump or load the database state")
    parser.add_argument('file_path', help="Path to the file for dumping/loading the database state")

    args = parser.parse_args()

    asyncio.run(main(args.action, args.file_path))
