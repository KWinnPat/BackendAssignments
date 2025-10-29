from flask import jsonify, request
from db import db
from models.book import Books


# CREATE

def add_book():
    post_data = request.form if request.form else request.get_json()

    fields = ['title', 'school_id', 'author', 'subject', 'rarity_level', 'magical_properties', 'available']
    required_fields = ['title', 'school_id']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
       
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_book = Books(values['title'], values['school_id'], values['author'], values['subject'], values['rarity_level'], values['magical_properties'], values.get('available', True))

    try:
        db.session.add(new_book)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400
    
    query = db.session.query(Books).filter(Books.title == values['title']).first()

    book = {
        "book_id": query.book_id,
        "title": query.title,
        "school_id": query.school_id,
        "author": query.author,
        "subject": query.subject,
        "rarity_level": query.rarity_level,
        "magical_properties": query.magical_properties,
        "available": query.available
    }

    return jsonify({"message": "book created", "result": book}), 200

# READ

def get_all_books():
    query = db.session.query(Books).all()

    print(query)

    book_list = []

    for book in query:
        book_dict = {
            'book_id': book.book_id,
            'title': book.title,
            'school_id': book.school_id,
            'author': book.author,
            'subject': book.subject,
            'rarity_level': book.rarity_level,
            'magical_properties': book.magical_properties,
            'available': book.available
        }

        book_list.append(book_dict)

    return jsonify({"message": "books found", "results": book_list}), 200

def get_available_books():
    query = db.session.query(Books).filter(Books.available == True).all()

    print(query)

    book_list = []

    for book in query:
        book_dict = {
            'book_id': book.book_id,
            'title': book.title,
            'school_id': book.school_id,
            'author': book.author,
            'subject': book.subject,
            'rarity_level': book.rarity_level,
            'magical_properties': book.magical_properties,
            'available': book.available
        }

        book_list.append(book_dict)

    return jsonify({"message": "available books found", "results": book_list}), 200

# UPDATE

def update_book_by_id(book_id):
    post_data = request.form if request.form else request.get_json()
    query = db.session.query(Books).filter(Books.book_id == book_id).first()
    
    query.title = post_data.get("title", query.title)
    query.school_id = post_data.get("school_id", query.school_id)
    query.author = post_data.get("author", query.author)
    query.subject = post_data.get("subject", query.subject)
    query.rarity_level = post_data.get("rarity_level", query.rarity_level)
    query.magical_properties = post_data.get("magical_properties", query.magical_properties)
    query.available = post_data.get("available", query.available)
    
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    updated_book_query = db.session.query(Books).filter(Books.book_id == book_id).first()

    book = {
        'book_id': updated_book_query.book_id,
        'title': updated_book_query.title,
        'school_id': updated_book_query.school_id,
        'author': updated_book_query.author,
        'subject': updated_book_query.subject,
        'rarity_level': updated_book_query.rarity_level,
        'magical_properties': updated_book_query.magical_properties,
        'available': updated_book_query.available
    }

    return jsonify({"message": "book updated", "result": book}), 200

# DELETE
def delete_book_by_id(book_id):
    query = db.session.query(Books).filter(Books.book_id == book_id).first()
    if not query:
        return jsonify({"message": f"book does not exist"}), 400

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "book deleted"}), 200
