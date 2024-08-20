from datetime import datetime
import os
from pprint import pprint
from sqlalchemy import BigInteger, Column, DateTime, Engine, Integer, String, Table, Text, create_engine, insert, select, text
from sqlalchemy.orm import Mapped, mapped_column, Session

from doris_alchemy.datatype import HASH, RANGE
from doris_alchemy.datatype import RANDOM
from doris_alchemy.orm_base import METADATA, DorisBase

USER = os.environ['DORIS_PROD_USER']
PWD = os.environ['DORIS_PROD_PWD']
HOST = '10.0.100.115'
PORT = '9030'
DB = 'test'

def make_eng() -> Engine:
    return create_engine(f"doris+mysqldb://{USER}:{PWD}@{HOST}:{PORT}/{DB}")


table = Table(
    'dummy_table',
    METADATA,
    Column('id', Integer),
    Column('name', String(64), nullable=False),
    Column('description', Text),
    Column('date', DateTime),
    
    # doris_unique_key=('id'),
    doris_partition_by=RANGE('id'),
    # doris_distributed_by=HASH('id'),
    doris_distributed_by = RANDOM(32),
    doris_properties={"replication_allocation": "tag.location.default: 1"},
    doris_autogen_primary_key=True
)


class Dummy(DorisBase):
    __tablename__ = 'dummy_two'
    
    id:             Mapped[int] = mapped_column(Integer, primary_key=True)
    name:           Mapped[str] = mapped_column(String(127))
    description:    Mapped[str]
    date:           Mapped[datetime]
    
    __table_args__ = {
        'doris_properties': {"replication_allocation": "tag.location.default: 1"},
        'comment': "Some table comment"
        }
    # doris_unique_key = 'id'
    # doris_distributed_by = HASH('id')
    # doris_distributed_by = RANDOM(32)
    # doris_partition_by = RANGE('id', ('PARTITION p1 VALUES LESS THAN ("1000")'))
    doris_autogen_primary_key = True


ROWS = [
    ('BMW', 'A car brand', datetime(2024, 1, 1)),
    ('Airbus', 'Construction bureau', datetime(2024, 2, 10)),
    ('Volvo', 'A car brand', datetime(2022, 12, 1, 10, 35))
]

def __mk_row(id :int, row: tuple[str, str, datetime]):
    return {
        'id': id,
        'name': row[0],
        'description': row[1],
        'date': row[2]
    }

if __name__ == '__main__':
    engine = make_eng()
    try:
        Dummy.drop(engine)
    except:
        print("Doesn't exist")
    Dummy.create(engine)
    # with Session(engine) as s:
    #     # print(engine.dialect.has_table(s.connection(), 'dummy_two'))
    #     vals = [__mk_row(i, ROWS[i]) for i in range(len(ROWS))]
    #     q = insert(Dummy)
    #     s.execute(q, vals)
    #     # s.execute(q)
    #     sel = select(Dummy)
    #     res = s.execute(sel)
    #     pprint(list(res))
    pass