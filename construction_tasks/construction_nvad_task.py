from random import choice
from tqdm import tqdm


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


def create_nvad_task(path_dir_nva_task,
                     path_to_nouns,
                     path_to_verbs,
                     path_to_librispeech_text,
                     path_dir_save_task, dev=True):
    
    if dev:
        name_task = 'nvad_easy_dev'
        nva = open_file(path_dir_nva_task + 'nva_easy_dev.txt')
    else:
        name_task = 'nvad_easy_test'
        nva = open_file(path_dir_nva_task + 'nva_easy_test.txt')
        
    assert len(nva) % 4 == 0
    nva = [[nva[4*i], nva[4*i+1], nva[4*i+2], nva[4*i+3]] for i in range(len(nva)//4)]
        
    nouns = open_file(path_to_nouns)
    nouns = [el.split(' ') for el in nouns]
    
    verbs = open_file(path_to_verbs)
    
    f = open(path_to_librispeech_text, 'r')
    libri_txt = f.read()
    f.close()
    
    to_write = ''
    
    for block in tqdm(nva):
        pair1 = block[0].replace('nva_easy', name_task)
        pair2 = block[1].replace('nva_easy', name_task)
        
        pair1 = pair1.split(',')
        pair1[2] = pair1[2].split(' ')
        pair1[3] = pair1[3].split(' ')
        pair2 = pair2.split(',')
        pair2[2] = pair2[2].split(' ')
        pair2[3] = pair2[3].split(' ')
        
        pair1_save = pair1 * 1
        pair2_save = pair2 * 1
        
        noun = choice(nouns)
        verb = choice(verbs)
        
        while (noun[0] + ' ' + pair1_save[2][2] in libri_txt) or (noun[1] + ' ' + pair2_save[2][2] in libri_txt):
            noun = choice(nouns)
        
        pair1[2] = ' '.join(pair1[2][:2] + ['that', verb, 'the', noun[1]] + pair1[2][2:])
        pair1[3] = ' '.join(pair1[3][:2] + ['that', verb, 'the', noun[1]] + pair1[3][2:])
        pair2[2] = ' '.join(pair2[2][:2] + ['that', verb, 'the', noun[0]] + pair2[2][2:])
        pair2[3] = ' '.join(pair2[3][:2] + ['that', verb, 'the', noun[0]] + pair2[3][2:])
        
        pair3 = ['', '', '', '']
        pair4 = ['', '', '', '']
        
        code = pair1_save[0][:-2]
        pair3[0] = code + 'r3'
        pair3[1] = code + 'w3'
        pair4[0] = code + 'r4'
        pair4[1] = code + 'w4'
        
        pair3[2] = ' '.join(pair1_save[2][:2] + ['that', verb, 'the', noun[0]] + pair1_save[2][2:])
        pair3[3] = ' '.join(pair1_save[3][:2] + ['that', verb, 'the', noun[0]] + pair1_save[3][2:])
        pair4[2] = ' '.join(pair2_save[2][:2] + ['that', verb, 'the', noun[1]] + pair2_save[2][2:])
        pair4[3] = ' '.join(pair2_save[3][:2] + ['that', verb, 'the', noun[1]] + pair2_save[3][2:])
        
        pair1 = ','.join(pair1) + '\n'
        pair2 = ','.join(pair2) + '\n'
        
        pair3 = ','.join(pair3) + '\n'
        pair4 = ','.join(pair4) + '\n'
        
        to_write += pair1 + pair2 + pair3 + pair4
            
    write_file(path_dir_save_task + name_task + '.txt', to_write)
    


# path_dir_nva_task = '/Data/tasks_quantized_scores/score_tasks/nva_easy/task/'
# path_to_nouns = '/Data/tasks_quantized_scores/score_tasks/nvad_easy/task/construction/nouns.txt'
# path_to_verbs = '/Data/tasks_quantized_scores/score_tasks/nvad_easy/task/construction/verbs.txt'
# path_to_librispeech_text = '/Data/models/topline_word_smallbert/construction/quantized/train_text_librispeech.txt'
# path_dir_save_task = '/Data/tasks_quantized_scores/score_tasks/nvad_easy/task/'
# create_nvad_task(path_dir_nva_task, path_to_nouns, path_to_verbs, path_to_librispeech_text, path_dir_save_task, dev=True)
# create_nvad_task(path_dir_nva_task, path_to_nouns, path_to_verbs, path_to_librispeech_text, path_dir_save_task, dev=False)












