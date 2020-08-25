from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io
import time


def sample_recognize(local_file_path):
    """
    Transcribe a short audio file using synchronous speech recognition

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """
    client = speech_v1.SpeechClient()
    # local_file_path = 'resources/brooklyn_bridge.raw'

    # The language of the supplied audio
    language_code = "ko-KR"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 22050
    audio_channel_count = 1
    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.FLAC
    config = {
 	"audio_channel_count" : audio_channel_count,
        "language_code": language_code
        #"sample_rate_hertz": sample_rate_hertz,
        #"encoding": encoding,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"STT : {}".format(alternative.transcript))
        Text = alternative.transcript
    
    try:
        return Text
    except:
        return "error"

    #print("time :", time.time() - start)

def get_STT():
    #start = time.time()
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/my_dir/NLP/ApisNLP/swm109-project-e282b0bbf05f.json"
    local_file_path = "/home/pi/my_dir/NLP/voice_file/record.wav"
    return sample_recognize(local_file_path)
    
if __name__ == "__main__":
    #pass
    print(get_STT())
