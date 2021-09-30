import random


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


def create_pos_sent_task(path_to_adj,
                         path_to_noun,
                         path_to_verb,
                         path_to_librispeech_text,
                         path_save_task,
                         num_block_produced,
                         easy_mode):
    
    with open(path_to_librispeech_text) as f:
        text_librispeech = f.read()
        txt_libri_lines = text_librispeech.split('\n')
        text_librispeech_split = text_librispeech.replace('\n', ' ').split(' ')
    freq_libri = {}
    for word in text_librispeech_split:
        if word in freq_libri:
            freq_libri[word] += 1
        else:
            freq_libri[word] = 1
            
    if not easy_mode:
        def two_words_in_Libri(word_1, word_2):
            in_Libri = False
            for line in txt_libri_lines:
                if (word_1 in line) and (word_2 in line):
                    in_Libri = True
                    break
            return in_Libri
    
    else:
        def two_words_in_Libri(word_1, word_2):
            in_Libri = False
            full_txt_libri =  ' '.join(txt_libri_lines)
            if (word_1 + ' ' + word_2 in full_txt_libri):
                in_Libri = True
            return in_Libri
    
    adj_list = [el for el in txt_to_list(path_to_adj) if el in freq_libri]
    noun_list = [el for el in txt_to_list(path_to_noun) if el in freq_libri]
    verb_list = [el for el in txt_to_list(path_to_verb) if el in freq_libri]
    
    n_block_produced = 0
    previous_sent = set()
    to_write = ''
    
    while n_block_produced < num_block_produced:
        
        adj = random.choice(adj_list)
        noun_1 = random.choice(noun_list)
        noun_2 = random.choice(noun_list)
        verb = random.choice(verb_list)
        
        if noun_1 != noun_2:
            if adj+noun_2+adj+verb not in previous_sent:
                if noun_1+verb+noun_1+noun_2 not in previous_sent:
                    if not two_words_in_Libri(adj, noun_2):
                        if not two_words_in_Libri(adj, verb):
                            if not two_words_in_Libri(noun_1, verb):
                                if not two_words_in_Libri(noun_1, noun_2):
                                    
                                    code = 'pos_sent_easy_dev_' + str(n_block_produced) + '_'
                                    to_write += code+'r1,' + code+'w1,' + ' '.join(['the', adj, noun_2]) + ',' + ' '.join(['the', adj, verb]) + '\n'
                                    to_write += code+'r2,' + code+'w2,' + ' '.join(['the', noun_1, verb]) + ',' + ' '.join(['the', noun_1, noun_2]) + '\n'
                                    
                                    n_block_produced += 1
                                    
                                    previous_sent.add(adj+noun_2+adj+verb)
                                    previous_sent.add(noun_1+verb+noun_1+noun_2)
        
        if n_block_produced % 10 == 0:
            print("Number of blocks produced:", n_block_produced)
            
    write(path_save_task, to_write)
    




# path_to_adj = '/Data/tasks_quantized_scores/score_tasks/pos_sent/task/construction/dev/adj_dev.txt'
# path_to_noun = '/Data/tasks_quantized_scores/score_tasks/pos_sent/task/construction/dev/noun_dev.txt'
# path_to_verb = '/Data/tasks_quantized_scores/score_tasks/pos_sent/task/construction/dev/verb_dev.txt'
# path_to_librispeech_text = '/Data/models/topline_word_smallbert/construction/quantized/train_text_librispeech.txt'
# path_save_task = '/Data/tasks_quantized_scores/score_tasks/pos_sent/task/pos_sent_dev.txt'
# num_block_produced = 500
# easy_mode = False

# create_pos_sent_task(path_to_adj,
#                      path_to_noun,
#                      path_to_verb,
#                      path_to_librispeech_text,
#                      path_save_task,
#                      num_block_produced,
#                      easy_mode)


# path_to_adj = '/Data/tasks_quantized_scores/score_tasks/pos_sent/task/construction/test/adj_test.txt'
# path_to_noun = '/Data/tasks_quantized_scores/score_tasks/pos_sent/task/construction/test/noun_test.txt'
# path_to_verb = '/Data/tasks_quantized_scores/score_tasks/pos_sent/task/construction/test/verb_test.txt'
# path_to_librispeech_text = '/Data/models/topline_word_smallbert/construction/quantized/train_text_librispeech.txt'
# path_save_task = '/Data/tasks_quantized_scores/score_tasks/pos_sent/task/pos_sent_test.txt'
# num_block_produced = 500
# easy_mode = False

# create_pos_sent_task(path_to_adj,
#                      path_to_noun,
#                      path_to_verb,
#                      path_to_librispeech_text,
#                      path_save_task,
#                      num_block_produced,
#                      easy_mode)









# path_to_adj = '/Data/tasks_quantized_scores/score_tasks/pos_sent/task/construction/dev/adj_dev.txt'
# path_to_noun = '/Data/tasks_quantized_scores/score_tasks/pos_sent/task/construction/dev/noun_dev.txt'
# path_to_verb = '/Data/tasks_quantized_scores/score_tasks/pos_sent/task/construction/dev/verb_dev.txt'
# path_to_librispeech_text = '/Data/models/topline_word_smallbert/construction/quantized/train_text_librispeech.txt'
# path_save_task = '/Data/tasks_quantized_scores/score_tasks/pos_sent_easy/task/pos_sent_easy_dev.txt'
# num_block_produced = 500
# easy_mode = True

# create_pos_sent_task(path_to_adj,
#                      path_to_noun,
#                      path_to_verb,
#                      path_to_librispeech_text,
#                      path_save_task,
#                      num_block_produced,
#                      easy_mode)


# path_to_adj = '/Data/tasks_quantized_scores/score_tasks/pos_sent/task/construction/test/adj_test.txt'
# path_to_noun = '/Data/tasks_quantized_scores/score_tasks/pos_sent/task/construction/test/noun_test.txt'
# path_to_verb = '/Data/tasks_quantized_scores/score_tasks/pos_sent/task/construction/test/verb_test.txt'
# path_to_librispeech_text = '/Data/models/topline_word_smallbert/construction/quantized/train_text_librispeech.txt'
# path_save_task = '/Data/tasks_quantized_scores/score_tasks/pos_sent_easy/task/pos_sent_easy_test.txt'
# num_block_produced = 500
# easy_mode = True

# create_pos_sent_task(path_to_adj,
#                      path_to_noun,
#                      path_to_verb,
#                      path_to_librispeech_text,
#                      path_save_task,
#                      num_block_produced,
#                      easy_mode)





