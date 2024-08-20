from datetime import datetime
import mariadb
import pandas as pd
from tqsdk import TqApi, TqAuth
import pymysql
import logging
import asyncio

# 数据库配置
local_db_ip = 'st'
local_db_user = 'ot'
local_db_passwd = 'T'
local_db_db = 'data'
local_db_table_15 = 'ag_15s'
local_db_table_60 = 'ag_60s'
local_db_port = 3306

cloud_db_ip = '39.105.149.40'
cloud_db_user = 'root'
cloud_db_passwd = 'Jy02160960'
cloud_db_db = 'bl'
cloud_db_table = 'ag'
cloud_db_table_60 = 'ag_60s'
cloud_db_port = 3306

# 初始化API
api = TqApi(auth=TqAuth("billin", "dnadna"))
klines_15s = api.get_kline_serial("KQ.i@SHFE.ag", 60,10000)
klines_60s = api.get_kline_serial("KQ.i@SHFE.ag", 60)

# 日志配置
logger = logging.getLogger("ag_60s")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
fh = logging.FileHandler("ag_60s.log")
fh.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%a %d %b %Y %H:%M:%S")
ch.setFormatter(fmt)
fh.setFormatter(fmt)
logger.addHandler(ch)
logger.addHandler(fh)

# 数据库连接函数
def conn_mysql(host, user, password, database, port=3306):
    try:
        conn = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
        return conn
    except Exception as e:
        logger.error(f"Can not connect to mysql {host}: {e}")

async def save_to_sql(df, host, user, password, db, table, port):
    
        connection = mariadb.connect(user="Jwz", password="Jwz0711~", host="1.92.70.241", port=3306, database="tiger_db")
        print(connection)
        cursor = connection.cursor()
       
        length=len(df)
        
        
        """
        values = list(df[["datetime", "close", "Ratio1", "Ratio"]].itertuples(index=False, name=None))
        
        items=values[len(values)-1]
        print("items:",items)
        """
        
        # insql=f"insert into {table} (datetime, close, Ratio1, Ratio) values('{items[0]}',{items[1]},{items[2]},{items[3]}) ON DUPLICATE KEY UPDATE datetime='{items[0]}';"
        # insql=f"insert into {table} (datetime, close, Ratio1, Ratio) values('{items[0]}',{items[1]},{items[2]},{items[3]}) ON DUPLICATE KEY UPDATE close='{items[1]}', Ratio1='{items[2]}', Ratio='{items[3]}';"
        
        
        #insql = f"INSERT INTO {table} (datetime, close, Ratio1, Ratio) VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE close = VALUES(close),Ratio1 = VALUES(Ratio1),Ratio = VALUES(Ratio)"
        insql = f"insert into {table} (datetime, close, Ratio1, Ratio) VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE close = VALUES(close),Ratio1 = VALUES(Ratio1),Ratio = VALUES(Ratio)"

        print(insql)
        values = list(df[["datetime_str", "close", "Ratio1", "Ratio"]].itertuples(index=False, name=None))
        #values = list(df[["datetime_str", "close", "Ratio1", "Ratio"]].itertuples(index=False, name=None))
        #print(values)
        #items=values[len(values)-1]
        #print("items:",items)
        #print(items[0])
        cursor.executemany(insql, values)
        connection.commit()


        
        #cursor.execute(insql)
        #connection.commit()
        

        connection.close()


async def save_to_sql60(df, host, user, password, db, table, port):
    
        connection = mariadb.connect(user="Jwz", password="Jwz0711~", host="1.92.70.241", port=3306, database="tiger_db")
        print(connection)
        cursor = connection.cursor()
       
        length=len(df)
        
        
        values = list(df[["datetime", "close", "Ratio3", "Ratio4"]].itertuples(index=False, name=None))
        
        items=values[len(values)-1]
        print("items:",items)
        
        
        #insql=f"insert into {table} (datetime, close, Ratio3, Ratio4) values('{items[0]}',{items[1]},{items[2]},{items[3]}) ON DUPLICATE KEY UPDATE datetime='{items[0]}';"
        
        #print(insql)
        #cursor.execute(insql)
        #connection.commit()

        insql = f"insert into {table} (datetime, close, Ratio3, Ratio4) VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE close = VALUES(close),Ratio3 = VALUES(Ratio3),Ratio4 = VALUES(Ratio4)"

        print(insql)
        values = list(df[["datetime_str", "close", "Ratio3", "Ratio4"]].itertuples(index=False, name=None))
        #print(values)
        #items=values[len(values)-1]
        #print("items:",items)
        #print(items[0])
        cursor.executemany(insql, values)
        connection.commit()

        
        connection.close()

    
