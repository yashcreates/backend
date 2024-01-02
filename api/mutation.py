from datetime import datetime

from ariadne import convert_kwargs_to_snake_case

from api import db
from api.models import Todo,User,WorkType



@convert_kwargs_to_snake_case
def resolve_mark_done(obj, info, todo_id):
    try:
        todo = Todo.query.get(todo_id)
        if(todo.completed ==1):
            todo.completed=0
        else:
            todo.completed=1
        db.session.add(todo)
        db.session.commit()
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors":  [f"Todo matching id {todo_id} was not found"]
        }

    return payload


@convert_kwargs_to_snake_case
def resolve_delete_todo(obj, info, todo_id):
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        payload = {"success": True}

    except AttributeError:
        payload = {
            "success": False,
            "errors": [f"Todo matching id {todo_id} not found"]
        }

    return payload

def resolve_delete_work(obj, info, workId):
    try:
        todo = WorkType.query.get(workId)
        db.session.delete(todo)
        db.session.commit()
        payload = {"success": True}

    except AttributeError:
        payload = {
            "success": False,
            "errors": [f"Todo matching id {workId} not found"]
        }

    return payload


from datetime import datetime 
@convert_kwargs_to_snake_case
def resolve_update_premium(obj, info,user_id):
    try:
        user = User.query.get(user_id)
        if user:
            if(user.premium==1):
                 payload = {
                 "success": True,
                "user": user.to_dict()
                }
            else:
                user.premium=1

                db.session.add(user)
                db.session.commit()
                payload = {
                    "success": True,
                    "user": user.to_dict()
                }
        else:
             payload = {
            "success": False,
            "user": user.to_dict()
        }


    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": ["Incorrect date format provided. user"]
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": [f"user matching id {user_id} not found"]
        }
    return payload

@convert_kwargs_to_snake_case
def resolve_create_todo(obj, info, description, due_date, user_id, workname):
    
    try:
        due_date = datetime.strptime(due_date, '%d-%m-%Y').date()
        user = User.query.filter_by(id=user_id).first()
        work = WorkType.query.filter_by(name=workname, user_id=user_id).first()
        
        todo = Todo(
            description=description, due_date=due_date, user=user, worktype=work
        )
        db.session.add(todo)
        db.session.commit()
    
        if todo:
            todo_dict = todo.to_dict()

            # Include user information
            user = todo.user
            if user:
                todo_dict['user'] = user.to_dict()
            else:
                todo_dict['user'] = None

            # Include worktype information
            worktype = todo.worktype
            if worktype:
                todo_dict['worktype'] = worktype.to_dict()
            else:
                todo_dict['worktype'] = None
        
        payload = {
            "success": True,
            "todo": todo_dict
        }
    except ValueError:  
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }

    return payload



@convert_kwargs_to_snake_case
def resolve_create_user(obj, info, id, name, email, password):
    try:
        # Check if a user with the given id already exists
        existing_user = User.query.filter_by(id=id).first()
        print(existing_user)
        print(id)

        if existing_user:
            payload = {
                "success": True,
                "errors": None,
                "user": existing_user.to_dict()
            }
        else:
            # Create a new user instance
            print("hi")
            new_user = User(id=id, name=name, email=email, password=password)
            print("m")
            # Add the user to the database session
            db.session.add(new_user)
            print("k")
            # Commit the changes to the database
            db.session.commit()
            print("bye")
            # Return the newly created user in the response
            payload = {
                "success": True,
                "errors": None,
                "user": new_user.to_dict()
            }

    except Exception as e:
        # Handle exceptions if necessary
        payload = {
            "success": False,
            "errors": [str(e)],
            "user": None
        }

    return payload


@convert_kwargs_to_snake_case
def resolve_create_worktype(obj, info, name, user_id):
    try:
        # Check if the user with the provided user_id exists
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        workk=WorkType.query.filter_by(name=name,user=user).first()
        if workk:
             payload = {
            "success": False,
            "errors": None,
            "work": workk.to_dict()
                }
        else:
        # Create a new worktype instance
            new_worktype = WorkType(name=name, user=user)

            # Add the worktype to the database session
            db.session.add(new_worktype)

            # Commit the changes to the database
            db.session.commit()

            # Return the newly created worktype in the response
            payload = {
                "success": True,
                "errors": None,
                "work": new_worktype.to_dict()
            }

    except Exception as e:
        # Handle exceptions if necessary
        payload = {
            "success": False,
            "errors": [str(e)],
            "work": None
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_addimg(obj, info, img, todo_id):  # Ensure 'todoId' matches the GraphQL schema
    try:
        print("lll")
        todo = Todo.query.filter_by(id=todo_id).first()
        print("mmmmm")

        todo.image = img
        print("nnnnnnn")
        db.session.add(todo)
        print("000000")
        db.session.commit()
        print("ppppppp")
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }

    except ValueError:  # date format errors
        print("ggggggg")
        payload = {
            "success": False,
            "errors": ["Incorrect date format provided. Date should be in the format dd-mm-yyyy"]
        }
    except AttributeError:  # todo not found
        print("hhhhhhhhhhh")
        payload = {
            "success": False,
            "errors": [f"Todo matching id {todo_id} not found"]
        }
    print("vvvvvvvv")
    return payload





@convert_kwargs_to_snake_case
def resolve_update_todo(obj, info, todo_id, description=None, due_date=None):
    print("llllloooooooooooooooooooooo",todo_id)
    try:
        todo = Todo.query.filter_by(id=todo_id).first()

        if not todo:
            return {
                "success": False,
                "errors": [f"Todo with ID {todo_id} not found."]
            }

        update_data = {}

        if description is not None and description!=" " and description!="" :
            update_data['description'] = description

        if due_date is not None:
            try:
                update_data['due_date'] = datetime.strptime(due_date, '%d-%m-%Y').date()
            except ValueError:
                return {
                    "success": False,
                    "errors": [f"Incorrect date format provided. Date should be in the format dd-mm-yyyy"]
                }

       

        Todo.query.filter_by(id=todo_id).update(update_data)
        db.session.commit()

        updated_todo = Todo.query.get(todo_id)
        updated_todo_dict = updated_todo.to_dict()

        user = updated_todo.user
        worktype = updated_todo.worktype

        if user:
            updated_todo_dict['user'] = user.to_dict()
        else:
            updated_todo_dict['user'] = None

        if worktype:
            updated_todo_dict['worktype'] = worktype.to_dict()
        else:
            updated_todo_dict['worktype'] = None

        payload = {
            "success": True,
            "todo": updated_todo_dict
        }

    except Exception as e:
        payload = {
            "success": False,
            "errors": [str(e)]
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_mutate_worktype(obj, info,work_id,name,user_id):
    try:
        user = User.query.get(user_id)
        workk=WorkType.query.filter_by(name=name,user=user).first()
        if workk:
             payload = {
            "success": False,
            "errors": None,
            "work":workk.to_dict()
             }
        else:
        # Check if the user with the provided user_id exists
            work = WorkType.query.filter_by(id=work_id).first()
            if not work:
                raise ValueError(f"User with ID {work_id} not found")

            # Create a new worktype instance
            work.name=name
            # Add the worktype to the database session
            db.session.add(work)

            # Commit the changes to the database
            db.session.commit()
            new=WorkType.query.filter_by(id=work_id).first()
            # Return the newly created worktype in the response
            payload = {
                "success": True,
                "errors": None,
                "work":new.to_dict()
            }

    except Exception as e:
        # Handle exceptions if necessary
        payload = {
            "success": False,
            "errors": [str(e)],
            "work": None
        }

    return payload