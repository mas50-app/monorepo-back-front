import asyncio
import asyncpg
from time import time
from bd_con.dsn_reader import get_info_dsn


async def make_pool(dsn):
    pool = await asyncpg.create_pool(dsn)
    return pool


class AsyncPsqlConnection:
    # dsn = 'postgres://{username}:{password}@{host}:{port}/{dbname}'.format(**get_info_dsn())
    dsn = "postgresql://ocasanueva:uf7pDVRc2CCAjwAqKYkC@190.114.255.158:5432/xsolucion"

    def __init__(self, dsn=dsn):
        self.pool = make_pool(dsn)



x = AsyncPsqlConnection()

async def dictfetchall():
    start = time()
    dsn = "postgresql://ocasanueva:uf7pDVRc2CCAjwAqKYkC@190.114.255.158:5432/xsolucion"

    pool = await asyncpg.create_pool(dsn)

    async with pool.acquire() as conn:
        async with conn.transaction():
            rows = await conn.fetch('SELECT * FROM item')

    rows_list = []
    for row in rows:
        row_dict = {}
        for rk in row.keys():
            row_dict[rk] = row[rk]
        rows_list.append(row_dict)
    print(f'It took {time()-start} seconds')
    for row in rows_list:
        await asyncio.sleep(.1)
        print(row)


async def delayer():
    while True:
        print("Im delaying ---------------------------------------------------------------------------------")
        await asyncio.sleep(.2)


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asyncio.gather(dictfetchall(), delayer()))









# class AsyncPsqlConnection:
#
#     def __init__(self):
#         try:
#             conn_info = {
#                 "dbname": "xsolucion",
#                 "user": "ocasanueva",
#                 "password": "uf7pDVRc2CCAjwAqKYkC",
#                 "host": "190.114.255.158",
#                 "port": 5432
#             }
#             self.dsn = 'dbname={dbname} user={user} host={host} password={password} port={port}'.format(**conn_info)
#             # self.dsn = 'dbname={dbname} user={user} host={host} password={password} port={port}'.format(**get_info_dsn())
#             print(self.dsn)
#             self.loop = asyncio.get_event_loop()
#             self.loop.run_until_complete(self.main())
#             self.loop.close()
#             print('exiting program')
#         except Exception as e:
#             raise ConnectionError('dsn.rc not found')
#
#     async def get_data(self, pool):
#         start = time()
#         async with pool.acquire() as conn:
#             async with conn.cursor() as cur:
#                 await cur.execute('SELECT * FROM item')
#                 result = await cur.fetchall()
#         print(f'there are {len(result)} records. Exec time: {time() - start}')
#         return result
#
#     async def main(self):
#         pool = await aiopg.create_pool(self.dsn)
#
#         start = time()
#         tasks = []
#
#         for i in range(3):
#             tasks.append(self.loop.create_task(self.get_data(pool)))
#
#         tasks, stat = await asyncio.wait(tasks)
#
#         for task in tasks:
#             print(f'number of items: {len(task.result())}')
#
#         print(f'total exec time: {time() - start} secs')
#
#         print('exiting main')
#
#
# async_psql_conn = AsyncPsqlConnection()