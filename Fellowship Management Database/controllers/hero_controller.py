from flask import jsonify, request
from db import db

from models.hero import Heroes, hero_schema, heroes_schema
from models.hero_quest import HeroQuests
from util.reflection import populate_object

# CREATE
def create_hero():
    data = request.form if request.form else request.get_json()
    new_hero = Heroes.new_hero_obj()

    populate_object(new_hero, data)

    try:
        db.session.add(new_hero)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "hero created", "results": hero_schema.dump(new_hero)}), 201

def create_hero_quest():
    post_data = request.form if request.form else request.get_json()
    
    hero_id = post_data.get('hero_id')
    quest_id = post_data.get('quest_id')

    hero = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()
    if not hero:
        return jsonify({"message": "hero not found"}), 404

    association = HeroQuests(hero_id=hero_id, quest_id=quest_id)

    try:
        db.session.add(association)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create association"}), 400
    
    return jsonify({"message": "hero added to quest", "results": hero_schema.dump(hero)}), 201

# READ
def get_all_heroes():
    query = db.session.query(Heroes).all()
    return jsonify({"results": heroes_schema.dump(query)}), 200

def get_alive_heroes():
    query = db.session.query(Heroes).filter(Heroes.is_alive == True).all()
    return jsonify({"results": heroes_schema.dump(query)}), 200

def get_hero_by_id(hero_id):
    query = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()
    if not query:
        return jsonify({"message": "hero not found"}), 404
    return jsonify({"results": hero_schema.dump(query)}), 200

def get_hero_quests(hero_id):
    hero = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()
    if not hero:
        return jsonify({"message": "hero not found"}), 404

    quests = [assoc.quest for assoc in hero.quests]

    from models.quest import quest_schema
    return jsonify({"results": [quest_schema.dump(quest) for quest in quests]}), 200

# UPDATE
def update_hero_by_id(hero_id):
    query = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()
    data = request.form if request.form else request.get_json()

    populate_object(query, data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "hero updated", "results": hero_schema.dump(query)}), 200

# DELETE
def delete_hero_by_id(hero_id):
    query = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()
    if not query:
        return jsonify({"message": "hero not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400
    return jsonify({"message": "hero deleted"}), 200