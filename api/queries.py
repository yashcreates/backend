from .models import Todo,User,WorkType
from ariadne import convert_kwargs_to_snake_case
from sqlalchemy import func
from datetime import datetime,timedelta
from app import db
def resolve_todos(obj, info):
    try:
        todos = Todo.query.all()
        todos_data = []

        for todo in todos:
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

            todos_data.append(todo_dict)

        payload = {
            "success": True,
            "errors": None,
            "todos": todos_data
        }
    
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)],
            "todos": None
        }
      
 
    return payload


#

@convert_kwargs_to_snake_case
def resolve_todo(obj, info, todo_id):
    try:
        # Retrieve the Todo item with the specified ID
        todo = Todo.query.get(todo_id)

        # If the todo item exists, create a dictionary representation
        # and include information about the associated user and worktype
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

            # Create the payload
            payload = {
                "success": True,
                "errors": None,
                "todo": todo_dict
            }
        else:
            # If the todo item is not found, return an error
            payload = {
                "success": False,
                "errors": [f"Todo item matching id {todo_id} not found"],
                "todo": None
            }

    except Exception as e:
        # Handle other exceptions if necessary
        payload = {
            "success": False,
            "errors": [str(e)],
            "todo": None
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_worktypes(obj, info):
    try:
        # Retrieve all worktypes from the database
       
        worktypes = WorkType.query.all()

        # If worktypes exist, create a list of dictionary representations
        if worktypes:
            worktypes_data = []

            for worktype in worktypes:
                worktype_dict = worktype.to_dict()

                # Include user information
                user = worktype.user
                if user:
                    worktype_dict['user'] = user.to_dict()
                else:
                    worktype_dict['user'] = None

                # Include todos information
                todos = worktype.todos
                if todos:
                    worktype_dict['todos'] = [todo.to_dict() for todo in todos]
                else:
                    worktype_dict['todos'] = []

                worktypes_data.append(worktype_dict)

            # Create the payload
            payload = {
                "success": True,
                "errors": None,
                "works": worktypes_data
            }
        else:
            # If no worktypes are found, return an empty list
            payload = {
                "success": True,
                "errors": None,
                "works": []
            }

    except Exception as e:
        # Handle other exceptions if necessary
        payload = {
            "success": False,
            "errors": [str(e)],
            "worktypes": None
        }

    return payload



@convert_kwargs_to_snake_case
def resolver_works(obj, info, work_id):  # Updated argument name to match GraphQL query
    try:
        # Retrieve the specific worktype from the database
        worktype = WorkType.query.get(work_id)

        # If the worktype exists, create a dictionary representation
        if worktype:
            worktype_dict = worktype.to_dict()

            # Include user information
            user = worktype.user
            if user:
                worktype_dict['user'] = user.to_dict()
            else:
                worktype_dict['user'] = None

            # Include todos information
            todos = worktype.todos
            if todos:
                worktype_dict['todos'] = [todo.to_dict() for todo in todos]
            else:
                worktype_dict['todos'] = []

            # Create the payload
            payload = {
                "success": True,
                "errors": None,
                "work": worktype_dict
            }
        else:
            # If the worktype is not found, return an error
            payload = {
                "success": False,
                "errors": [f"WorkType with ID {work_id} not found"],
                "work": None
            }

    except Exception as e:
        # Handle other exceptions if necessary
        payload = {
            "success": False,
            "errors": [str(e)],
            "work": None
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_users(obj, info):
    try:
        # Retrieve all users from the database
        users = User.query.all()

        # If users exist, create a list of dictionary representations
        if users:
            users_data = [user.to_dict() for user in users]

            
            # Create the payload
            payload = {
                "success": True,
                "errors": None,
                "users": users_data
            }
        else:
            # If no users found, return an empty list
            payload = {
                "success": True,
                "errors": None,
                "users": []
            }

    except Exception as e:
        # Handle other exceptions if necessary
        payload = {
            "success": False,
            "errors": [str(e)],
            "users": None
        }
    
    return payload

@convert_kwargs_to_snake_case
def resolve_user(obj, info, user_id):
    try:
        # Retrieve the user with the specified ID from the database
        user = User.query.get(user_id)

        # If user exists, create a dictionary representation
        if user:
            user_data = user.to_dict()

            # Create the payload
            payload = {
                "success": True,
                "errors": None,
                "user": user_data
            }
        else:
            # If no user found, return an error
            payload = {
                "success": False,
                "errors": [f"User with ID {user_id} not found"],
                "user": None
            }

    except Exception as e:
        # Handle other exceptions if necessary
        payload = {
            "success": False,
            "errors": [str(e)],
            "user": None
        }

    return payload


@convert_kwargs_to_snake_case

def resolve_todos_user(obj, info,userId):
    try:
        todos =Todo.query.filter_by(user_id=userId).all()

        todos_data = []

        for todo in todos:
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

            todos_data.append(todo_dict)

        payload = {
            "success": True,
            "errors": None,
            "todos": todos_data
        }
    
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)],
            "todos": None
        }

    return payload


