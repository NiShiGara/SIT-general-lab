from app import app
from flask import render_template
from models.suggest_event_model import *
from utils import get_db_connection
from controllers.functions import *


@app.route('/suggest_event', methods=['GET', 'POST'])
def suggest_event():
    conn = get_db_connection()

    df_theme = get_theme_for_admin(conn)
    df_type = get_type_for_admin(conn)
    df_organizer = get_organizer_for_admin(conn)
    df_location = get_location_for_admin(conn)
    df_status = get_status_for_admin(conn)

    # Отправка предложенного мероприятия на рассмотрение администратору
    if request.values.get('add_suggest_event'):
        venue_id, location_name = event(conn, df_location, 'location', 'new_event_venue')
        add_suggest_event(conn,
                          request.values.get('new_event_name'),
                          request.values.get('theme'),
                          request.values.get('type'),
                          request.values.get('new_event_part'),
                          request.values.get('new_event_beginning_date')[6:11] + "-" +
                          request.values.get('new_event_beginning_date')[3:5] + "-" +
                          request.values.get('new_event_beginning_date')[0:2],
                          request.values.get('new_event_expiration_date')[6:11] + "-" +
                          request.values.get('new_event_expiration_date')[3:5] + "-" +
                          request.values.get('new_event_expiration_date')[0:2],
                          request.values.get('start_time'),
                          request.values.get('end_time'),
                          request.values.get('organizer'),
                          int(get_location_id(conn, venue_id, location_name)),
                          request.values.get('new_event_description'),
                          request.values.get('picture'),
                          request.values.get('suggest_event_mail'))

    html = render_template(
        'suggest_event.html',
        theme_list=df_theme,
        type_list=df_type,
        organizer_list=df_organizer,
        location_list=df_location,
        status_list=df_status,
        len=len
    )

    return html
