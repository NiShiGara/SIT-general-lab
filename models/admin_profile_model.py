import pandas as pd


def add_new_event(conn, event_name, theme_id, type_id, participants, beginning_date, expiration_date, start_time,
                  end_time, organizer_id, location_id, description, status_id, picture):
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO event (event_name, theme_id, type_id, participants, beginning_date, expiration_date, start_time, 
    end_time, organizer_id, location_id, description, status_id, status, picture) 
    VALUES (:event_name, :theme_id, :type_id, :participants, :beginning_date, :expiration_date, :start_time, :end_time,
    :organizer_id, :location_id, :description, :status_id, 'current', :picture)
    ''', {"event_name": event_name, "theme_id": theme_id, "type_id": type_id, "participants": participants,
          "beginning_date": beginning_date, "expiration_date": expiration_date, "start_time": start_time,
          "end_time": end_time, "organizer_id": organizer_id, "location_id": location_id, "description": description,
          "status_id": status_id, "picture": picture})
    conn.commit()
    return cur.lastrowid


def update_event(conn, event_id, event_name, theme_id, type_id, participants, beginning_date, expiration_date,
                 start_time, end_time, organizer_id, location_id, description, status_id, picture):
    cur = conn.cursor()
    cur.execute('''
    UPDATE event
    SET 
        event_name = :event_name,
        theme_id = :theme_id,
        type_id = :type_id,
        participants = :participants,
        beginning_date = :beginning_date,
        expiration_date = :expiration_date,
        start_time = :start_time,
        end_time = :end_time,
        organizer_id = :organizer_id,
        location_id = :location_id,
        description = :description,
        status_id = :status_id,
        picture = :picture
    WHERE event_id = :event_id
    ''', {"event_id": event_id, "event_name": event_name, "theme_id": theme_id, "type_id": type_id,
          "participants": participants, "beginning_date": beginning_date, "expiration_date": expiration_date,
          "start_time": start_time, "end_time": end_time, "organizer_id": organizer_id, "location_id": location_id,
          "description": description, "status_id": status_id, "picture": picture})
    return conn.commit()


def get_location_by_id(conn):
    return pd.read_sql('''
    SELECT location_name
    FROM location
    LEFT JOIN event USING (location_id)
    GROUP BY location_name
    ''', conn)


def add_new_venue(conn, venue_name):
    cur = conn.cursor()
    cur.execute('''
    INSERT OR IGNORE INTO venue(venue_name) VALUES (:venue_name)
     ''', {"venue_name": venue_name})
    conn.commit()
    return cur.lastrowid


def get_venue_id(conn, venue_name):
    return pd.read_sql('''
    SELECT venue_id
    FROM venue
    WHERE venue_name = :venue_name
    ''', conn, params={"venue_name": venue_name}).values[0][0]


def add_new_location(conn, venue_id, location_name):
    cur = conn.cursor()
    cur.execute('''
    INSERT OR IGNORE 
    INTO location(venue_id, location_name) 
    VALUES (:venue_id, :location_name)
    ''', {"venue_id": venue_id, "location_name": location_name})
    conn.commit()
    return cur.lastrowid


def get_location_id(conn, venue_id, location_name):
    return pd.read_sql('''
    SELECT location_id
    FROM location
    WHERE venue_id = :venue_id AND location_name = :location_name
    ''', conn, params={"venue_id": venue_id, "location_name": location_name}).values[0][0]


def get_users_events(conn):
    return pd.read_sql('''
    SELECT login, rate, event_name, strftime('%d.%m.%Y',beginning_date) as beginning_dat
    FROM user_event
    LEFT JOIN users USING (user_id)
    LEFT JOIN event USING (event_id)
    WHERE rate IS NOT NULL AND rate <> :none
    ORDER BY event_name
    ''', conn, params={"none": "None"})


def delete_event(conn, event_id):
    cur = conn.cursor()
    cur.execute(f'''
    DELETE FROM event
    WHERE event_id=:event_id;
    ''', {"event_id": event_id})
    conn.commit()
    return cur.lastrowid


def get_theme_for_admin(conn):
    return pd.read_sql('''
    SELECT theme_name as name
    FROM theme
    ''', conn)


def get_type_for_admin(conn):
    return pd.read_sql('''
    SELECT
    type_name as name
    FROM type
    ''', conn)


def get_organizer_for_admin(conn):
    return pd.read_sql('''
    SELECT organizer_name as name
    FROM organizer
    ''', conn)


def get_location_for_admin(conn):
    return pd.read_sql('''
    SELECT location_name as name
    FROM location
    GROUP BY name
    ''', conn)


def get_status_for_admin(conn):
    return pd.read_sql('''
    SELECT status_name as name
    FROM status
    ''', conn)


def get_suggest_event(conn):
    return pd.read_sql('''
    SELECT event_name, theme_name, type_name, participants, strftime('%d.%m.%Y',beginning_date) as beginning_dat,
    strftime('%d.%m.%Y',expiration_date) as expiration_dat, start_time, end_time, organizer_name, location_name, 
    venue_name, description, status_name,status_id,event_id,beginning_date,expiration_date,picture, mail
    FROM event 
    LEFT JOIN theme USING (theme_id) 
    LEFT JOIN type USING (type_id) 
    LEFT JOIN organizer USING (organizer_id) 
    LEFT JOIN location USING (location_id) 
    LEFT JOIN venue USING (venue_id) 
    LEFT JOIN status USING (status_id)
    WHERE status = 'suggest'
    ORDER BY status_id, strftime('%Y-%m-%d', beginning_date) DESC, event_name
    ''', conn)


def update_suggest_event(conn, event_id):
    cur = conn.cursor()
    cur.execute('''
    UPDATE event
    SET status= 'current'
    WHERE event_id = :event_id
    ''', {"event_id": event_id})
    return conn.commit()
