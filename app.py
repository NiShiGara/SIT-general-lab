from flask import Flask, session



app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

import controllers.event
import controllers.profile