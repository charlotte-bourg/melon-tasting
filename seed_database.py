import os

import crud
import model
import server
from datetime import datetime

os.system("dropdb reservations")
os.system("createdb reservations")
model.connect_to_db(server.app)
server.app.app_context().push()
model.db.create_all()

usr = crud.create_user("hackbright.charlotte@gmail.com")
# res = crud.create_reservation(datetime.now(), 1)
# res2 = crud.create_reservation(datetime(2023,6,4), 1)
res = crud.create_reservation(datetime.now().date(), datetime.strptime('10:30','%H:%M').time(), 1)
res2 = crud.create_reservation(datetime(2023,6,4).date(), datetime.strptime('15:00','%H:%M').time(), 1)
model.db.session.add(usr)
model.db.session.add(res)
model.db.session.add(res2)
model.db.session.commit()