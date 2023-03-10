from app import app
from flask import render_template, request, session, make_response
from utils import get_db_connection
from models.profile_model import *
from models.event_model import get_event_info,get_participants

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    conn = get_db_connection()
    info_ = 0
    rate_window = False
    event_id = 0

        # нажата кнопка отменить
    if request.values.get('cancel'):
        event_id = int(request.values.get('cancel'))
        to_cancel(conn,session['user_id'],event_id)

        # нажата кнопка оценить
    elif request.values.get('to_rate'):
        session['remember_id_'] = int(request.values.get('to_rate'))
        rate_window = True
        # нажата кнопка отправить оценку

        # нажата кнопка подробнее
    elif request.values.get('choice_event'):
        event_id = int(request.values.get('choice_event'))
        info_ = 1


    if request.values.get('to_rate_event'):
        rate_box = request.values.get('rate_box')
        rate_text= request.values.get('rate_text')
        rate = "Оценка: " + rate_box+" Комментарий: "+rate_text
        if 'remember_id_' in session:
            to_rate(conn,session['remember_id_'],rate,session['user_id'])
            session.pop('remember_id_', None)

    if 'status_user' not in session:
        session['status_user'] = []

    # нажата кнопка Очистить
    if request.form.get('clear'):
        status = []
        session['status_user'] = []
    else:
        status = request.form.getlist("Статус мероприятия")

    if request.form.get('search'):
        session['status_user'] = status

    df_status = get_status(conn, session['user_id'])
    df_event = get_user_events(conn, session['user_id'])
    event_info = get_event_info(conn, event_id)
    df_event = df_event[((df_event['status_name'].isin(session['status_user'])) | (len(session['status_user']) == 0))]
    df_participants = get_participants(conn)

    print(df_event)

    html = render_template(
        'profile.html',
        events=df_event,
        status_list=df_status,
        rate_window=rate_window,
        event_info=event_info,
        info_=info_,
        participants_list=df_participants,
        len=len
    )

    return html