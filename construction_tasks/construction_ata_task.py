from random import sample


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


def create_ata_task(path_to_gender_nouns, path_to_nouns, path_to_verbs, path_dir_save_task, dev=True):
    
    if dev:
        name_task = 'ata_easy_dev'
    else:
        name_task = 'ata_easy_test'
        
    gender_nouns = open_file(path_to_gender_nouns)
    gender_nouns = [el.split(' ') for el in gender_nouns]
    if dev:
        gender_nouns = gender_nouns[:len(gender_nouns)//2]
    else:
        gender_nouns = gender_nouns[len(gender_nouns)//2:]
        
    nouns = open_file(path_to_nouns)
    nouns = [el.split(' ') for el in nouns]
    if dev:
        nouns = nouns[:len(nouns)//2]
    else:
        nouns = nouns[len(nouns)//2:]
    
    verbs = open_file(path_to_verbs)
    
    to_write = ''
    
    nb = 0
    for gender_noun in gender_nouns:
        for noun in sample(nouns, 5):
            for verb in sample(verbs, 3):
                r1 = ' '.join(['the', gender_noun[0], verb, 'himself'])
                w1 = ' '.join(['the', gender_noun[0], verb, 'itself'])
                r2 = ' '.join(['the', noun[0], verb, 'itself'])
                w2 = ' '.join(['the', noun[0], verb, 'himself'])
                
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
            
        for noun in sample(nouns, 5):
            for verb in sample(verbs, 3):
                r1 = ' '.join(['the', gender_noun[1], verb, 'herself'])
                w1 = ' '.join(['the', gender_noun[1], verb, 'itself'])
                r2 = ' '.join(['the', noun[0], verb, 'itself'])
                w2 = ' '.join(['the', noun[0], verb, 'herself'])
                
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
    


# path_to_gender_nouns = '/Data/tasks_quantized_scores/score_tasks/ata_easy/task/construction/gender_nouns.txt'
# path_to_nouns = '/Data/tasks_quantized_scores/score_tasks/ata_easy/task/construction/nouns.txt'
# path_to_verbs = '/Data/tasks_quantized_scores/score_tasks/ata_easy/task/construction/verbs.txt'
# path_dir_save_task = '/Data/tasks_quantized_scores/score_tasks/ata_easy/task/'
# create_ata_task(path_to_gender_nouns, path_to_nouns, path_to_verbs, path_dir_save_task, dev=True)
# create_ata_task(path_to_gender_nouns, path_to_nouns, path_to_verbs, path_dir_save_task, dev=False)




