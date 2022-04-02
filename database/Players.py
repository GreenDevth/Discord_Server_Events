from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def exists_players(discord_id):
    """ Check Player Exists """
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select count(*) from scum_players where DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)


def players_info(discord_id):
    """ Get player information. """
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select * from scum_players where DISCORD_ID = %s', (discord_id,))
        row = cur.fetchall()
        while row is not None:
            for x in row:
                return x
        return False
    except Error as e:
        print(e)
        return None


def level_update(discord_id, level):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('update scum_players set LEVEL = %s where DISCORD_ID = %s', (level, discord_id,))
        conn.commit()
        print('Level update successfull.')
        cur.close()
        return
    except Error as e:
        print(e)
        return
    finally:
        if conn.is_connected():
            conn.close()
            return
        return


def update_exp(discord_id, exp):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('update scum_players set EXP = %s where DISCORD_ID = %s', (exp, discord_id,))
        conn.commit()
        print('Exp update successfull.')
        cur.close()
        return
    except Error as e:
        print(e)
        return
    finally:
        if conn.is_connected():
            conn.close()
            return
        return


def exp_update(discord_id, exp):
    player = players_info(discord_id)
    player_level = player[6]
    player_exp = player[7]
    exp_plus = player_exp + exp
    default_level = 100000
    msg = None
    if default_level <= exp_plus:
        exp_after = exp_plus - default_level
        level_update(discord_id, player_level + 1)
        update_exp(discord_id, exp_after)
        level = players_info(discord_id)
        msg = f'Congratulation Your Level up! {level[6]}'
    elif exp_plus < default_level:
        update_exp(discord_id, exp_plus)
        exp = players_info(discord_id)
        msg = exp[7]
    return msg


def get_lates_player():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("select * from scum_players order by PLAYERS_ID DESC limit 1")
        row = cur.fetchall()
        for x in row:
            return x
    except Error as e:
        print(e)
