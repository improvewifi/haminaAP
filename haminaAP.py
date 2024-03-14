from flask import Flask, render_template, request, send_file, send_from_directory
from aplocation import *
import os, zipfile, json

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        units = request.form['neededUnits']
        delivery = request.form.getlist('fileReq')
        copiedData = request.form['copiedData']
        fileName = haminaData(units, copiedData)
        with open('/home/walrus/env/hamina/uploads/' + fileName + '.txt', 'r') as f:
            screenText = f.readlines()
        if 'csv' in delivery or 'json' in delivery:
            zip_file_name = fileName + '.zip'
            zip_object = zipfile.ZipFile('/home/walrus/env/hamina/uploads/'+zip_file_name, 'w')
            if 'csv' in delivery:
                zip_object.write('/home/walrus/env/hamina/uploads/'+ fileName + '.csv', os.path.basename('/home/walrus/env/hamina/uploads/'+ fileName + '.csv'))
            if 'json' in delivery:
                zip_object.write('/home/walrus/env/hamina/uploads/'+ fileName + '.txt', os.path.basename('/home/walrus/env/hamina/uploads/' + fileName + '.txt'))
            zip_object.close()
            if 'csv' in delivery or 'json' in delivery:
                return render_template('results.html', filename=zip_file_name, aps=screenText)
            else:
                return render_template('result.html', aps=screenText)
        else:
            return render_template('result.html', aps=screenText) 
    else:
        return render_template('index.html')

app.config['UPLOAD_FOLDER'] = '/home/walrus/env/hamina/uploads/' 
@app.route('/uploads/<filename>')
def fileDownload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], path=filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
