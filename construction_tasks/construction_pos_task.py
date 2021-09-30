import numpy as np
import random
from Levenshtein import distance as dist


def txt_to_list(path_file):
    f = open(path_file, 'r')
    txt = f.read()
    txt_list = txt.split('\n')
    f.close()
    return txt_list


def write(path_file, to_write):
    f = open(path_file, 'w')
    f.truncate(0)
    f.write(to_write)
    f.close()


def create_pos_task(path_to_adj,
                    path_to_noun,
                    path_to_verb,
                    path_to_librispeech_text,
                    path_to_phonemes_adj,
                    path_to_phoneme_noun,
                    path_to_phoneme_verb,
                    path_save_task,
                    freq_sim,
                    len_sim,
                    edit_sim,
                    num_produced):
    
    adj = txt_to_list(path_to_adj)
    noun = txt_to_list(path_to_noun)
    verb = txt_to_list(path_to_verb)
    
    all_words = adj + noun + verb
    dic_all_words = {el: 1 for el in all_words}
    
    phoneme_adj = txt_to_list(path_to_phoneme_adj)
    phoneme_noun = txt_to_list(path_to_phoneme_noun)
    phoneme_verb = txt_to_list(path_to_phoneme_verb)
    all_phonemes = phoneme_adj + phoneme_noun + phoneme_verb
    
    assert(len(adj) == len(phoneme_adj))
    assert(len(noun) == len(phoneme_noun))
    assert(len(verb) == len(phoneme_verb))
    
    dic_word_phoneme = {all_words[i]: all_phonemes[i] for i in range(len(all_words))}
    
    with open(path_to_librispeech_text) as f:
        text_librispeech = f.read()
        text_librispeech_split = text_librispeech.replace('\n', ' ').split(' ')
    freq_libri = {}
    for word in text_librispeech_split:
        if word in dic_all_words:
            if word in freq_libri:
                freq_libri[word] += 1
            else:
                freq_libri[word] = 1
    
    n_produced = 0
    previous_a_x = set()
    to_write = ''
    
    while n_produced < num_produced:
        
        cat = np.random.randint(0, 3)
        if cat == 0:
            word_cat = adj
            word_not_cat = noun + verb
        elif cat == 1:
            word_cat = noun
            word_not_cat = adj + verb
        elif cat == 2:
            word_cat = verb
            word_not_cat = adj + noun
            
        A = random.choice(word_cat)
        X = random.choice(word_cat)
        if (A != X) and (A + ' ' + X not in previous_a_x) and (X + ' ' + A not in previous_a_x):
            
            list_B = []
            for word in word_not_cat:       
                if np.abs(np.log(freq_libri[word])/np.log(freq_sim) \
                          - np.log(freq_libri[A])/np.log(freq_sim)) <= 1:
                    if (len(word) >= (1-len_sim)*len(A)) and \
                        (len(word) <= (1+len_sim)*len(A)):
                            p_A = dic_word_phoneme[A]
                            p_X = dic_word_phoneme[X]
                            p_word = dic_word_phoneme[word]
                            if np.abs(dist(p_A, p_X) - dist(p_X, p_word)) <= edit_sim:
                                list_B.append(word)
            
            if len(list_B) >= 5:
                previous_a_x.add(A + ' ' + X)
                n_produced += 1
                to_write += ' '.join([A, X]+ list_B)
                if n_produced < num_produced:
                    to_write += '\n'
                
                if n_produced % 100 == 0:
                    print("Number produced:", n_produced)
            
    write(path_save_task, to_write)
        


# path_to_adj = '/Data/tasks_quantized_scores/similarity_tasks/pos/task/construction/dev/adj_dev.txt'
# path_to_noun = '/Data/tasks_quantized_scores/similarity_tasks/pos/task/construction/dev/noun_dev.txt'
# path_to_verb = '/Data/tasks_quantized_scores/similarity_tasks/pos/task/construction/dev/verb_dev.txt'
# path_to_librispeech_text = '/Data/models/topline_word_smallbert/construction/quantized/train_text_librispeech.txt'
# path_to_phoneme_adj = '/Data/tasks_quantized_scores/similarity_tasks/pos/task/construction/dev/phoneme_adj_dev.txt'
# path_to_phoneme_noun = '/Data/tasks_quantized_scores/similarity_tasks/pos/task/construction/dev/phoneme_noun_dev.txt'
# path_to_phoneme_verb = '/Data/tasks_quantized_scores/similarity_tasks/pos/task/construction/dev/phoneme_verb_dev.txt'
# path_save_task = '/Data/tasks_quantized_scores/similarity_tasks/pos/task/pos_dev.txt'
# freq_sim = 1.5
# len_sim = 0
# edit_sim = 0
# num_produced = 5000

# create_pos_task(path_to_adj,
#                 path_to_noun,
#                 path_to_verb,
#                 path_to_librispeech_text,
#                 path_to_phoneme_adj,
#                 path_to_phoneme_noun,
#                 path_to_phoneme_verb,
#                 path_save_task,
#                 freq_sim,
#                 len_sim,
#                 edit_sim,
#                 num_produced)


# path_to_adj = '/Data/tasks_quantized_scores/similarity_tasks/pos/task/construction/test/adj_test.txt'
# path_to_noun = '/Data/tasks_quantized_scores/similarity_tasks/pos/task/construction/test/noun_test.txt'
# path_to_verb = '/Data/tasks_quantized_scores/similarity_tasks/pos/task/construction/test/verb_test.txt'
# path_to_librispeech_text = '/Data/models/topline_word_smallbert/construction/quantized/train_text_librispeech.txt'
# path_to_phoneme_adj = '/Data/tasks_quantized_scores/similarity_tasks/pos/task/construction/test/phoneme_adj_test.txt'
# path_to_phoneme_noun = '/Data/tasks_quantized_scores/similarity_tasks/pos/task/construction/test/phoneme_noun_test.txt'
# path_to_phoneme_verb = '/Data/tasks_quantized_scores/similarity_tasks/pos/task/construction/test/phoneme_verb_test.txt'
# path_save_task = '/Data/tasks_quantized_scores/similarity_tasks/pos/task/pos_test.txt'
# freq_sim = 1.5
# len_sim = 0
# edit_sim = 0
# num_produced = 5000

# create_pos_task(path_to_adj,
#                 path_to_noun,
#                 path_to_verb,
#                 path_to_librispeech_text,
#                 path_to_phoneme_adj,
#                 path_to_phoneme_noun,
#                 path_to_phoneme_verb,
#                 path_save_task,
#                 freq_sim,
#                 len_sim,
#                 edit_sim,
#                 num_produced)




