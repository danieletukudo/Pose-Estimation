from flask import Flask, request, jsonify, url_for,Blueprint
import time
import  left_hib
import right_hib
import left_knee
import right_knee
import left_shoulder
import right_shoulder
import left_elbow
import right_elbow
import os


"""
      This is the face recognition API which takes in the image from the web browser and then passes it to the face recogntion
      model which detects and reocgnizes the face and then sends it back to the browser
       """

app = Flask(__name__, static_url_path='/')

bp1 = Blueprint('bp1', __name__, static_folder='static1')
bp2 = Blueprint('bp2', __name__, static_folder='static2')
bp3 = Blueprint('bp3', __name__, static_folder='static3')


# Register the blueprints with the Flask app
app.register_blueprint(bp1)
app.register_blueprint(bp2)

app.register_blueprint(bp3)
UPLOAD_FOLDER = "./static1"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = { 'mp4','mov'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add', methods=['POST'])
def save_file():
    try:
        if request.method == 'POST':

            input_image = request.files['file']

            # image = cv2.imread(input_image.filename)
            # print(image)
            input_video = request.files['file']

            input_file_path = f'files/{time.ctime()}_{input_video.filename}'

            input_video.save(input_file_path)
            if input_image.filename == '':
                return  jsonify({'response':'No  files inserted yet'})


            if input_image and allowed_file(input_image.filename):
                name = request.form.to_dict()

                angle_name = name['angle_name'].lower()
                default_value = name['angle_state'].lower()
                stop_value = int(name['stop_value'])
                print(type(default_value))
                print(default_value)

                if default_value == 'auto' or default_value =='manual' :

                    if angle_name == 'right_shoulder_angel':
                        # print(input_file_path,default_value,stop_value)

                        shoulder = right_shoulder.run(input_file_path,default_value,stop_value)
                        os.remove(input_file_path)
                        video_path = f'{shoulder[1]}.mp4'
                        file_path = f'right_shoulder_angel@{shoulder[0]}.txt'
                        img_url = url_for('bp1.static', filename=video_path, _external=True)
                        file_url = url_for('bp2.static', filename=file_path, _external=True)

                        return jsonify({ 'Exercise_Result' : file_url,'video_Url': img_url

                                        }), 200

                    if angle_name == 'left_shoulder_angel':

                        shoulder = left_shoulder.run(input_file_path, default_value, stop_value)
                        print(input_file_path, default_value, stop_value)
                        os.remove(input_file_path)
                        video_path = f'{shoulder[1]}.mp4'
                        file_path = f'left_shoulder_angel@{shoulder[0]}.txt'
                        img_url = url_for('bp1.static', filename=video_path, _external=True)
                        file_url = url_for('bp2.static', filename=file_path, _external=True)


                        return jsonify({'Exercise_Result': file_url, 'video_Url': img_url

                                        }), 200
                    if angle_name == 'left_elbow_angel':
                        shoulder = left_elbow.run(input_file_path, default_value, stop_value)
                        print(input_file_path, default_value, stop_value)
                        os.remove(input_file_path)
                        video_path = f'{shoulder[1]}.mp4'
                        file_path = f'left_elbow_angel@{shoulder[0]}.txt'
                        img_url = url_for('bp1.static', filename=video_path, _external=True)
                        file_url = url_for('bp2.static', filename=file_path, _external=True)
                        return jsonify({'Exercise_Result': file_url, 'video_Url': img_url

                                        }), 200

                    if angle_name == 'right_elbow_angel':
                        shoulder = right_elbow.run(input_file_path, default_value, stop_value)
                        print(input_file_path, default_value, stop_value)
                        os.remove(input_file_path)
                        video_path = f'{shoulder[1]}.mp4'
                        file_path = f'right_elbow_angel@{shoulder[0]}.txt'
                        img_url = url_for('bp1.static', filename=video_path, _external=True)
                        file_url = url_for('bp2.static', filename=file_path, _external=True)
                        return jsonify({'Exercise_Result': file_url, 'video_Url': img_url

                                        }), 200

                    if angle_name == 'left_knee_angel':
                        shoulder = left_knee.run(input_file_path, default_value, stop_value)
                        print(input_file_path, default_value, stop_value)
                        os.remove(input_file_path)
                        video_path = f'{shoulder[1]}.mp4'
                        file_path = f'left_knee_angel@{shoulder[0]}.txt'
                        img_url = url_for('bp1.static', filename=video_path, _external=True)
                        file_url = url_for('bp2.static', filename=file_path, _external=True)
                        return jsonify({'Exercise_Result': file_url, 'video_Url': img_url

                                        }), 200

                    if angle_name == 'right_knee_angel':
                        shoulder = right_knee.run(input_file_path, default_value, stop_value)
                        print(input_file_path, default_value, stop_value)
                        os.remove(input_file_path)
                        video_path = f'{shoulder[1]}.mp4'
                        file_path = f'right_knee_angel@{shoulder[0]}.txt'
                        img_url = url_for('bp1.static', filename=video_path, _external=True)
                        file_url = url_for('bp2.static', filename=file_path, _external=True)
                        return jsonify({'Exercise_Result': file_url, 'video_Url': img_url
                                        }), 200

                    if angle_name == 'right_hip_angel':
                        shoulder = right_hib.run(input_file_path, default_value, stop_value)
                        print(input_file_path, default_value, stop_value)
                        os.remove(input_file_path)
                        video_path = f'{shoulder[1]}.mp4'
                        file_path = f'right_hip_angel@{shoulder[0]}.txt'
                        img_url = url_for('bp1.static', filename=video_path, _external=True)
                        file_url = url_for('bp2.static', filename=file_path, _external=True)

                        return jsonify({'Exercise_Result': file_url, 'video_Url': img_url
                                        }), 200

                    if angle_name == 'left_hip_angel':
                        shoulder = left_hib.run(input_file_path, default_value, stop_value)
                        print(input_file_path, default_value, stop_value)
                        os.remove(input_file_path)
                        video_path = f'{shoulder[1]}.mp4'
                        file_path = f'left_hip_angel@{shoulder[0]}.txt'
                        img_url = url_for('bp1.static', filename=video_path, _external=True)
                        file_url = url_for('bp2.static', filename=file_path, _external=True)

                        return jsonify({'Exercise_Result': file_url, 'video_Url': img_url
                                        }), 200
                else:

                    return 'invalid angle state'



            else:
                    return jsonify({'response':'Please upload the right video file with extension of  mp4 or mov'})
    except:

        return jsonify({'response': 'invalid input'})

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=7005,debug=True)





