"""Pictures REST API completed with OpenAI Codex assistance.

The official data, supplied tests and dependency declarations remain unchanged.
See AI_ACKNOWLEDGEMENT.md for the implementation and verification scope.
"""

import json
import os

from flask import abort, jsonify, make_response, request, url_for

from . import app

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
with open(json_url, encoding="utf-8") as picture_file:
    data: list = json.load(picture_file)


def _find_picture(picture_id):
    """Find the resource by its ID rather than its position in the list."""
    return next((picture for picture in data if picture["id"] == picture_id), None)


def _read_picture():
    """Read a complete picture resource and reject invalid JSON with HTTP 400."""
    picture = request.get_json(silent=True)
    required_fields = (
        "id", "pic_url", "event_country", "event_state", "event_city", "event_date"
    )
    if not isinstance(picture, dict) or any(
        field not in picture for field in required_fields
    ):
        abort(make_response(
            jsonify(message="a complete picture JSON object is required"), 400
        ))

    picture_id = picture["id"]
    if isinstance(picture_id, bool) or not isinstance(picture_id, int) or picture_id < 0:
        abort(make_response(
            jsonify(message="picture id must be a nonnegative integer"), 400
        ))
    if any(not isinstance(picture[field], str) for field in required_fields[1:]):
        abort(make_response(jsonify(message="picture details must be strings"), 400))
    return picture

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all picture resources as a JSON array."""
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return the requested resource, or the course's JSON not-found response."""
    picture = _find_picture(id)
    if picture is None:
        return jsonify(message="picture not found"), 404
    return jsonify(picture), 200


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a resource, preserving the assignment's HTTP 302 duplicate rule."""
    picture = _read_picture()
    if _find_picture(picture["id"]) is not None:
        return jsonify(Message=f"picture with id {picture['id']} already present"), 302

    data.append(picture)
    return jsonify(picture), 201, {
        "Location": url_for("get_picture_by_id", id=picture["id"])
    }

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Replace an existing resource; a PUT must retain the URL's resource ID."""
    current = _find_picture(id)
    if current is None:
        return jsonify(message="picture not found"), 404

    picture = _read_picture()
    if picture["id"] != id:
        return jsonify(message="picture id must match the URL"), 400
    current.clear()
    current.update(picture)
    return jsonify(current), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete an existing picture and return the required empty HTTP 204 body."""
    picture = _find_picture(id)
    if picture is None:
        return jsonify(message="picture not found"), 404
    data.remove(picture)
    return "", 204
