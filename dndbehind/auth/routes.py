"""Routes for user authentication and management."""

from flask import request, jsonify, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from . import bp
from .. import db, models


@bp.route("/user", methods=["POST"])
def create_user() -> tuple[str, int]:
    """Creates new user according to JSON document in request body.

    Returns:
        tuple[str, int]: message and HTTP result code<br>
            On succes, the message will be the new user ID and the status code will be 201.
            If the email address is already registered, an appropriate message and status code 409 will be returned.
            If any other error occurs, a generic error message and status code 500 will be returned.
    """
    userdata = request.get_json()
    new_user = models.User(
        username=userdata["username"],
        email=userdata["email"],
    )
    try:
        db.session.add(new_user)

        if "password" in userdata:
            new_user.set_password(userdata["password"])
        
        db.session.commit()
        return jsonify(id=new_user.id), 201
    except IntegrityError as integrity_error:
        db.session.rollback()
        return jsonify(error="Conflict", message="Unable to create user; duplicate email address?"), 409
    except Exception as e:
        db.session.rollback()
        return jsonify(error="Unknown error", message="An unexpected error occurred. User not created."), 500


@bp.route("/login", methods=["POST"])
def login_user() -> Response:
    """Logs in user according to JSON document in request body.

    Returns:
        Response: JSON response with user ID and status code<br>
            On success, the response will contain the user ID and status code 200.<br>
            If the username or password is missing, an appropriate message and status code 400 will be returned.<br>
            If the username or password is incorrect, an appropriate message and status code 401 will be returned.
    """
    
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify(msg="Username and password are required."), 400
    
    user = db.session.query(models.User).filter(models.User.username == username).first()
    if user is None or not user.check_password(password):
        return jsonify(msg="Invalid username or password."), 401
    
    if user.disabled:
        return jsonify(msg="User account is disabled."), 401

    user.update_login_time()

    token = create_access_token(identity=str(user.id))
    return jsonify(token=token)


@bp.route("/protected", methods=["GET"])
@jwt_required()
def protected() -> Response:
    """Protected route that requires a valid JWT token to access.

    Returns:
        Reponse: JSON response with the username of the authenticated user.
    """
    current_user_id = get_jwt_identity()

    current_user = models.User.query.get(current_user_id)
    if not current_user:
        return jsonify(msg="Unknown user."), 500
    
    return jsonify(logged_in_as=current_user.username)
