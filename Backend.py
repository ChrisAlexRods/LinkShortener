from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class UrlMapping(db.Model):
    id = db.Column(db.String(6), primary_key=True)
    url = db.Column(db.String(512))

db.create_all()

def generate_unique_id():
    # Try to generate a unique ID until we succeed
    while True:
        id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if UrlMapping.query.get(id) is None:
            return id

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.json['url']
    # Generate a random unique ID for this URL
    id = generate_unique_id()
    mapping = UrlMapping(id=id, url=original_url)
    db.session.add(mapping)
    db.session.commit()
    # Return the shortened URL to the user
    return jsonify(shortened_url='http://yourdomain/' + id)

@app.route('/<id>', methods=['GET'])
def redirect_url(id):
    mapping = UrlMapping.query.get(id)
    if mapping is None:
        return "URL not found", 404
    else:
        return redirect(mapping.url)
@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)
