import sqlite3

con = sqlite3.connect("event_db.sqlite")

con.executescript('''
CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
login VARCHAR(30),
password VARCHAR(30),
user_role VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS type(
type_id INTEGER PRIMARY KEY AUTOINCREMENT,
type_name VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS theme(
theme_id INTEGER PRIMARY KEY AUTOINCREMENT,
theme_name VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS venue(
venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
venue_name VARCHAR(70)
);

CREATE TABLE IF NOT EXISTS organizer(
organizer_id INTEGER PRIMARY KEY AUTOINCREMENT,
organizer_name VARCHAR(70)
);

CREATE TABLE IF NOT EXISTS status(
status_id INTEGER PRIMARY KEY AUTOINCREMENT,
status_name VARCHAR(70)
);

CREATE TABLE IF NOT EXISTS location(
location_id INTEGER PRIMARY KEY AUTOINCREMENT,
venue_id INT,
location_name VARCHAR(70),
UNIQUE(venue_id, location_name)
FOREIGN KEY (venue_id)  REFERENCES venue (venue_id)
);

CREATE TABLE IF NOT EXISTS event(
event_id INTEGER PRIMARY KEY AUTOINCREMENT,
event_name VARCHAR(120),
theme_id INT,
type_id INT,
participants INT,
beginning_date DATE,
expiration_date DATE,
start_time TIME,
end_time TIME,
organizer_id INT,
location_id INT,
description VARCHAR(500),
status_id INT,
status VARCHAR(30),
picture VARCHAR(150),
mail VARCHAR(70),
FOREIGN KEY (theme_id)  REFERENCES theme (theme_id),
FOREIGN KEY (type_id)  REFERENCES type (type_id),
FOREIGN KEY (organizer_id)  REFERENCES organizer (organizer_id),
FOREIGN KEY (location_id)  REFERENCES location (location_id),
FOREIGN KEY (status_id)  REFERENCES status (status_id)
);

CREATE TABLE IF NOT EXISTS user_event(
user_event_id INTEGER PRIMARY KEY AUTOINCREMENT,
event_id INT,
user_id INT,
rate VARCHAR(500),
UNIQUE(event_id, user_id)
FOREIGN KEY (event_id)  REFERENCES event (event_id),
FOREIGN KEY (user_id)  REFERENCES user (user_id)
);
''')

