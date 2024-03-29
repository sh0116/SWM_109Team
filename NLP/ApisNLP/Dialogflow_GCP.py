import dialogflow_v2 as dialogflow
import json
import boto3
import os

def get_Dialogflow(STT_Text):
    """
    #s3에 Text파일로 저장하는 방법일때
    s3 = boto3.resource('s3')
    obj = s3.Object("nlp.data.swm109", "pc_file/count_number.txt")
    count_number = int(obj.get()['Body'].read())
    #보낼 텍스트
    obj = s3.Object("nlp.data.swm109", "stt_text_file/STT_TEXT_"+str(count_number-1)+".txt")
    text = obj.get()['Body'].read()

    f= open(text_file_name,"w+")
    f.write( str(text,'utf-8') )
    f.close()

    #s3에 Text파일로 저장하는 방법일때
    f= open("/tmp/Temp.txt","w+")
    f.write(response.query_result.fulfillment_text)
    f.close()
    s3.meta.client.upload_file("/tmp/Temp.txt", 'nlp.data.swm109', 'dialogflow_text_file/dialogflow_text_'+str(count_number-1)+'.txt')
    """
 
    # swm109-project 에이전트 인증키
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/my_dir/NLP/ApisNLP/swm109-project-e282b0bbf05f.json"

    #DB-TEST ID
    project_id = 'swm109-project'

    #세션 ID
    session_id = "admin_name_hyeon"

    #언어 코드
    language_code = 'ko'


    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=STT_Text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)


    # print('=' * 20)
    # print('Query text: {}'.format(response.query_result.query_text))
    # print('Detected intent: {} (confidence: {})\n'.format(
    #    response.query_result.intent.display_name,
    #    response.query_result.intent_detection_confidence))
    # print('Fulfillment text: {}\n'.format(
    #    response.query_result.fulfillment_text))
    response_text =  response.query_result.fulfillment_text
    
    return response_text.split(',')


if __name__ == "__main__":
    pass
