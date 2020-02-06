import os
import dlib
import json
import uuid
import scipy.misc
from io import BytesIO
import numpy as np
from PIL import Image
from flask import render_template, request, send_from_directory
from flask import redirect, url_for, flash
from werkzeug.utils import secure_filename

from app import app
from app import db
from app.models import Users


# Conputer Vision
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_recognition_model = dlib.face_recognition_model_v1(
    'dlib_face_recognition_resnet_model_v1.dat')

TOLERANCE = 0.6
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def get_face_encodings(path_to_image):
    image = scipy.misc.imread(path_to_image)
    detected_faces = face_detector(image, 1)
    shapes_faces = [shape_predictor(image, face) for face in detected_faces]

    return [np.array(face_recognition_model.compute_face_descriptor(image, face_pose, 1)) for face_pose in shapes_faces]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/search')
def search():
    return render_template('search.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/uploadImage", methods=["GET", "POST"])
def upload_image():
    target = os.path.join(APP_ROOT, 'images/')

    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print(f"Could not upload directory {target}")

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        phone = request.form["phone"]
        pin_code = request.form["pin_code"]
        med_cond = request.form["med_cond"]
        age = request.form["age"]
        latitude = request.form["lat"]
        longitude = request.form["long"]
        image_uploaded = request.files["file"]
        public_id = str(uuid.uuid4())

        if image_uploaded.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if image_uploaded and allowed_file(image_uploaded.filename):
            filename = image_uploaded.filename
            filename = secure_filename(filename)
            filename = public_id + ".jpg"
            destination = "/".join([target, filename])
            image_uploaded.save(destination)

            encoding = get_face_encodings(image_uploaded)
            enc_list = []
            for i in encoding[0]:
                enc_list.append(i)

            enc_list = json.dumps(enc_list)

            signature = Users(
                public_id=public_id,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                age=age,
                med_cond=med_cond,
                latitude=latitude,
                longitude=longitude,
                pin_code=pin_code,
                face_encoding=enc_list)

        # image_bytes = BytesIO(image_uploaded.read())
        # img = Image.open(image_bytes)
        # size = (128, 128)
        #
        # image_uploaded = img.resize(size)

            db.session.add(signature)
            db.session.commit()

            flash("Image Successfully Uploaded")
            return redirect(url_for("index"))

            # return render_template("upload_result.html", image_name=filename)

    flash("Please upload a .jpg/,jpeg image")
    return redirect(url_for("upload"))


@app.route('/uploadImage/<imgname>')
def show_uploaded_image(imgname):
    return send_from_directory('images', imgname)


@app.route('/searchImage', methods=["GET", "POST"])
def search_image():

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)

        input_img = request.files["file"]

        if input_img and allowed_file(input_img.filename):
            encoding = get_face_encodings(input_img)
            enc_input_image = []
            for i in encoding[0]:
                enc_input_image.append(i)

            enc_input_image = np.array(enc_input_image)

            users = Users.query.all()

            matched_enc = []
            for user in users:
                encs = user.face_encoding
                encs = json.loads(encs)
                encs = np.array(encs)
                match = np.linalg.norm(encs - enc_input_image) <= TOLERANCE
                if match:
                    matched_enc.append(encs)
                else:
                    pass

            # print("matched_enc: ", matched_enc)
            user_info_found_list = []
            user_info_keys = ['public_id', 'first_name', 'last_name', 'phone',
                              'pin_code', 'age', 'med_cond', 'latitude',
                              'longitude']

            if match:
                matched_enc_list = np.array(matched_enc).tolist()
                matched_enc_result = []
                for i in range(len(matched_enc_list)):
                    matched_enc_result.append(matched_enc_list[i])

                matched_enc_result_json_dump = []
                users_found = []
                for i in matched_enc_result:
                    matched_enc_result_json_dump = json.dumps(i)
                    user_found = Users.query.filter_by(
                        face_encoding=matched_enc_result_json_dump).first()
                    users_found.append(user_found)

                for user in users_found:
                    user_info_found = []
                    public_id_found = user.public_id
                    first_name_found = user.first_name
                    last_name_found = user.last_name
                    phone_found = user.phone
                    pin_code_found = user.pin_code
                    age_found = user.age
                    med_cond_found = user.med_cond
                    lat_found = user.latitude
                    long_found = user.longitude
                    user_info_found.extend([public_id_found,
                                            first_name_found,
                                            last_name_found,
                                            phone_found,
                                            pin_code_found,
                                            age_found,
                                            med_cond_found,
                                            lat_found,
                                            long_found])

                    user_info_found_list.append(dict(zip(user_info_keys,
                                                         user_info_found)))

            else:
                user_info_found_list.append("No Match Found")

            return render_template('search_result.html',
                                   user_info=user_info_found_list)

    flash("Please upload a .jpg/,jpeg image")
    return redirect(url_for("search"))


@app.route('/searchImage/<imgname>')
def show_searched_image(imgname):
    return send_from_directory('images', imgname)
