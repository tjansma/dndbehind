"""Routes for user authentication and management."""

from flask import request, jsonify, Response, url_for
from flask_jwt_extended import create_access_token, jwt_required, current_user
from sqlalchemy.exc import IntegrityError

from . import bp
from .. import db, models
from .rbac import role_required, self_or_role_required
from ..utils import make_response_without_resource_state, \
    required_keys_present, make_response_with_resource_state


@bp.route("/user/<int:user_id>", methods=["GET"])
@self_or_role_required("user_id", "admin")
def get_user(user_id: int) -> Response:
    """Retrieves user according to user ID specified in the URL path.

    Args:
        user_id (int): ID of the user to retrieve.

    Returns:
        Response: JSON response with user data.
    """
    try:
        target_user = models.User.from_id(user_id)
        return jsonify(target_user.as_dict())
    except LookupError as lookup_error:
        return jsonify(msg="Unknown user"), 404


@bp.route("/user", methods=["POST"])
def create_user() -> Response:
    """Creates new user according to JSON document in request body.

    Returns:
        tuple[str, int]: message and HTTP result code

            On success, the message will be the new user ID and the status code 
            will be 201.
            If the email address is already registered, an appropriate message 
            and status code 409 will be returned.
            If any other error occurs, a generic error message and status code
            500 will be returned.
    """
    userdata = request.get_json()
    required_keys = {"username", "email", "password"}

    if not required_keys_present(required_keys, userdata):
        return jsonify(
                error="Bad request", message="Missing required fields."
            ), 400

    new_user = models.User(
        username=userdata["username"],
        email=userdata["email"],
    )
    
    try:
        db.session.add(new_user)
        new_user.set_password(userdata["password"])
        db.session.commit()

        response = make_response_with_resource_state(
            message="User created successfully.",
            status_code=201,
            resource_state=new_user.as_dict()
        )
        response.headers["Location"] = url_for(
            'auth.get_user',
            user_id=new_user.id,
            _external=True)

        return response
    
    except IntegrityError as integrity_error:
        db.session.rollback()
        return make_response_without_resource_state(
            message="Unable to create user; duplicate email address?",
            status_code=409)


@bp.route("/user/<int:user_id>", methods=["PUT", "PATCH"])
@self_or_role_required("user_id", "admin")
def update_user(user_id: int) -> Response:
    """Updates user according to JSON document in request body.
    The user ID is specified in the URL path.
    The user ID must be the same as the one in the JWT token, or the user must
    have the "admin" role.

    Args:
        user_id (int): ID of the user to update.

    Returns:
        Response: JSON response with status message of result.        
    """
    valid_field_set = {
        "username",
        "email",
        "password",
        "disabled",
        "last_logged_in"
    }

    updated_userdata = request.get_json()
    target_user = models.User.from_id(user_id)

    # Check if the target user exists
    # If not, return an error message
    if target_user is None:
        return jsonify(msg="Unknown user"), 404
    
    # Check if any valid fields are present in the request
    # If not, return an error message
    if not valid_field_set.intersection(updated_userdata.keys()):
        return jsonify(msg="No valid fields to update."), 400
    
    # Check if any invalid fields are present in the request
    # If so, return an error message
    if set(updated_userdata.keys()).difference(valid_field_set):
        return jsonify(msg="Invalid fields in request."), 400
    
    if "username" in updated_userdata:
        target_user.username = updated_userdata["username"]
    if "email" in updated_userdata:
        target_user.email = updated_userdata["email"]
    if "password" in updated_userdata:
        target_user.set_password(updated_userdata["password"])
    if "disabled" in updated_userdata:
        target_user.disabled = updated_userdata["disabled"]
    if "last_logged_in" in updated_userdata:
        target_user.last_logged_in = updated_userdata["last_logged_in"]
    db.session.commit()

    return jsonify(
            msg="User updated successfully.",
            user=target_user.as_dict())


