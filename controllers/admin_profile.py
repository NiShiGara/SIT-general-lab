from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.event_model import *
from controllers.functions import *


@app.route('/admin_profile', methods=['GET', 'POST'])
def admin_profile():
    conn = get_db_connection()

    # Начальная инициализация параметров
    admin_panel_button = None
    df_theme = get_theme_for_admin(conn)
    df_type = get_type_for_admin(conn)
    df_organizer = get_organizer_for_admin(conn)
    df_location = get_location_for_admin(conn)
    df_status = get_status_for_admin(conn)
    df_user_event = get_users_events(conn)
    detailed_info = False
    checked_value = False

    # Начальная инициализация session
    if 'event_id' not in session:
        session['event_id'] = 0

    # Просмотр интерфейса каждой функции из панели администратора
    if request.values.get('panel'):
        admin_panel_button = request.values.get('panel').title()

    # Добавление нового мероприятия
    if request.values.get('add_new_event'):
        venue_id, location_name = event(conn, df_location, 'location', 'new_event_venue')
        admin_panel_button = "Добавление"
        add_new_event(conn,
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
                      request.values.get('status'),
                      request.values.get('picture'))

    # Удаление мероприятия
    elif request.values.get('delete_event'):
        session['event_id'] = int(request.values.get('delete_event'))
        admin_panel_button = "Редактирование"
        delete_event(conn, session['event_id'])

    # Просмотр подробной информации о мероприятии
    elif request.values.get('choice_event'):
        session['event_id'] = int(request.values.get('choice_event'))
        admin_panel_button = "Редактирование"

    # Просмотр предложенных мероприятий
    elif request.values.get('choice_event_suggest'):
        session['event_id'] = int(request.values.get('choice_event_suggest'))
        admin_panel_button = "Предложения"

    # Добавление предложенного мероприятия
    elif request.values.get('add_suggest_event'):
        session['event_id'] = int(request.values.get('add_suggest_event'))
        admin_panel_button = "Предложения"
        update_suggest_event(conn, session['event_id'])

    # Удаление предложенного мероприятия
    elif request.values.get('delete_suggest_event'):
        session['event_id'] = int(request.values.get('delete_suggest_event'))
        admin_panel_button = "Предложения"
        delete_event(conn, session['event_id'])

    # Редактирование мероприятия
    elif request.values.get('is_edit_event'):
        checked_value = True
        session['event_id'] = request.values.get('is_edit_event')
        admin_panel_button = "Редактирование"

    # Редактирование полей мероприятия
    elif request.values.get('edit_event'):
        admin_panel_button = "Редактирование"
        venue_id, location_name = event(conn, df_location, 'edit_location', 'edit_event_venue')
        update_event(conn,
                     session['event_id'],
                     request.values.get('edit_event_name'),
                     request.values.get('edit_theme'),
                     request.values.get('edit_type'),
                     request.values.get('edit_event_participants'),
                     request.values.get('edit_event_beginning_dat')[6:11] + "-" +
                     request.values.get('edit_event_beginning_dat')[3:5] + "-" +
                     request.values.get('edit_event_beginning_dat')[0:2],
                     request.values.get('edit_event_expiration_dat')[6:11] + "-" +
                     request.values.get('edit_event_expiration_dat')[3:5] + "-" +
                     request.values.get('edit_event_expiration_dat')[0:2],
                     request.values.get('edit_event_start_time'),
                     request.values.get('edit_event_end_time'),
                     request.values.get('edit_organizer'),
                     int(get_location_id(conn, venue_id, location_name)),
                     request.values.get('edit_event_description'),
                     request.values.get('edit_status'),
                     request.values.get('edit_event_picture'))

    event_info = get_event_info(conn, session['event_id'])
    df_event = get_event(conn)
    df_participants = get_participants(conn)
    df_suggest_event = get_suggest_event(conn)

    list_title = init_list_title()

    html = render_template(
        'admin_profile.html',
        admin_panel_button=admin_panel_button,
        theme_list=df_theme,
        type_list=df_type,
        organizer_list=df_organizer,
        location_list=df_location,
        status_list=df_status,
        user_rate=df_user_event,
        all_events=df_event,
        detailed_info=detailed_info,
        event_info=event_info,
        participants_list=df_participants,
        checked_value=checked_value,
        one_event_info=event_info,
        suggest_event=df_suggest_event,
        len=len,
        list_title=list_title
    )

    return html
