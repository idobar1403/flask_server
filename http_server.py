import pymongo
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = pymongo.MongoClient("mongodb+srv://noamv:12345@cluster0.5vok1pd.mongodb.net/?retryWrites=true&w=majority")
db = client["DMA"]
guides_collection = db["guides"]

guide = {
    "domain": "www.btl.gov.il",
    "guide_name": "106",
    "steps": [
        {"id": "c1", "action": "color"},
        {"id": "button", "action": "click"}
    ]
}


@app.route('/guide/<domain>/<guide_name>', methods=['GET'])
def get_guide(domain, guide_name):
    guide = guides_collection.find_one({"domain": domain, "guide_name": guide_name}, {"_id": False})
    if guide:
        return jsonify(guide)
    else:
        return jsonify({"message": "Guide not found"}), 404


# define a route to insert a new guide
@app.route('/guide', methods=['POST'])
def insert_guide():
    guide = request.get_json()
    print(guide)
    result = guides_collection.insert_one(guide)
    return jsonify({"message": "Guide inserted", "id": str(result.inserted_id)}), 201

@app.route('/guides/<domain>', methods=['GET'])
def get_guides_by_domain(domain):
    guides = guides_collection.find({"domain": domain}, {"_id": False})
    guides_list = list(guides)
    if guides_list:
        return jsonify(guides_list)
    else:
        return jsonify({"message": "No guides found for the specified domain"}), 404
@app.route('/guides', methods=['GET'])
def get_guides():
    print("here")
    guides = guides_collection.find({"_id": False})
    guides_list = list(guides)
    if guides_list:
        return jsonify(guides_list)
    else:
        return jsonify({"message": "No guides found for the specified domain"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 5000, debug=True)