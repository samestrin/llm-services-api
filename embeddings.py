from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.route('/embed', methods=['POST'])
def embed():
    data = request.json
    topic = data.get('topic')
    if not topic:
        return jsonify({'error': 'No topic provided'}), 400

    # Generate the embedding
    embedding = model.encode(topic).tolist()
    return jsonify({'embedding': embedding})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
