from flask import Flask, render_template

from myapp.views.notes import bp as notes_bp

app = Flask(__name__)

app.register_blueprint(notes_bp)

