from flask import jsonify, request
from db import db

from models.quest import Quests, quest_schema, quests_schema
from util.reflection import populate_object

# CREATE
def create_quest():
    data = request.form if request.form else request.get_json()
    new_quest = Quests.new_quest_obj()

    populate_object(new_quest, data)

    try:
        db.session.add(new_quest)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "quest created", "results": quest_schema.dump(new_quest)}), 201

# READ
def get_quests_by_difficulty(difficulty):
    query = db.session.query(Quests).filter(Quests.difficulty == difficulty).all()
    if not query:
        return jsonify({"message": "no quests found for this difficulty"}), 404
    return jsonify({"results": quests_schema.dump(query)}), 200

def get_quest_by_id(quest_id):
    query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()
    if not query:
        return jsonify({"message": "quest not found"}), 404
    return jsonify({"results": quest_schema.dump(query)}), 200

# UPDATE
def update_quest_by_id(quest_id):
    query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()
    data = request.form if request.form else request.get_json()

    populate_object(query, data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "quest updated", "results": quest_schema.dump(query)}), 200

def set_quest_completed(quest_id):
    query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()
    if not query:
        return jsonify({"message": "quest not found"}), 404

    query.completed = True

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to set quest as completed"}), 400

    return jsonify({"message": "quest marked as completed", "results": quest_schema.dump(query)}), 200

# DELETE
def delete_quest_by_id(quest_id):
    query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()
    if not query:
        return jsonify({"message": "quest not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400