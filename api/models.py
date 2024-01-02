from app import db

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)
    worktypes = db.relationship('WorkType', backref='user', lazy=True, primaryjoin="User.id == foreign(WorkType.user_id)")
    premium = db.Column(db.Boolean, default=False)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "premium":self.premium,
        }



class WorkType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    todos = db.relationship('Todo', backref='worktype', lazy=True)
   
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
           
            "user_id": self.user_id
        }

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    worktype_id = db.Column(db.Integer, db.ForeignKey('work_type.id'))
    image=db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "completed": self.completed,
            "description": self.description,
            "due_date": str(self.due_date.strftime('%d-%m-%Y')),
            "user_id": self.user_id,
            "worktype_id": self.worktype_id,
            "image":self.image
        }

db.configure_mappers()
