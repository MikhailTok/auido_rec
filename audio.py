
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import datetime
import os
from pydub import AudioSegment

from openai import OpenAI


from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.environ['API_KEY'],
    base_url=os.environ['BASE_URL'],
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

FRAGMENTS_DIR = "audio_fragments"
os.makedirs(FRAGMENTS_DIR, exist_ok=True)

CONVERTED_DIR = "audio_fragments_converted"
os.makedirs(CONVERTED_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")


def convert_webm_to_mp3(input_path: str, output_path: str):
    audio = AudioSegment.from_file(input_path, format="webm")
    audio.export(output_path, format="mp3", bitrate="192k")


@socketio.on('message')
def handle_message(data):

    sid = request.sid
    # Генерируем уникальное имя для фрагмента
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{FRAGMENTS_DIR}/{sid}_{timestamp}.webm"
    converted_filename = f"{CONVERTED_DIR}/{sid}_{timestamp}.mp3"

    try:
        # Сохраняем фрагмент как отдельный файл
        with open(filename, 'wb') as f:
            f.write(data['data'])
        print(f'Фрагмент сохранен: {filename}, размер: {len(data['data'])} байт')
        # print(type(data['data']))


        convert_webm_to_mp3(filename, converted_filename)        
        # Отправляем подтверждение клиенту
        # socketio.emit('message', {'filename': filename}, to=sid)

        audio_file= open(converted_filename, "rb")

        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )

        print(transcription.text)

        socketio.emit('message',  {"message": transcription.text})

        
    except Exception as e:
        print(f'Ошибка сохранения фрагмента: {str(e)}')
        # socketio.emit('chunk_error', {'error': str(e)}, to=sid)



if __name__ == '__main__':
    socketio.run(app, debug=True)



    