from contextlib import closing
import sys
import boto3
import os

def get_TTS(NLP_Text):
    # aws 폴리 접속 인증
    client = boto3.client('polly',region_name='ap-northeast-2',
         aws_access_key_id="AKIATH5XVEXCREBHIIZQ",
         aws_secret_access_key="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"
	)

    #client = boto3.client('polly',region_name='ap-northeast-2')
    print("TTS : ", NLP_Text)
    response = client.synthesize_speech(
        OutputFormat='mp3',
        Text= NLP_Text,
	SampleRate = "22050",
        TextType= 'text',
        LanguageCode= 'ko-KR',
        VoiceId= 'Seoyeon'
    )
    #print(response)


    file = open('/home/pi/robot109/voice_processing/voice_file/TTS.mp3','wb')
    file.write(response['AudioStream'].read())
    file.close()
'''
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = "TTS.wav"

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())

                    
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
	
    return True

'''
if __name__ == "__main__":
    pass
    #get_TTS("내일 구리시 오전 기온은 24도, 오후 기온은 34도 입니다")
