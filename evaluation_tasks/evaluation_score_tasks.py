def open_file(path_to_txt):
    f = open(path_to_txt, 'r')
    txt = f.read().split('\n')
    f.close()
    return txt


def get_scores(path_to_scores):
    
    scores = open_file(path_to_scores)
    dic_scores = {}
    for line in scores:
        spl = line.split(' ')
        dic_scores[spl[0]] = float(spl[1])
        
    return dic_scores


def evaluate_score_task(path_to_score_task, path_to_scores, cpc_km_bert = False):
    
    task = open_file(path_to_score_task)
    dic_scores = get_scores(path_to_scores)
    
    voices = ['']
    if cpc_km_bert:
        voices = ['_A', '_C', '_H', '_J']
    
    scores = []
    for line in task:
        p1 = line.split(',')[0]
        p2 = line.split(',')[1]
        for voice in voices:
            if (p1 + voice in dic_scores) and (p2 + voice in dic_scores):
                if dic_scores[p1 + voice] > dic_scores[p2 + voice]:
                    scores.append(1)
                else:
                    scores.append(0)
                    
    print(f'{len(scores)}/{len(task)*len(voices)} tests are considered.')
    print(f'The average score for this model for this task is {100*sum(scores)/len(scores):.1f}.')



# path_to_score_task = '/Data/tasks_quantized_scores/score_tasks/aga_easy/task/aga_easy_test.txt'
# path_to_scores = '/Data/tasks_quantized_scores/score_tasks/aga_easy/scores/word/scores.txt'
# cpc_km_bert = False
# evaluate_score_task(path_to_score_task, path_to_scores, cpc_km_bert)











