import os

import crud
import model
import server

os.system("dropdb reservations")
os.system("createdb reservations")

model.connect_to_db(server.app)
server.app.app_context().push()
model.db.create_all()