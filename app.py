from flask import Flask, render_template, request, redirect, send_from_directory
from blockchain import Blockchain
import os, hashlib

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

bc = Blockchain()
pending_docs = {}

def hash_data(name, aadhaar):
    return hashlib.sha256(f"{name}{aadhaar}".encode()).hexdigest()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    name = request.form['name']
    aadhaar = request.form['aadhaar']
    file = request.files['document']
    if file:
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        pending_docs[name] = {'aadhaar': aadhaar, 'file': file.filename}
        return "✅ Document uploaded successfully! Wait for admin verification."
    return "❌ Upload failed."

@app.route('/admin')
def admin():
    return render_template('admin.html', pending=pending_docs)

@app.route('/verify/<username>')
def verify(username):
    data = pending_docs.get(username)
    if not data:
        return "User not found!"
    h = hash_data(username, data['aadhaar'])
    bc.add_block({'name': username, 'aadhaar': data['aadhaar'], 'hash': h})
    del pending_docs[username]
    return f"✅ {username}'s document verified and added to blockchain."

@app.route('/user_check')
def user_check():
    return render_template('user_check.html', chain=bc.chain)

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
