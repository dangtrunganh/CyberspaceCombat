from app import app

print(app.config['UPLOAD_FOLDER'])

app.run(debug=True)
