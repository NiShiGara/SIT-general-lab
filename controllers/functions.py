from flask import request, session
from models.admin_profile_model import *


def event(conn, df_location, value_1, value_2):
    location_name = df_location.loc[int(request.values.get(value_1)) - 1][0]
    venue_name = str(request.values.get(value_2))
    add_new_venue(conn, venue_name)
    venue_id = int(get_venue_id(conn, venue_name))
    add_new_location(conn, venue_id, location_name)
    get_location_id(conn, venue_id, location_name)

    return venue_id, location_name


def init_session():
    session['types'] = []
    session['themes'] = []
    session['organizers'] = []
    session['locations'] = []
    session['status'] = []
    session['start_date'] = "0000-00-00"
    session['end_date'] = "9999-99-99"
    session['start_time'] = "00:00"
    session['end_time'] = "23:59"


def init_list_title():
    list_title = ['', '', '', 'Тема', 'Количество участников', 'Дата', 'Дата завершения', 'Время',
                  'Время завершения', 'Организатор', 'Место проведения', 'Аудитория', 'Статус', 'Описание',
                  '0', '0', '0', '0']
    return list_title