con.executescript('''
INSERT INTO type (type_name)
VALUES
('Спектакль'),
('Мастер-класс'),
('Игра'),
('Концерт'),
('Фестиваль'),
('Лекция'),
('Тренинг'),
('Выставка'),
('Открытый микрофон');

INSERT INTO theme (theme_name)
VALUES
('Наука'),
('Культура'),
('Туризм'),
('IT'),
('Экология'),
('Искусство'),
('Поэзия'),
('История'),
('Дизайн'),
('Бизнес'),
('Юмор'),
('Иностранные языки'),
('Разное');

INSERT INTO users (login,password, user_role)
VALUES
('nakao.pd','1234567', 'admin'),
('agapova.dr','qwerty', 'admin'),
('burakov.aa','burpass', 'user'),
('yakimova.av','DkapIdUts', 'user'),
('samoilenko.vs','PspUyhb6', 'user');

INSERT INTO organizer (organizer_name)
VALUES
('Юридическая школа'),
('Школа искусств и гуманитарных наук'),
('Институт математики и компьютерных технология'),
('Восточный институт'),
('Инженерная школа'),
('Политехнический институт'),
('Клуб поэзии ДВФУ'),
('Клуб дебатов'),
('Клуб "Омерта"'),
('Студенческое научное общество'),
('АРИС');

INSERT INTO status (status_name)
VALUES
('Актуально'),
('Перенесено'),
('Отменено'),
('Завершено');

INSERT INTO venue (venue_name)
VALUES
('Синий зал'),
('Коворкинг "Аякс"'),
('А411'),
('А412'),
('Красный холл'),
('D504'),
('А727'),
('А510'),
('А840'),
('А839'),
('А511'),
('D348'),
('Средний зал'),
('Морской зал'),
('Красный зал');

INSERT INTO location (venue_id,location_name)
VALUES
(2,'Корпус А'),
(3,'Корпус А'),
(4,'Корпус А'),
(5,'Корпус А'),
(7,'Корпус А'),
(8,'Корпус А'),
(9,'Корпус А'),
(10,'Корпус А'),
(11,'Корпус А'),
(1,'Корпус B'),
(13,'Корпус B'),
(14,'Корпус B'),
(15,'Корпус B'),
(6,'Корпус D'),
(12,'Корпус D');

INSERT INTO event (event_name,theme_id,type_id,participants,beginning_date,expiration_date,start_time,end_time,organizer_id,location_id,description,status_id, status, picture)
VALUES
('Язык китайского Интернета',12,6,30,'2022-12-27','2022-12-27','16:00','17:30',4,2,'Если вы давно хотели узнать о лексике, употребляемой в китайской интернет-коммуникации и её особенностях, то вы найдёте все ответы на лекции от старшего преподавателя кафедры китаеведения Александра Николаевича Сбоева.',1, 'current', '/static/image/Язык%20китайского%20Интернета.jpg'),
('Интелектуальная игра "История.ру"',8,3,60,'2022-12-21','2022-12-21','17:00','19:00',4,4,'Уверен ли ты, что хорошо знаешь отечественную историю?Можешь это проверить, придя на интеллектуальную игру "История.ру"! Повтори историю нашей Родины и будь готов отвечать на самые разные вопросы! Регистрируйся и приходи ! Ждём всех, заинтересованных в истории',4, 'current', '/static/image/Интелектуальная%20игра%20История.ру.jpg'),
('Поэтический вечер',7,9,30,'2022-12-15','2022-12-15','18:00','19:30',2,14,'На нашем мероприятии каждый может поделиться с друзьями своим любимым стихотворениями на родном языке или просто наслаждаться вечером, слушая романсы и попивая вкуснейший чай с домашней выпечкой. Приходи и раздели весеннее настроение вместе с нами!',4, 'current', '/static/image/Поэтический%20вечер.jpg'),
('Творческий вечер "4 строчки"',7,9,15,'2023-01-17','2023-01-17','11:00','12:30',7,9,'На этом творческом вечере ты сможешь хорошо провести время, слушая (и читая) стихотворения, отдыхая в приятной атмосфере и знакомясь с новыми людьми. ',1, 'current', '/static/image/Творческий%20вечер%204%20строчки.jpg'),
('Ящик пандоры BRAIN ON',1,3,60,'2023-01-05','2023-01-05','14:00','16:00',4,15,'Любишь азарт и эрудирован в науке? Хочешь приятно провести время и потренировать свой ум? Тогда мы приглашаем тебя на интеллектуальную игру "Brain On"! Будь готов отвечать на вопросы из абсолютно разных областей науки! Также тебя ждут приятные призы от наших спонсоров в случае победы.',1, 'current', '/static/image/Ящик%20пандоры%20BRAIN%20ON.jpg'),
('Возможности обучения в Китае',12,6,30,'2022-12-26','2022-12-26','15:00','16:30',4,2,'Chinese speaking club ARIS приглашает всех желающих посетить лекцию, посвящённую возможностям обучения в Китае!

На мероприятии вы сможете узнать: 
почему Китай и зачем уезжать туда учиться? 
как поехать на стажировку? 
какие программы по академической мобильности предлагает ДВФУ? 
магистратура и языковой год в КНР: явки, пароли и подводные камни. 

Также вас ждет лекция от студентки, которая в настоящий момент проходит стажировку в Пекинском университете иностранных языков. ',3, 'current', '/static/image/Возможности%20обучения%20в%20Китае.jpg'),
('Постановка "Старушка-богатырша"',2,1,40,'2022-12-24','2022-12-24','12:00','14:30',4,11,'Изучаете японский или просто интересуетесь культурой страны восходящего Солнца?

Тогда предлагаем вам на один вечер окунуться в мир японских народных сказок и насладиться театральной постановкой по мотивам сказки «Старушка-богатырша» от студентов-японистов 1-го курса

Вас ждёт невероятная история о том, как в канун Нового года одна старушка спасла целую деревню от нашествия демонов.',3, 'current', '/static/image/Постановка%20Старушка-богатырша.jpg'),
('Тестовое мероприятие на 3 человек',4,6,3,'2022-12-28','2022-12-28','19:00','19:30',3,14,'Простое тестовое мероприятие для проверки регистрации.',1, 'current', '/static/image/Тестовое%20мероприятие%20на%203%20человек.jpg'),
('Традиционная игра "Мафия"',13,3,12,'2023-01-24','2023-01-25','18:00','20:00',3,14,'Сыграй с нами в всеми любимую мафию. Найди мафию среди людей, который только что стали тебе друзьяи',1, 'current', '/static/image/Традиционная%20игра%20Мафия.jpg'),
('Лекция про развитие AI',4,6,30,'2022-12-29','2022-12-29','15:00','16:30',3,2,'Лекция об изменения и новвоведениях в AI. Новые технологии. Новые способы развития. Ждет ли нас восстание машин???',2, 'current', '/static/image/Лекция%20про%20развитие%20AI.jpg'),
('Новый год с Дедом морозом-программистом',4,6,3,'2022-12-30','2022-12-30','19:00','19:30',3,1,'Проведи Новый год вместе с айтишниками! Конкурсы, Дед Мороз-программист и многое другое ждет тебя здесь!',1, 'current', '/static/image/Новый%20год%20с%20Дедом%20морозом-программистом.jpg');

INSERT INTO user_event (event_id,user_id, rate)
VALUES
(1,4,'None'),
(2,4,'Оценка: Всё очень понравилось Комментарий: Было круто! Схожу еще раз'),
(3,4,'Оценка: Всё очень понравилось Комментарий: шикарное мероприятие, удобное время, интересные темы'),
(4,4,'None'),
(5,4,'None'),
(6,4,'None'),
(7,4,'None'),
(8,4,'None'),
(9,4,'None'),
(10,4,'None'),
(1,3,'None'),
(2,3,'Оценка: Всё было хорошо Комментарий: норм, но время не удобное!'),
(11,3,'None'),
(3,3,'Оценка: Всё было хорошо Комментарий: хотелось бы аудиторию побольше'),
(8,3,'None'),
(4,3,'None'),
(5,3,'None'),
(6,3,'None'),
(1,5,'None'),
(3,5,'Оценка: Были недостатки Комментарий: организатор хам!!!'),
(2,5,'Оценка: Были недостатки Комментарий: нормально, но аудитория слишком старая'),
(8,5,'None'),
(6,5,'None');
''')

con.commit()
