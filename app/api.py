"""Flask application factory and route definitions."""
from __future__ import annotations
from flask import Flask, jsonify, request
from app.db import add_user, get_user
from app.utils import doThing


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.post("/users")
    def create_user():
        payload = request.get_json(silent=True) or {}
        name = payload.get("name", "")
        user_id = add_user(str(name))
        return jsonify(id=user_id), 201

    @app.get("/users/<int:user_id>")
    def read_user(user_id: int):
        u = get_user(user_id)
        if u is None:
            return jsonify(error="not found"), 404
        return jsonify(id=u.id, name=u.name)

    @app.post("/dothing")
    def dothing():
        payload = request.get_json(silent=True) or {}
        name = str(payload.get("name", ""))

        meta = payload.get("meta", [])
        if not isinstance(meta, list) or len(meta) != 9:
            return jsonify(error="meta must be a list of 9 values"), 400

        # doThing(a,b,c,d,e,f,g,h,i,j) -> a=name, puis 9 valeurs
        ok = doThing(
            name,
            meta[0],
            meta[1],
            meta[2],
            meta[3],
            meta[4],
            meta[5],
            meta[6],
            meta[7],
            meta[8],
        )

        if ok is None:
            return jsonify(status="error", result=None), 500
        return jsonify(status="ok", result=bool(ok)), 200

    return app
