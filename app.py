from flask import Flask, jsonify, request
from models import db, Item
from prometheus_flask_exporter import PrometheusMetrics
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
db.init_app(app)
metrics = PrometheusMetrics(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    return "Welcome to Flask App!"

@app.route("/items", methods=["GET"])
def get_items():
    items = Item.query.all()
    return jsonify([{"id": i.id, "name": i.name} for i in items])

@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    item = Item(name=data["name"])
    db.session.add(item)
    db.session.commit()
    return jsonify({"id": item.id, "name": item.name}), 201

@app.route("/items/<int:id>", methods=["GET"])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify({"id": item.id, "name": item.name})

@app.route("/items/<int:id>", methods=["PUT"])
def update_item(id):
    data = request.get_json()
    item = Item.query.get_or_404(id)
    item.name = data["name"]
    db.session.commit()
    return jsonify({"id": item.id, "name": item.name})

@app.route("/items/<int:id>", methods=["DELETE"])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
