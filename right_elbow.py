import  mediapipe as mp
import cv2
import numpy as np
import uuid
import imageio
import os

mp_drawing = mp.solutions.drawing_utils

mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(b[1] - c[1], b[0] - c[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

file_id = uuid.uuid4()
file_name = f'files/result@{file_id}.txt'

def run(video,default_value,stop_value):

    direction = 0
    counter = 0
    default_value = default_value
    gotten_angles=[]
    stop_value = stop_value
    cap = cv2.VideoCapture(video)
    video_id = uuid.uuid4()
    output_file = f'./static1/{video_id}.mp4'
    writer = imageio.get_writer(output_file, fps=25)

    with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose:
        file = open(file_name, 'w')
        while cap.isOpened():
            suc, frame = cap.read()
            if not suc:
                break
            image_height, image_width, _ = frame.shape
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                ##################
                x = int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * image_width)
                y = int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * image_height)

                right_elbow_x = int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * image_width)

                right_elbow_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * image_height)

                right_shoulder_x = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * image_width)
                right_shoulder_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * image_height)

                right_wrist_x = int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * image_width)
                right_wrist_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * image_height)

                cv2.circle(image, (right_elbow_x, right_elbow_y), 10, (255, 255, 0), 5)
                cv2.circle(image, (right_shoulder_x, right_shoulder_y), 15, (255, 255, 0), 6)
                cv2.circle(image, (right_wrist_x, right_wrist_y), 15, (255, 255, 0), 6)

                cv2.line(image, (right_wrist_x, right_wrist_y), (right_elbow_x, right_elbow_y), (0, 0, 255), 4)
                cv2.line(image, (right_elbow_x, right_elbow_y), (right_shoulder_x, right_shoulder_y), (0, 0, 255), 4)

                ################################

                right_angle = int(calculate_angle(right_shoulder, right_elbow, right_wrist))

                if default_value == 'auto':

                    if right_angle > 90:
                        cv2.putText(image, 'Right Elbow Flexion',
                                    (0, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 5, cv2.LINE_AA
                                    )

                        cv2.putText(image, 'Correct Elbow Flexion',
                                    (0, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 4, cv2.LINE_AA
                                    )


                        if right_angle >= 90:
                            if direction == 1:
                                counter += 0.5
                                direction = 0
                                gotten_angles.clear()

                    gotten_angles.append(right_angle)

                    if right_angle < 90:
                        cv2.putText(image, 'Right Elbow Extension',
                                    (0, 150),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 5, cv2.LINE_AA
                                    )

                        cv2.putText(image, 'Bend Elbow ',
                                    (0, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 4, cv2.LINE_AA
                                    )

                        if right_angle <= 90:
                            if direction == 0:
                                counter += 0.5
                                direction = 1

                elif default_value =='manual':

                    if right_angle > stop_value:
                        cv2.putText(image, 'Right Elbow Flexion',
                                    (0, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 5, cv2.LINE_AA
                                    )

                        cv2.putText(image, 'Correct Elbow Flexion',
                                    (0, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 4, cv2.LINE_AA
                                    )

                        if direction == 1:
                            counter += 0.5
                            direction = 0
                            gotten_angles.clear()

                    gotten_angles.append(right_angle)
                    if right_angle < 90:
                        cv2.putText(image, 'Right Elbow Extension',
                                    (0, 150),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 5, cv2.LINE_AA
                                    )

                        cv2.putText(image, 'Bend Elbow ',
                                    (0, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 4, cv2.LINE_AA
                                    )

                        if right_angle <= 90:
                            if direction == 0:
                                counter += 0.5
                                direction = 1


                cv2.putText(image, f'Right Elbow  Angle : {right_angle}', (0, 200), cv2.FONT_HERSHEY_DUPLEX, 1,
                            (0, 255, 255), 5)
                cv2.rectangle(image, (0, 0), (120, 120), (255, 0, 0), -1)
                cv2.putText(image,str(int(counter)),(1,70),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1.6,(0,0,255),6)
                cv2.putText(image, 'RIGHT ELBOW DETECTION ', (500, 100),
                            cv2.FONT_HERSHEY_DUPLEX,
                            1, (0, 255, 255), 3)


                if counter >= 1:
                    file.write(
                        f" {gotten_angles},  {int(counter)} \n"
                    )
                frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                writer.append_data(frame_rgb)


            except:
                pass

            # cv2.imshow('Mediapipe Feed', image)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        writer.close()

        with open(file_name, 'r') as file:
            lines = file.readlines()

        sections = {}
        # Iterate over the lines in the file
        for line in lines:
            # Extract the numbers and section identifier
            numbers, section = line.strip().split('],')
            numbers = list(map(int, numbers.strip('[]').split(',')))
            section = int(section.strip())

            # Divide the numbers into sections
            if section not in sections:
                sections[section] = []
            sections[section].extend(numbers)

        # Find the maximum value in each section
        max_values = {}
        for section, numbers in sections.items():
            max_values[section] = max(numbers)

        # Print the maximum value in each section

        # Write the results to a new file
        with open(f'static2/right_elbow_angel@{file_id}.txt', 'w') as file:

            for section, max_value in max_values.items():
                if default_value == 'manual':
                    file.write(
                        f"Angle Attained for Elbow Flexion' :  {max_value}, for   Flexion' number {int(section)},  when given default stop value of {stop_value} \n"
                    )
                if default_value == 'auto':
                    file.write(
                        f"Angle Attained for  Elbow Flexion' :  {max_value}, for  Elbow Flexion' number {int(section)},  when given default stop value of 90 \n"
                    )

        os.remove(file_name)
        return file_id, video_id

# video = 'right_elbow.mp4'
# v = run(video, 'manual', 100)
# print(v[1], v[0])


