import mysql.connector
from dotenv import load_dotenv
import os
from uuid import uuid4
from datetime import datetime
import pytz
import time
import random
import string
import asyncio
import aiomysql

load_dotenv()


try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()

class UserDB:

    def __init__(self) -> None:
        self.MYSQL_HOST = os.getenv("MYSQL_HOST")
        self.MYSQL_USER = os.getenv("MYSQL_USER")
        self.MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
        self.MYSQL_DB = os.getenv("MYSQL_DB")

    async def pool(self):
        # pool = await aiomysql.create_pool(host=self.MYSQL_HOST, port=3306,user=self.MYSQL_USER, password=self.MYSQL_PASSWORD,db=self.MYSQL_DB, loop=loop)
        return await aiomysql.create_pool(host=self.MYSQL_HOST, port=3306,user=self.MYSQL_USER, password=self.MYSQL_PASSWORD,db=self.MYSQL_DB, loop=loop)
        # async with pool.acquire() as conn:
        #     async with conn.cursor() as cur:

    async def generate_char(self, length=10, upper=None)->str:
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choices(characters, k=length))        
        return random_string if not upper else random_string.upper()

    async def create_user(self, username, email, passwd, token, transfer_enable, expire_in):
        try:
            money=0
            rebate=0
            uuid=uuid4().__str__()
            lang="en_US"
            t=int(time.time())
            u=0
            d=0
            used=0
            total_data_used=0
            # expire_in=datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
            status=1
            reg_date=datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
            reg_ip="127.0.0.1"
            speedlimit=1024
            iplimit=10
            role=0
            server_group=1
            afflink=await self.generate_char()
            verify=1
            ref_by=1
            notice_status=0
            notice_id=None
            affclicks=0
            ga=await self.generate_char(length=16, upper=True)
            ga_status=0
            data_expire_cron=0
            data_used_cron=0
            payout_completed=0.00
            payout_pending=0.00
            payout_balance=0.00
            packageid=None
            plan=None
            image=None
            currency="IRR"
            tg_token=await self.generate_char(length=16)
            telegram_id=0
            telegram_name=None
            notification="""{"sendnotices":"0","dataused":"0","dataexpire":"0","loginnotify":"0"}"""
            last_check_in=None
            user_group=""

            query = """INSERT INTO user (
                username,
                email,
                passwd,
                money,
                rebate,
                uuid,
                token,
                lang,
                t,
                u,
                d,
                transfer_enable,
                used,
                total_data_used,
                expire_in,
                status,
                reg_date,
                reg_ip,
                speedlimit,
                iplimit,
                role,
                server_group,
                afflink,
                verify,
                ref_by,
                notice_status,
                notice_id,
                affclicks,
                ga,
                ga_status,
                data_expire_cron,
                data_used_cron,
                payout_completed,
                payout_pending,
                payout_balance,
                packageid,
                plan,
                image,
                currency,
                tg_token,
                telegram_id,
                telegram_name,
                notification,
                last_check_in,
                user_group
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (username, email, passwd, money, rebate, uuid, token, lang, t, u, d, transfer_enable, used, total_data_used, expire_in, status, reg_date, reg_ip, speedlimit, iplimit, role, server_group, afflink, verify, ref_by, notice_status, notice_id, affclicks, ga, ga_status, data_expire_cron, data_used_cron, payout_completed, payout_pending, payout_balance, packageid, plan, image, currency, tg_token, telegram_id, telegram_name, notification, last_check_in, user_group)
            
            pool = await aiomysql.create_pool(host=self.MYSQL_HOST, port=3306,user=self.MYSQL_USER, password=self.MYSQL_PASSWORD,db=self.MYSQL_DB, loop=loop)
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, values)
                    await conn.commit()
                    await cur.close()
                    conn.close()
                    return cur.lastrowid 
        except:
            return False

    async def update(self, email, transfer_enable, expire_in):
        try:
            query = f"""UPDATE user SET transfer_enable='{transfer_enable}', expire_in='{expire_in}', used=0, total_data_used=0 WHERE email='{email}'"""
            pool = await aiomysql.create_pool(host=self.MYSQL_HOST, port=3306,user=self.MYSQL_USER, password=self.MYSQL_PASSWORD,db=self.MYSQL_DB, loop=loop)
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query)
                    await conn.commit()
                    await cur.close()
                    conn.close()
                    return cur.lastrowid 
        except:
            return False
    
    async def delete(self, email):
        try:
            query = f"""DELETE FROM user WHERE email='{email}'"""
            pool = await aiomysql.create_pool(host=self.MYSQL_HOST, port=3306,user=self.MYSQL_USER, password=self.MYSQL_PASSWORD,db=self.MYSQL_DB, loop=loop)
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query)
                    await conn.commit()
                    await cur.close()
                    conn.close()
                    return cur.lastrowid 
        except:
            return False
        
    async def select(self, email):
        try:
            query = f"""SELECT * FROM user WHERE email='{email}'"""
            pool = await aiomysql.create_pool(host=self.MYSQL_HOST, port=3306,user=self.MYSQL_USER, password=self.MYSQL_PASSWORD,db=self.MYSQL_DB, loop=loop)
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(query)
                    my_user = await cur.fetchone()
                    await cur.close()
                    conn.close()
                    return my_user
        except:
            return False


def get_user_db():
    return UserDB()

# u = UserDB()

# # print(asyncio.run(u.create_user("hajjjj", "hajjjj@ja", "Ddddddddd", "8gug8v88v", 234567890, "2024-06-21 16:07:53")))
# # print(asyncio.run(u.update("hajjjj@ja", 1111111111, "2024-08-21 16:07:53")))
# # print(asyncio.run(u.delete("hajjjj@ja")))
# print(asyncio.run(u.select("string@")))