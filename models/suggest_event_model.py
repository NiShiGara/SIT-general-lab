def add_suggest_event(conn, event_name, theme_id, type_id, participants, beginning_date, expiration_date, start_time,
                      end_time, organizer_id, location_id, description, picture, mail):
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO event(event_name, theme_id, type_id, participants, beginning_date, expiration_date, start_time, 
    end_time, organizer_id, location_id, description, status_id, status, picture, mail) 
    VALUES (:event_name, :theme_id, :type_id, :participants, :beginning_date, :expiration_date, :start_time, :end_time,
    :organizer_id, :location_id, :description, :status_id, 'suggest', :picture, :mail)
    ''', {"event_name": event_name, "theme_id": theme_id, "type_id": type_id, "participants": participants,
          "beginning_date": beginning_date, "expiration_date": expiration_date, "start_time": start_time,
          "end_time": end_time, "organizer_id": organizer_id, "location_id": location_id, "description": description,
          "status_id": "1", "picture": picture, "mail": mail})
    conn.commit()
    return cur.lastrowid
