import pandas as pd


def get_user_events(conn, idd):
    return pd.read_sql('''
    SELECT event_name, picture, type_name, theme_name, participants, strftime('%d.%m.%Y', beginning_date) as beginning_date,
    strftime('%d.%m.%Y', expiration_date) as expiration_date, start_time, end_time, organizer_name, location_name, 
    venue_name, description, status_name, status_id, event_id
    FROM user_event
    LEFT JOIN event USING (event_id) 
    LEFT JOIN theme USING (theme_id) 
    LEFT JOIN type USING (type_id) 
    LEFT JOIN organizer USING (organizer_id) 
    LEFT JOIN location USING (location_id) 
    LEFT JOIN venue USING (venue_id) 
    LEFT JOIN status USING (status_id)
    WHERE user_id = :id
    ORDER BY status_id, strftime('%Y-%m-%d', beginning_date) DESC, event_name 
    ''', conn, params={"id": idd})


def get_user_events_sort(conn, idd, sort):
    return pd.read_sql(f'''
    SELECT event_name, picture, type_name, theme_name, participants, strftime('%d.%m.%Y', beginning_date) as beginning_date,
    strftime('%d.%m.%Y', expiration_date) as expiration_date, start_time, end_time, organizer_name, location_name, 
    venue_name, description, status_name, status_id, event_id
    FROM user_event
    LEFT JOIN event USING (event_id) 
    LEFT JOIN theme USING (theme_id) 
    LEFT JOIN type USING (type_id) 
    LEFT JOIN organizer USING (organizer_id) 
    LEFT JOIN location USING (location_id) 
    LEFT JOIN venue USING (venue_id) 
    LEFT JOIN status USING (status_id)
    WHERE user_id = :id
    ORDER BY {sort} 
    ''', conn, params={"id": idd})


def get_status(conn, idd):
    return pd.read_sql(f'''
    SELECT status_name as name, COUNT(event_id) AS coun
    FROM status
    LEFT JOIN event USING (status_id)
    LEFT JOIN user_event USING (event_id)
    WHERE user_id = {idd}
    GROUP BY status_name
    ''', conn)


def to_cancel(conn, user_id, event_id):
    cur = conn.cursor()
    cur.execute('''
    DELETE FROM user_event
    WHERE user_id = :user_id AND event_id = :event_id;
    ''', {"user_id": user_id, "event_id": event_id})
    conn.commit()
    return cur.lastrowid


def to_rate(conn, event_id, text, user_id):
    cur = conn.cursor()
    cur.execute('''
    UPDATE user_event
    SET rate = :text
    WHERE user_id = :user_id AND event_id = :event_id
     ''', {"user_id": user_id, "event_id": event_id, "text": text})
    conn.commit()
    return cur.lastrowid


def get_user_events_(conn, idd):
    return pd.read_sql(f'''
    SELECT event_name, rate, user_id
    FROM user_event
    LEFT JOIN event USING (event_id) 
    WHERE user_id = {id}
    ''', conn)
