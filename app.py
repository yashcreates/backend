from api import app, db
import stripe
import requests
import os
import urllib.request
from werkzeug.utils import secure_filename 
from flask import Flask, jsonify,request,render_template,redirect
from api import models
from api.models import db,Todo
from flask import Flask, send_from_directory
from flask import Flask, url_for
from flask import send_file



from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api.queries import resolve_todos, resolve_todo
from api.mutation import resolve_create_todo
from api.mutation import resolve_create_todo, resolve_mark_done, \
    resolve_delete_todo,resolve_update_premium,resolve_create_user,\
    resolve_create_worktype,resolve_delete_work,resolve_addimg,resolve_update_todo,resolve_mutate_worktype
from api.queries import resolve_worktypes,resolver_works,resolve_users,resolve_user,resolve_todos_user
query = ObjectType("Query")

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


query.set_field("todos", resolve_todos)
query.set_field("todo", resolve_todo)
query.set_field("works", resolve_worktypes)
query.set_field("work", resolver_works)
query.set_field("users", resolve_users)
query.set_field("user", resolve_user)
query.set_field("usersTodos", resolve_todos_user)


mutation = ObjectType("Mutation")
mutation.set_field("updatepremium", resolve_update_premium)
mutation.set_field("markDone", resolve_mark_done)
mutation.set_field("createTodo", resolve_create_todo)
mutation.set_field("createUser", resolve_create_user)
mutation.set_field("createWorks", resolve_create_worktype)
mutation.set_field("deleteTodo", resolve_delete_todo)
mutation.set_field("deleteWorks", resolve_delete_work)
mutation.set_field("addImage", resolve_addimg)
mutation.set_field("updateTodo",resolve_update_todo)
mutation.set_field("updateWork",resolve_mutate_worktype)


type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)



stripe.api_key ="sk_test_51ORv1QSDhbqmV2uuVBY6NlsXRN3uJoAdJl2pXcGZqcHdWNBBxVe1EBo5nUwdjH4o9imvZX1DprIU0TI3eBYeSlih00u8TuReTf"


from flask import jsonify

@app.route('/create-checkout-session', methods=['POST', 'GET'])
def create_checkout_session():
    try:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!vvbvbvbb")
        user_id=request.json.get('userId')
        print(user_id)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1ORvBzSDhbqmV2uu1w6vLX0p',
                    'quantity': 1
                }
            ],
            mode="payment",
            success_url="http://localhost:3000/",  # Redirect to the same URL for simplicity
            cancel_url="http://localhost:3000/",
            metadata={'userId': user_id}
        )
        return jsonify({'checkoutSessionUrl': checkout_session.url})
    except Exception as e:
        print("Error creating checkout session:", str(e))
        return jsonify({'error': str(e)}), 500
    

    
@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    print("lllllllllllllkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header,"whsec_67b4008ab33c47913ac036021cf9608102c649e7eb5854d6fec9263391f8ec67"
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event['data']['object']
        user_id = session.get('metadata', {}).get('userId')
        print("Payment was successful.", user_id)
        if user_id:
            # Now, you can use the user ID in your GraphQL mutation or other actions

            # Example: Update premium status using GraphQL mutation
            graphql_url = 'http://localhost:3000/graphql'
            graphql_query = '''
                mutation {
                    updatepremium(userId:"%s") {
                        success
                        user {
                            id
                            name
                            premium
                        }
                    }
                }
            ''' % user_id

            headers = {'Content-Type': 'application/json'}
            response = requests.post(graphql_url, json={'query': graphql_query}, headers=headers)

            if response.status_code == 200:
                print("GraphQL mutation successful:", response.json())
            else:
                print("GraphQL mutation failed:", response.text)

    return "Success", 200



UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({
            "message": 'No file part in the request',
            "status": 'failed'
        })
        resp.status_code = 400
        return resp
  
    files = request.files.getlist('files[]')
      
    errors = {}
    success = False
    filename=""
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            newFile=Todo.query.get(request.form.get("todoId"))
            newFile.image =filename
            db.session.add(newFile)
            db.session.commit()
 
            success = True
        else:
            resp = jsonify({
                "message": 'File type is not allowed',
                "status": 'failed'
            })
            return resp
         
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        errors['status'] = 'failed'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({
            "message": 'Files successfully uploaded',
            "status": 'successs',
            "imag":filename
        })
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp

@app.route('/images', methods=['GET'])
def get_images():
    image_files = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
    images = [{'url': f'/uploads/{image}'} for image in image_files]
    print(images[0]["url"])
    return jsonify({'images': images})



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(file_path)
    print(f"Attempting to serve file: {file_path}")
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'})














@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code