@bp.route("/login", methods=["POST"])
def login_user() -> Response:
    """Logs in user according to JSON document in request body.

    Returns:
        Response: JSON response with user ID and status code<br>
            On success, the response will contain the user ID and status code 
            200.<br>
            If the username or password is missing, an appropriate message and 
            status code 400 will be returned.<br>
            If the username or password is incorrect, an appropriate message 
            and status code 401 will be returned.
    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify(msg="Username and password are required."), 400

    try:
        user = models.User.from_username(username)
    except LookupError:
        return jsonify(msg="Invalid username or password."), 401

    if not user.check_password(password):
        return jsonify(msg="Invalid username or password."), 401

    if user.disabled:
        return jsonify(msg="User account is disabled."), 401

    user.update_login_time()

    user_roles = [role.name for role in user.roles]

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"roles": user_roles})
    return jsonify(access_token=token)


@bp.route("/whoami", methods=["GET"])
@jwt_required()
def whoami() -> Response:
    """Protected route that requires a valid JWT token to access.

    Returns:
        Reponse: JSON response with the username of the authenticated user.
    """
    try:
        return jsonify(logged_in_as=current_user.as_dict())
    except LookupError as lookup_error:
        return jsonify(msg="Unknown user."), 500

@bp.route("/userrole", methods=["GET"])
@role_required("admin")
def list_all_user_roles() -> Response:
    """List all users and all roles assigned to them.

    Returns:
        Response: JSON with all roles assigned to all users.
    """
    all_users = models.User.query.all()
    result = []
    for user in all_users:
        result.append(user.as_dict())
        result[-1]["roles"] = [ role.as_dict() for role in user.roles ]
    
    return jsonify(result)

@bp.route("/userrole/<int:user_id>", methods=["GET"])
@role_required("admin")
def list_specific_user_roles(user_id: int) -> Response:
    """List all roles assigned to specific user.

    Args:
        user_id (int): user ID to list roles for.

    Returns:
        Response: JSON encoded list of roles.
    """
    user = models.User.from_id(user_id)
    result_dict = user.as_dict()
    result_dict["roles"] = [ role.as_dict() for role in user.roles ]

    return jsonify(result_dict)

@bp.route("/userrole/<int:user_id>", methods=["PUT"])
@role_required("admin")
def add_roles_to_user(user_id: int) -> Response:
    """Adds roles to specified user, identified by user_id.
    Requires list of roles in request body.

    Args:
        user_id (int): user ID of user to add roles to.

    Returns:
        Response:  JSON response with status message of result.
    """
    try:
        target_user = models.User.from_id(user_id)
    except LookupError:
        return jsonify(msg="Unknown user"), 404

    rolenames = request.json.get("roles", None)
    if rolenames is None:
        return jsonify(msg="List of roles missing"), 400
    
    # db.session.begin()
    try:
        for rolename in rolenames:
            current_role = models.Role.from_rolename(rolename)
            if current_role not in target_user.roles:
                target_user.roles.append(current_role)
    except LookupError as lookup_error:
        db.session.rollback()
        return jsonify(msg="Unknown role name."), 400
    
    db.session.commit()
    return jsonify(msg="Roles assigned to user.")

@bp.route("/userrole/<int:user_id>", methods=["DELETE"])
@role_required("admin")
def delete_roles_from_user(user_id: int) -> Response:
    """Removes roles from specified user, identified by user_id.
    Requires list of roles in request body.

    Args:
        user_id (int): user ID of user to remove roles from.

    Returns:
        Response:  JSON response with status message of result.
    """
    try:
        target_user = models.User.from_id(user_id)
    except LookupError:
        return jsonify(msg="Unknown user"), 404
    
    try:
        rolenames = request.json.get("roles", None)
    except AttributeError:
        return jsonify(msg="Malformed request"), 400
    if rolenames is None:
        return jsonify(msg="List of roles missing"), 400
    
    # db.session.begin()
    try:
        for rolename in rolenames:
            current_role = models.Role.from_rolename(rolename)
            target_user.roles.remove(current_role)
    except ValueError:
        db.session.rollback()
        return jsonify(
                msg="Specified role was not assigned to user, cannot remove"
            ), 400
    except LookupError:
        db.session.rollback()
        return jsonify(msg="Unknown role"), 404
    
    db.session.commit()
    return jsonify(msg="Roles removed from user.")
