import pandas as pd


def is_correct_login_and_password(conn, login, password):
    try:
        return pd.read_sql('''
        SELECT user_role
        FROM users
        WHERE login = :login AND password = :password;
        ''', conn, params={"login": login, "password": password}).values[0][0]

    except IndexError:
        return "error"


def add_user(conn, log, passw):
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO users(login, password, user_role) 
    VALUES (:login, :password, "user")
    ''', {"login": log, "password": passw})
    conn.commit()
    return cur.lastrowid


def to_delete_user(conn, user_id):
    cur = conn.cursor()
    cur.execute('''
    DELETE FROM users
    WHERE user_id = :user_id;
    ''', {"user_id": user_id})
    conn.commit()
    return cur.lastrowid


def get_user_id(conn, login):
    try:
        return pd.read_sql('''
        SELECT user_id 
        FROM users
        WHERE login = :login
        ''', conn, params={"login": login}).values[0][0]

    except IndexError:
        return "error"


def get_theme(conn):
    return pd.read_sql('''
    SELECT theme_name as name, COUNT(event_id) AS coun
    FROM theme
    LEFT JOIN event USING (theme_id)
    GROUP BY theme_name
    ''', conn)


def get_type(conn):
    return pd.read_sql('''
    SELECT type_name as name, COUNT(event_id) AS coun
    FROM type
    LEFT JOIN event USING (type_id)
    GROUP BY type_name
    ''', conn)


def get_organizer(conn):
    return pd.read_sql('''
    SELECT organizer_name as name, COUNT(event_id) AS coun FROM organizer
    LEFT JOIN event USING (organizer_id)
    GROUP BY organizer_name
    ''', conn)


def get_location(conn):
    return pd.read_sql('''
    SELECT location_name as name, COUNT(event_id) AS coun
    FROM location
    LEFT JOIN event USING (location_id)
    GROUP BY location_name
    ''', conn)


def get_status(conn):
    return pd.read_sql('''
    SELECT status_name as name, COUNT(event_id) AS coun
    FROM status
    LEFT JOIN event USING (status_id)
    GROUP BY status_name
    ''', conn)


def get_event(conn):
    return pd.read_sql('''
    SELECT event_name, picture, type_name, theme_name,  participants, strftime('%d.%m.%Y', beginning_date) as beginning_dat, 
    strftime('%d.%m.%Y', expiration_date) as expiration_dat, start_time, end_time, organizer_name, location_name,
    venue_name, description, status_name, status_id, event_id, beginning_date, expiration_date
    FROM event 
    LEFT JOIN theme USING (theme_id) 
    LEFT JOIN type USING (type_id) 
    LEFT JOIN organizer USING (organizer_id) 
    LEFT JOIN location USING (location_id) 
    LEFT JOIN venue USING (venue_id) 
    LEFT JOIN status USING (status_id)
    WHERE status = 'current'
    ORDER BY status_id, strftime('%Y-%m-%d', beginning_date) DESC, event_name
    ''', conn)


def get_event_sort(conn, sort):
    return pd.read_sql(f'''
    SELECT event_name, picture, type_name, theme_name, participants, strftime('%d.%m.%Y',beginning_date) as beginning_dat,
    strftime('%d.%m.%Y',expiration_date) as expiration_dat, start_time, end_time, organizer_name, location_name, 
    venue_name, status_name, description, status_id, event_id, beginning_date, expiration_date, status
    FROM event 
    LEFT JOIN theme USING (theme_id) 
    LEFT JOIN type USING (type_id) 
    LEFT JOIN organizer USING (organizer_id) 
    LEFT JOIN location USING (location_id) 
    LEFT JOIN venue USING (venue_id) 
    LEFT JOIN status USING (status_id)
    WHERE status = 'current'
    ORDER BY {sort}
    ''', conn)


def get_event_info(conn, idd):
    return pd.read_sql(f'''
    SELECT event_name, picture, type_name, theme_name, participants, strftime('%d.%m.%Y', beginning_date) as beginning_dat,
    strftime('%d.%m.%Y',expiration_date) as expiration_dat, start_time, end_time, organizer_name, location_name, 
    venue_name, status_name, description, status_id,  event_id
    FROM event  
    LEFT JOIN theme USING (theme_id) 
    LEFT JOIN type USING (type_id) 
    LEFT JOIN organizer USING (organizer_id) 
    LEFT JOIN location USING (location_id) 
    LEFT JOIN venue USING (venue_id) 
    LEFT JOIN status USING (status_id)
    WHERE event_id = {idd}
    ''', conn)


def get_users(conn):
    return pd.read_sql('''
    SELECT * 
    FROM users
    ''', conn)


def to_registrate(conn, user_id, event_id):
    cur = conn.cursor()
    cur.execute('''
    INSERT OR IGNORE 
    INTO user_event(user_id, event_id) 
    VALUES (:user_id, :event_id)
    ''', {"user_id": user_id, "event_id": event_id})
    conn.commit()
    return cur.lastrowid


def to_cancel(conn, user_id, event_id):
    cur = conn.cursor()
    cur.execute('''
    DELETE FROM user_event
    WHERE user_id = :user_id AND event_id = :event_id;
    ''', {"user_id": user_id, "event_id": event_id})
    conn.commit()
    return cur.lastrowid


def get_user_events_only_id(conn, idd):
    return pd.read_sql(f'''
    SELECT event_id
    FROM user_event
    WHERE user_id = {idd}
    ''', conn)


def get_participants(conn):
    return pd.read_sql('''
    SELECT event_id, COUNT(user_id) as coun
    FROM user_event
    GROUP BY event_id
    ''', conn)


def is_correct_password(conn, login):
    return pd.read_sql('''
    SELECT password
    FROM users
    WHERE login = :login;
    ''', conn, params={"login": login}).values[0][0]


def is_was_registarte_to_event(conn, user_id, event_id):
    return pd.read_sql('''
    SELECT user_id
    FROM user_event
    WHERE user_id = :user_id AND event_id = :event_id;
    ''', conn, params={"user_id": user_id, "event_id": event_id})
