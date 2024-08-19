import importlib.resources as pkg_resources
import os
import pyzipper


def list():
    print("Project Avaliable:\n-Drone Vision \n-Hand Cricket Sign Detection \n-Word Emotion Detection \n-MERN Chat App \n-Java Local Server Chat App \n-Logistic Regression \n-Vehicle Counter \n-SERN To-do list \n-Face Attendance System \n-Rahul PortFolio Website \n-SERN Stack Class Attendance Management For NEC \n-FastAPI Reference Server Build \n-Stream Lit Song Recommender")


def get_resource_path(filename):
    with pkg_resources.path(__package__, filename) as resource_path:
        return str(resource_path)


def _extract_zip(name, zip_file_path, extract_to_path):
    try:
        if not os.path.exists(extract_to_path):
            os.makedirs(extract_to_path)

        zip_file_path = get_resource_path(zip_file_path)

        with pyzipper.AESZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_path)
            print(f"{name} project has been built in {extract_to_path}")

    except Exception as e:
        print(f"An error occurred: {e}")



def drone_vision(path):
    _extract_zip("Drone Vision", "drone_vision.zip", path)


def hand_cricket_sign(path):
    _extract_zip("Hand Cricket Sign Detection", "Hand_Sign.zip", path)


def word_emotion(path):
    _extract_zip("Word Emotion Detection", "Word emotion.zip", path)


def mern_chat_app(path):
    _extract_zip("MERN Stack Chat App", "chat-app.zip", path)


def java_chat_app(path):
    _extract_zip("Java Local Server Chat App", "java-chat-app.zip", path)


def scratch_logistic(path):
    _extract_zip("Scratch Logistic Regression", "LogisticRegression.zip", path)


def vehicle_counter_yolo(path):
    _extract_zip("Vehicle Counter", "Traffic light.zip", path)


def sern_todolist(path):
    _extract_zip("SERN Stack Todo List","todolist.zip",path)


def face_attendance(path):
    _extract_zip("Face Based Attendance System","Face_security.zip",path)


def rahul_portfolio(path):
    _extract_zip("Rahul portfolio","Portfolio-main.zip",path)


def sern_class_attendance_management(path):
    _extract_zip("SERN Based Class Attendance Management","AttendanceSystem.zip",path)


def FastAPI_reference(path):
    _extract_zip("FastAPI python reference to build","FastAPI_Web.zip",path)


def song_recommender(path):
    _extract_zip("Stream Lit Song Recommender","Song_recommender.zip",path)