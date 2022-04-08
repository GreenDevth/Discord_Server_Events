from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def photo_count(code):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM scum_photo_hunter WHERE hunter_code = %s", (code,))
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)


def photo_hunter(code):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("SELECT * FROM scum_photo_hunter WHERE hunter_code=%s", (code,))
        row = cur.fetchone()
        return row
    except Error as e:
        print(e)


def photho_hunter_status(code):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT hunter_code_status FROM scum_photo_hunter WHERE hunter_code=%s', (code,))
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)


def photo_hunter_update_status(code):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("UPDATE scum_photo_hunter SET hunter_code_status = 0 WHERE hunter_code = %s", (code,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
            return None


def photo_hunter_code():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("SELECT hunter_code FROM scum_photo_hunter ORDER BY hunter_id")
        row = cur.fetchall()
        code_list = []
        for index in range(len(row)):
            code_list.append(row[index][0])
        return code_list
    except Error as e:
        print(e)


def players(discord):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM scum_players WHERE DISCORD_ID=%s", (discord,))
        row = cur.fetchone()
        return row[0]
    except Error as e:
        print(e)


def player_info(discord):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("SELECT * FROM scum_players WHERE DISCORD_ID=%s", (discord,))
        row = cur.fetchone()
        return row
    except Error as e:
        print(e)


def player_photo_hunter_update(discord, number):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("UPDATE scum_players SET PHOTO_HUNTER = %s WHERE DISCORD_ID=%s", (number, discord,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
            return None


def get_coin_and_exp(code):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT hunter_award, hunter_exp, hunter_answer FROM scum_photo_hunter WHERE hunter_code=%s', (code,))
        row = cur.fetchone()
        res = list(row)
        return res
    except Error as e:
        print(e)


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


def reset_exp(discord):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("UPDATE scum_players SET EXP = 0 WHERE DISCORD_ID=%s", (discord,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
            return None


def exp_update(discord_id, exp):
    player = player_info(discord_id)
    player_level = player[6]
    player_exp = player[7]
    exp_plus = player_exp + exp
    default_level = 100000
    msg = None
    if default_level <= exp_plus:
        exp_after = exp_plus - default_level
        level_update(discord_id, player_level + 1)
        update_exp(discord_id, exp_after)
        level = player_info(discord_id)
        if level != 0:
            reset_exp(discord_id)
        msg = f'Congratulation Your Level up! {level[6]}'
    elif exp_plus < default_level:
        update_exp(discord_id, exp_plus)
        exp = player_info(discord_id)
        msg = exp[7]
    return msg
