from app import db, app
from api.models import Todo, User, WorkType
from datetime import datetime

app.app_context().push()

# Creating a user
user = User(id="dtrszsrsr",name="k2", email="k@.com", password="12346")
db.session.add(user)
db.session.commit()

# Creating a work type
worktype = WorkType(name="WorkType Example", user=user)
db.session.add(worktype)
db.session.commit()

# Creating a todo associated with the user and work type
todo = Todo(description="Task Example", completed=False, due_date=datetime.today().date(), user=user, worktype=worktype)
db.session.add(todo)
db.session.commit()
