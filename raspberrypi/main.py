import websocket
import pyaudio
import json
import threading

# AssemblyAI API key
ASSEMBLYAI_API_KEY = ""

# Audio configuration
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 16000

# Control flag for pausing/resuming data sending
is_paused = threading.Event()
is_paused.set()  # Initially set to pause

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

# WebSocket URL
WEBSOCKET_URL = f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={SAMPLE_RATE}"

# WebSocket callbacks
def on_message(ws, message):
    # Parse the message
    response = json.loads(message)
    if response['message_type'] == 'PartialTranscript':
        print(f"Partial: {response['text']}")
    elif response['message_type'] == 'FinalTranscript':
        print(f"Final: {response['text']}")

def on_error(ws, error):
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket connection established")

    def send_audio():
        try:
            while True:
                if is_paused.is_set():
                    continue  # Skip sending audio if paused

                # Read audio data from the microphone
                data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)

                # Send binary data to the WebSocket
                ws.send(data, opcode=websocket.ABNF.OPCODE_BINARY)
        except Exception as e:
            print(f"Error in audio streaming: {e}")
        finally:
            print("Audio stream stopped")

    # Start audio streaming in a separate thread
    threading.Thread(target=send_audio, daemon=True).start()

# WebSocket initialization
websocket.enableTrace(False)
ws = websocket.WebSocketApp(
    WEBSOCKET_URL,
    header={"Authorization": ASSEMBLYAI_API_KEY},
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
    on_open=on_open,
)

# Function to toggle pause/resume
def toggle_pause():
    if is_paused.is_set():
        print("Resuming transcription...")
        is_paused.clear()
    else:
        print("Pausing transcription...")
        is_paused.set()

# Run WebSocket and handle user input
try:
    print("Starting transcription... Press 'p' to pause/resume. Press 'q' to quit.")
    threading.Thread(target=ws.run_forever, daemon=True).start()

    while True:
        user_input = input()
        if user_input.lower() == 'p':
            toggle_pause()
        elif user_input.lower() == 'q':
            print("Exiting...")
            break
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ws.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
