import os
import asyncpg
#import asyncio

URL = os.getenv('DATABASE_URL')

async def register_user(user):
    conn = await asyncpg.connect(URL)
    id = f"{user.name}#{user.discriminator}"

    await conn.execute(f"""INSERT INTO profiles(discord_id, wallet, bank_bal, 
max_bank_bal, level, xp) VALUES ('{id}', 100, 0, 1000, 1, 0)""")
    
    await conn.close()

async def get_user(user):
    conn = await asyncpg.connect(URL)
    id = f"{user.name}#{user.discriminator}"

    row = await conn.fetchrow("SELECT * FROM profiles WHERE discord_id = $1", id)
    
    await conn.close()
    return row

async def set_value(user, value, value_to_set):
    conn = await asyncpg.connect(URL)
    id = f"{user.name}#{user.discriminator}"

    await conn.execute(
        f"""UPDATE profiles SET {value} = {value_to_set} WHERE discord_id = '{id}'""")
    
    await conn.close()

async def test():
    conn = await asyncpg.connect(URL)

    await conn.execute(
     '''CODE HERE'''
    )
    await conn.close()

#asyncio.get_event_loop().run_until_complete(init())