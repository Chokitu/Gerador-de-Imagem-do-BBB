import os,io
from flask import Flask, request, redirect, url_for,Response,render_template,send_file,make_response,jsonify,send_from_directory
from werkzeug.utils import secure_filename
import base64
from PIL import Image
import numpy as np
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from imagem import imagembbb
import uuid


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static\\upload')
VIDEO_FOLDER = os.path.join(APP_ROOT,'static\\video')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)




def allowed_file(filename):
    """
    :param filename: 
    :return: 
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET','POST'])

def upload_file():
    if request.method == 'POST':

        nome = request.form['nome']
        idade = request.form['idade']
        profissao = request.form['profissao']
        cidade = request.form['cidade']

        # np.savetxt('nome.txt', [nome], fmt='%s')
        # np.savetxt('idade.txt', [idade], fmt='%s')
        # np.savetxt('profissao.txt', [profissao], fmt='%s')
        # np.savetxt('cidade.txt', [cidade], fmt='%s')
        
    
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            byte_io = io.BytesIO()
            byte_io.write(file.read())
            byte_io.seek(0)
            response = make_response(send_file(byte_io,mimetype='image/jpg'))
            response.headers['Content-Transfer-Encoding']='base64'
            uuidimage = str(uuid.uuid4())
            imagePath = (uuidimage+".png")
            img = Image.open(byte_io)
            img.save(imagePath, 'png')
            varbbb = imagembbb(nome, idade, profissao, cidade, uuidimage)
            return render_template('bbb.html', img=varbbb)

            


    return render_template('index.html')


@app.route('/bbb', methods=['GET'])

def download_bbb():

    return render_template('bbb.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')


if __name__ == '__main__':
    app.run(debug=True)