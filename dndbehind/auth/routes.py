from flask import request

from . import bp
from .. import db, models


@bp.route("/user", methods=["POST"])
def create_user():
    userdata = request.get_json()
    new_user = models.User(
        username=userdata["username"],
        email=userdata["email"],
    )
    db.session.add(new_user)

    if "password" in userdata:
        new_user.set_password(userdata["password"])

    db.session.commit()

    return str(new_user.id), 201