while False:
    api.wait_update()
    if api.is_changing(klines_15s):
        df_1 = pd.DataFrame(klines_15s, columns=['id', 'datetime', 'open', 'high', 'low', 'close', 'volume'])
        df_1['datetime'] = df_1['datetime'].apply(lambda x: datetime.fromtimestamp(x / 1e9))
        #df_1['datetime'] = pd.to_datetime(df_1['datetime'],unit="s")
        #df_1['datetime'] = pd.to_datetime(df_1['datetime'])
        df_1['datetime_str'] = df_1['datetime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        
        df_1['change'] = df_1['close'] - df_1['close'].shift(1)
        df_1.dropna(subset=['change'], inplace=True)
        df_1['Ratio1'] = df_1['close'].ewm(alpha=0.3313, adjust=False).mean()
        df_1['Ratio'] = df_1['close'].ewm(alpha=0.2257, adjust=False).mean()
        df_1 = df_1.iloc[20:]
        #print(df_1)

        # 保存数据到数据库
        asyncio.run(save_to_sql15(df_1, cloud_db_ip, cloud_db_user, cloud_db_passwd, cloud_db_db, cloud_db_table_15, cloud_db_port))
        print("15S数据保存数据库成功")

    

    
    if api.is_changing(klines_60s):
        df_2 = pd.DataFrame(klines_60s, columns=['id', 'datetime', 'open', 'high', 'low', 'close', 'volume'])
        df_2['datetime'] = df_2['datetime'].apply(lambda x: datetime.fromtimestamp(x / 1e9))
        df_2['datetime_str'] = df_2['datetime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        df_2['change'] = df_2['close'] - df_2['close'].shift(1)
        df_2.dropna(subset=['change'], inplace=True)
        df_2['Ratio3'] = df_2['close'].ewm(alpha=0.3313, adjust=False).mean()
        df_2['Ratio4'] = df_2['close'].ewm(alpha=0.2257, adjust=False).mean()
        df_2 = df_2.iloc[20:]

        asyncio.run(save_to_sql60(df_2, cloud_db_ip, cloud_db_user, cloud_db_passwd, cloud_db_db, cloud_db_table_60, cloud_db_port))
        print("60S数据保存数据库成功")

    


#盘后测试代码
if api.is_changing(klines_15s):
    print("klines got!!!")
    # 将klines转换为DataFrame
    df_1 = pd.DataFrame(klines_15s, columns=['id', 'datetime', 'open', 'high', 'low', 'close', 'volume'])
    df_1['datetime'] = df_1['datetime'].apply(lambda x: datetime.fromtimestamp(x / 1e9))
    df_1['datetime_str'] = df_1['datetime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

    """
    df_1['change'] = df_1['close'] - df_1['close'].shift(1)
    df_1.dropna(subset=['change'], inplace=True)
    df_1['Ratio1'] = df_1['close'].ewm(alpha=0.3313, adjust=False).mean()
    df_1['Ratio'] = df_1['close'].ewm(alpha=0.2257, adjust=False).mean()
    df_1 = df_1.iloc[20:]
    """
    print(df_1)
    print(len(df_1))

    # 保存数据到数据库
    #await asyncio.gather(
        #save_to_mysql(df_1, local_db_ip, local_db_user, local_db_passwd, local_db_db, local_db_table_15, local_db_port),
    
    #)
    #asyncio.run(save_to_mysql(df_1, cloud_db_ip, cloud_db_user, cloud_db_passwd, cloud_db_db, cloud_db_table_15, cloud_db_port))
    #asyncio.run(save_to_sql(df_1, cloud_db_ip, cloud_db_user, cloud_db_passwd, cloud_db_db, cloud_db_table, cloud_db_port))




"""
    connection2 = mariadb.connect(user="Jwz", password="Jwz0711~", host="1.92.70.241", port=3306, database="tiger_db")
    print(connection2)

    cur = connection2.cursor()
    sql="select * from ag_15s"
    cur.execute(sql)
    result = cur.fetchall()

    for one in result:
        print(one)
"""
    
# 关闭api,释放相应资源
api.close()