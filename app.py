from flask import Flask

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

import controllers.event
import controllers.profile
import controllers.admin_profile
import controllers.suggest_event
