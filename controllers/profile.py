from app import app
from flask import render_template
from utils import get_db_connection
from models.profile_model import *
from models.event_model import get_event_info, get_participants, get_user_events_only_id
from controllers.functions import *


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    conn = get_db_connection()

    # Начальная инициализация параметров
    rate_window = False
    event_id = 0

    # Начальная инициализация session
    if 'status_user' not in session:
        session['status_user'] = []

    # Отмена регистрации пользователя на мероприятии
    if request.values.get('cancel'):
        event_id = int(request.values.get('cancel'))
        to_cancel(conn, session['user_id'], event_id)

    # Оценка мероприятия пользователя
    elif request.values.get('to_rate'):
        session['remember_id_'] = int(request.values.get('to_rate'))
        rate_window = True

    # Просмотр подробной информации о мероприятии
    elif request.values.get('choice_event'):
        event_id = int(request.values.get('choice_event'))

    # Отправка отзыва о мероприятии
    if request.values.get('to_rate_event'):
        rate_box = request.values.get('rate_box')
        rate_text = request.values.get('rate_text')
        rate = "Оценка: " + rate_box + " Комментарий: " + rate_text
        if 'remember_id_' in session:
            to_rate(conn, session['remember_id_'], rate, session['user_id'])
            session.pop('remember_id_', None)

    # Очистка фильтров поиска
    if request.form.get('clear'):
        status = []
        session['status_user'] = []
    else:
        status = request.form.getlist("Статус мероприятия")

    # Поиск мероприятий по фильтрам
    if request.form.get('search'):
        session['status_user'] = status

    df_status = get_status(conn, session['user_id'])
    df_event = get_user_events(conn, session['user_id'])
    event_info = get_event_info(conn, event_id)
    df_participants = get_participants(conn)
    df_event = df_event[((df_event['status_name'].isin(session['status_user'])) | (len(session['status_user']) == 0))]

    # Способы сортировки
    title = request.values.get('select-list')
    if title == 'Отсортировать по алфавиту ↓':
        sort = 'event_name DESC'
        df_event = get_user_events_sort(conn, session['user_id'], sort)
    elif title == 'Отсортировать по алфавиту ↑':
        sort = 'event_name'
        df_event = get_user_events_sort(conn, session['user_id'], sort)
    elif title == 'Отсортировать по дате ↓':
        sort = 'strftime("%Y-%m-%d", beginning_date) DESC'
        df_event = get_user_events_sort(conn, session['user_id'], sort)
    elif title == 'Отсортировать по дате ↑':
        sort = 'strftime("%Y-%m-%d", beginning_date)'
        df_event = get_user_events_sort(conn, session['user_id'], sort)
    elif title == 'Отсортировать по статусу ↓':
        sort = 'status_id DESC'
        df_event = get_user_events_sort(conn, session['user_id'], sort)
    elif title == 'Отсортировать по статусу ↑':
        sort = 'status_id'
        df_event = get_user_events_sort(conn, session['user_id'], sort)
    elif title == 'Рекомендуемая сортировка':
        df_event = get_user_events(conn, session['user_id'])

    df_user_event = get_user_events_only_id(conn, session['user_id']).values.tolist()

    list_title = init_list_title()

    html = render_template(
        'profile.html',
        events=df_event,
        status_list=df_status,
        rate_window=rate_window,
        event_info=event_info,
        participants_list=df_participants,
        len=len,
        title=title,
        user_event_list=df_user_event,
        list_title=list_title
    )

    return html
