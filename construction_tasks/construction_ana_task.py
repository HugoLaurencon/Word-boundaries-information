def open_file(path_to_txt):
    f = open(path_to_txt, 'r')
    txt = f.read().split('\n')
    f.close()
    return txt


def write_file(path_save, to_write):
    f = open(path_save, 'w')
    f.truncate(0)
    if (to_write[-1] == '\n'):
        f.write(to_write[:-1])
    else:
        f.write(to_write)
    f.close()


def create_ana_task(path_to_nouns, path_to_verbs, path_dir_save_task, dev=True):
    
    if dev:
        name_task = 'ana_easy_dev'
    else:
        name_task = 'ana_easy_test'
        
    nouns = open_file(path_to_nouns)
    nouns = [el.split(' ') for el in nouns]
    if dev:
        nouns = nouns[:len(nouns)//2]
    else:
        nouns = nouns[len(nouns)//2:]
    
    verbs = open_file(path_to_verbs)
    
    to_write = ''
    
    nb = 0
    for noun in nouns:
        for verb in verbs:
            r1 = ' '.join(['the', noun[0], verb, 'himself'])
            w1 = ' '.join(['the', noun[0], verb, 'themselves'])
            r2 = ' '.join(['the', noun[1], verb, 'themselves'])
            w2 = ' '.join(['the', noun[1], verb, 'himself'])
            
            prep1 = name_task + '_' + str(nb) + '_' + 'r1,' + name_task + '_' + str(nb) + '_' + 'w1'
            prep2 = name_task + '_' + str(nb) + '_' + 'r2,' + name_task + '_' + str(nb) + '_' + 'w2'
            prep3 = name_task + '_' + str(nb) + '_' + 'r1,' + name_task + '_' + str(nb) + '_' + 'w2'
            prep4 = name_task + '_' + str(nb) + '_' + 'r2,' + name_task + '_' + str(nb) + '_' + 'w1'
            
            pair1 = ','.join([prep1, r1, w1])
            pair2 = ','.join([prep2, r2, w2])
            pair3 = ','.join([prep3, r1, w2])
            pair4 = ','.join([prep4, r2, w1])
            
            to_write += '\n'.join([pair1, pair2, pair3, pair4]) + '\n'
            nb += 1
        
        for verb in verbs:
            r1 = ' '.join(['the', noun[2], verb, 'herself'])
            w1 = ' '.join(['the', noun[2], verb, 'themselves'])
            r2 = ' '.join(['the', noun[3], verb, 'themselves'])
            w2 = ' '.join(['the', noun[3], verb, 'herself'])
            
            prep1 = name_task + '_' + str(nb) + '_' + 'r1,' + name_task + '_' + str(nb) + '_' + 'w1'
            prep2 = name_task + '_' + str(nb) + '_' + 'r2,' + name_task + '_' + str(nb) + '_' + 'w2'
            prep3 = name_task + '_' + str(nb) + '_' + 'r1,' + name_task + '_' + str(nb) + '_' + 'w2'
            prep4 = name_task + '_' + str(nb) + '_' + 'r2,' + name_task + '_' + str(nb) + '_' + 'w1'
            
            pair1 = ','.join([prep1, r1, w1])
            pair2 = ','.join([prep2, r2, w2])
            pair3 = ','.join([prep3, r1, w2])
            pair4 = ','.join([prep4, r2, w1])
            
            to_write += '\n'.join([pair1, pair2, pair3, pair4]) + '\n'
            nb += 1
            
    write_file(path_dir_save_task + name_task + '.txt', to_write)
    


# path_to_nouns = '/Data/tasks_quantized_scores/score_tasks/ana_easy/task/construction/gender_nouns_sing_plur.txt'
# path_to_verbs = '/Data/tasks_quantized_scores/score_tasks/ana_easy/task/construction/verbs.txt'
# path_dir_save_task = '/Data/tasks_quantized_scores/score_tasks/ana_easy/task/'
# create_ana_task(path_to_nouns, path_to_verbs, path_dir_save_task, dev=True)
# create_ana_task(path_to_nouns, path_to_verbs, path_dir_save_task, dev=False)





