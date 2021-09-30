# Before executing this script, copy the following command in the shell
# and replace "path_to_private_key_api" by the actual path to the private
# key for the  API (which is a json file):
# export GOOGLE_APPLICATION_CREDENTIALS="path_to_private_key_api"


from google.cloud import texttospeech
from tqdm import tqdm


def text_to_speech(text, voice_code, save_path):

    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        sample_rate_hertz = 16000
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    with open(save_path, "wb") as out:
        out.write(response.audio_content)


def create_speech_similarity_task(paths_to_similarity_task, voices_code, save_dir):
    
    dic_sent = set()
    for path in paths_to_similarity_task:
        f = open(path, 'r')
        txt = f.read().split('\n')
        f.close()
        for line in txt:
            for word in line.split(' '):
                if word != '':
                    dic_sent.add(word)
            
    for sent in tqdm(dic_sent):
        for voice_code in voices_code:
            save_path = save_dir + '/' + sent + '_' + voice_code[-1] + '.wav'
            text_to_speech(sent, voice_code, save_path)


def create_speech_score_task(paths_to_score_task, voices_code, save_dir):
    
    dic_sent = {}
    for path in paths_to_score_task:
        with open(path) as f:
            for line in f:
                spl = line.split(',')
                dic_sent[spl[0]] = spl[2]
                dic_sent[spl[1]] = spl[3]
            
    for sent in tqdm(dic_sent):
        for voice_code in voices_code:
            save_path = save_dir + '/' + sent + '_' + voice_code[-1] + '.wav'
            text_to_speech(dic_sent[sent], voice_code, save_path)
            


# paths_to_similarity_task = ['/Data/tasks_quantized_scores/similarity_tasks/syn/task/syn_dev.txt',
#                             '/Data/tasks_quantized_scores/similarity_tasks/syn/task/syn_test.txt']
# voices_code = ["en-US-Wavenet-A", # Man voice
#                 "en-US-Wavenet-C", # Woman voice
#                 "en-US-Wavenet-H", # Woman voice
#                 "en-US-Wavenet-J"] # Man voice
# save_dir = '/Data/tasks_audio/audio_syn'
# create_speech_similarity_task(paths_to_similarity_task, voices_code, save_dir)


# paths_to_score_task = ['/Data/tasks_quantized_scores/score_tasks/aga_easy/task/aga_easy_dev.txt',
#                         '/Data/tasks_quantized_scores/score_tasks/aga_easy/task/aga_easy_test.txt']
# voices_code = ["en-US-Wavenet-A", # Man voice
#                 "en-US-Wavenet-C", # Woman voice
#                 "en-US-Wavenet-H", # Woman voice
#                 "en-US-Wavenet-J"] # Man voice
# save_dir = '/Data/tasks_audio/audio_aga_easy'
# create_speech_score_task(paths_to_score_task, voices_code, save_dir)



