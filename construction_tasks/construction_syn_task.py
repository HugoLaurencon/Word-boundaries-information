import spacy
import copy
import numpy as np
from Levenshtein import distance as dist


def cstr_syn_dic(path_to_pairs, nmax_word, path_to_librispeech_text, nmin_freq):
    """
    Applies the following constraints for the pairs:
        -the dictionnary cannot contain two identical pairs,
        -the same word cannot be present more than nmax_word times in the dic,
        -both words of a pair have to be present in the librispeech dataset,
        -both words of a pair have to have the same POS,
        -both words of a pair have to have a number of occurences of at least
         nmin_freq in the librispeech dataset.
    Returns a list of the pairs that does not satisfy all of these conditions
    """
    
    pairs = []
    dic_pairs = {}
    dic_words = {}
    
    for path in path_to_pairs:
        pairs_path = []
        with open(path) as f:
            for line in f:
                line = line.replace('\n', '').split(' ')
                pairs_path.append(line)
                if line[0] + '_' + line[1] in dic_pairs:
                    dic_pairs[line[0] + ' ' + line[1]] += 1
                    dic_pairs[line[1] + ' ' + line[0]] += 1
                else:
                    dic_pairs[line[0] + ' ' + line[1]] = 1
                    dic_pairs[line[1] + ' ' + line[0]] = 1
                if line[0] in dic_words:
                    dic_words[line[0]] += 1
                else:
                    dic_words[line[0]] = 1
                if line[1] in dic_words:
                    dic_words[line[1]] += 1
                else:
                    dic_words[line[1]] = 1
        pairs.append(pairs_path)
    
    freq_libri = {}
    with open(path_to_librispeech_text) as f:
        text_librispeech = f.read()
        text_librispeech_split = text_librispeech.replace('\n', ' ').split(' ')
    for word in text_librispeech_split:
        if word in freq_libri:
            freq_libri[word] += 1
        else:
            freq_libri[word] = 1
            
    wrong_pairs = []
    nlp = spacy.load('en_core_web_sm')
    for pair in dic_pairs:
        
        if dic_pairs[pair] > 1:
            wrong_pairs.append(pair)
            
        words = pair.split(' ')
        if dic_words[words[0]] > nmax_word:
            wrong_pairs.append(pair)
        elif dic_words[words[1]] > nmax_word:
            wrong_pairs.append(pair)
            
        if words[0] not in freq_libri:
            wrong_pairs.append(pair)
        elif words[1] not in freq_libri:
            wrong_pairs.append(pair)
        else:
            if freq_libri[words[0]] < nmin_freq:
                wrong_pairs.append(pair)
            elif freq_libri[words[1]] < nmin_freq:
                wrong_pairs.append(pair)
            
        # NOTE: If pairs are appended to wrong_pairs because of the following
        # test, it does not mean that it is necessary wrong and it should
        # be checked by hand. The same word can be a verb and an adjective for
        # example.
        # doc0, doc1 = nlp(words[0]), nlp(words[1])
        # pos0, pos1 = [tok for tok in doc0][0].pos_, [tok for tok in doc1][0].pos_
        # if pos0 != pos1:
        #     wrong_pairs.append(pair)
    
    print('{:}/{:} pairs satisfy every condition.' \
          .format(len(dic_pairs)//2 - len(wrong_pairs)//2, len(dic_pairs)//2))
    
    return wrong_pairs


def reorder_pairs_by_meaning(path_to_pairs,
                             path_save):
    for i in range(len(path_to_pairs)):
        
        pairs = []
        dic_cl_eq = {} # Classe d'equivalence pour le sens des mots
        
        with open(path_to_pairs[i]) as f:
            for line in f:
                line = line.replace('\n', '').split(' ')
                pairs.append(line)
                if line[0] in dic_cl_eq:
                    dic_cl_eq[line[0]].add(line[1])
                else:
                    dic_cl_eq[line[0]] = {line[1]}
                if line[1] in dic_cl_eq:
                    dic_cl_eq[line[1]].add(line[0])
                else:
                    dic_cl_eq[line[1]] = {line[0]}
        
        dic_cl_eq_prev = {}
        while dic_cl_eq_prev != dic_cl_eq:
            dic_cl_eq_prev = copy.deepcopy(dic_cl_eq)
            for word in dic_cl_eq:
                for syn in dic_cl_eq[word]:
                    dic_cl_eq[word] = set.union(dic_cl_eq[word], dic_cl_eq[syn])
                    
        groups_meaning = []
        for group in dic_cl_eq.values():
            if group not in groups_meaning:
                groups_meaning.append(group)
        #groups_meaning = list(set(dic_cl_eq.values()))
        pairs_meaning = [[] for group in groups_meaning]
        for pair in pairs:
            for j in range(len(groups_meaning)):
                if pair[0] in groups_meaning[j]:
                    pairs_meaning[j].append(pair)
                    break
            
        file = open(path_save[i], 'w+')
        file.truncate(0)
        for group in pairs_meaning:
            for pair in group:
                file.write(' '.join(pair) + '\n')
        file.close()
    
    
def create_B_words(path_to_pairs,
                   path_to_librispeech_text,
                   path_to_phonemes,
                   path_save,
                   freq_sim,
                   len_sim,
                   edit_sim):
    """
    Creates some B words for every pair, with the following constraints
    regarding a B word:
        -it cannot be identical to a word already in the pair, or have
         the same meaning of it,
        -it has to have the same POS as both words of the pair,
        -it has to have a frequency in LibriSpeech fb such that it verifies
         abs(log(fb)/log(freq_sim) - log(fa)/log(freq_sim)) <= 1 with fa the
         frequency of the word A in LibriSpeech. It is equivalent to say
         that fb is no greater than fa * freq_sim or lower than fa / freq_sim,
        -it has to have a length between (1-len_sim)*len_a and (1+len_sim)*len_a
         with len_a the length of the word A,
        -it has to verify abs(d(X,A)-d(X,B)) < edit_sim, with d the
         Levenshtein distance between phonemes.
    """
    for i in range(len(path_to_pairs)):
        
        pairs = []
        dic_cl_eq = {} # Classe d'equivalence pour le sens des mots
        
        with open(path_to_pairs[i]) as f:
            for line in f:
                line = line.replace('\n', '').split(' ')
                pairs.append(line)
                if line[0] in dic_cl_eq:
                    dic_cl_eq[line[0]].add(line[1])
                else:
                    dic_cl_eq[line[0]] = {line[1]}
                if line[1] in dic_cl_eq:
                    dic_cl_eq[line[1]].add(line[0])
                else:
                    dic_cl_eq[line[1]] = {line[0]}
        
        dic_cl_eq_prev = {}
        while dic_cl_eq_prev != dic_cl_eq:
            dic_cl_eq_prev = copy.deepcopy(dic_cl_eq)
            for word in dic_cl_eq:
                for syn in dic_cl_eq[word]:
                    dic_cl_eq[word] = set.union(dic_cl_eq[word], dic_cl_eq[syn])
        
        with open(path_to_librispeech_text) as f:
            text_librispeech = f.read()
            text_librispeech_split = text_librispeech.replace('\n', ' ').split(' ')
        freq_libri = {}
        for word in text_librispeech_split:
            if word in dic_cl_eq:
                if word in freq_libri:
                    freq_libri[word] += 1
                else:
                    freq_libri[word] = 1
                    
        phonemes = []
        with open(path_to_phonemes[i]) as f:
            for line in f:
                line = line.replace('\n', '').split(' ')
                phonemes.append(line)
                
        dic_word_phonemes = {}
        for j in range(len(pairs)):
            dic_word_phonemes[pairs[j][0]] = phonemes[j][0]
            dic_word_phonemes[pairs[j][1]] = phonemes[j][1]
        
        file = open(path_save[i], 'w+')
        file.truncate(0)
        
        for j in range(len(pairs)):
            A, X = pairs[j]
            B_0 = []
            for word in dic_cl_eq:
                if word not in dic_cl_eq[A]:
                    if np.abs(np.log(freq_libri[word])/np.log(freq_sim) \
                              - np.log(freq_libri[A])/np.log(freq_sim)) <= 1:
                        if (len(word) > (1-len_sim)*len(A)) and \
                            (len(word) < (1+len_sim)*len(A)):
                                p_A = dic_word_phonemes[A]
                                p_X = dic_word_phonemes[X]
                                p_word = dic_word_phonemes[word]
                                if np.abs(dist(p_A, p_X) - dist(p_X, p_word)) < edit_sim:
                                    B_0.append(word)
            line_0 = ' '.join([A, X] + B_0)
            
            X, A = pairs[j]
            B_1 = []
            for word in dic_cl_eq:
                if word not in dic_cl_eq[A]:
                    if np.abs(np.log(freq_libri[word])/np.log(freq_sim) \
                              - np.log(freq_libri[A])/np.log(freq_sim)) <= 1:
                        if (len(word) > np.around((1-len_sim)*len(A), decimals=2)) and \
                            (len(word) < np.around((1+len_sim)*len(A), decimals=2)):
                                p_A = dic_word_phonemes[A]
                                p_X = dic_word_phonemes[X]
                                p_word = dic_word_phonemes[word]
                                if np.abs(dist(p_A, p_X) - dist(p_X, p_word)) < edit_sim:
                                    B_1.append(word)
            line_1 = ' '.join([A, X] + B_1)
            
            if max(len(B_0), len(B_1)) == 0:
                print(X, A)
                
            line = line_0 if len(line_0) > len(line_1) else line_1
            if j < len(pairs) - 1:
                line += '\n'
            file.write(line)
        
        file.close()
    


# path_to_pairs = ['/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/dev_adjs_nouns_verbs/dev_adj.txt',
#                  '/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/dev_adjs_nouns_verbs/dev_noun.txt',
#                  '/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/dev_adjs_nouns_verbs/dev_verb.txt']
# path_to_librispeech_text = '/Data/models/topline_word_smallbert/construction/quantized/train_text_librispeech.txt'
# path_to_phonemes = ['/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/dev_adjs_nouns_verbs/dev_adj_phonemes_processed.txt',
#                     '/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/dev_adjs_nouns_verbs/dev_noun_phonemes_processed.txt',
#                     '/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/dev_adjs_nouns_verbs/dev_verb_phonemes_processed.txt']
# path_save = ['/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/dev_adjs_nouns_verbs/dev_full_adj.txt',
#              '/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/dev_adjs_nouns_verbs/dev_full_noun.txt',
#              '/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/dev_adjs_nouns_verbs/dev_full_verb.txt']
# freq_sim = 2
# len_sim = 1/3
# edit_sim = 1
# create_B_words(path_to_pairs,
#                path_to_librispeech_text,
#                path_to_phonemes,
#                path_save,
#                freq_sim,
#                len_sim,
#                edit_sim)


# path_to_pairs = ['/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/test_adjs_nouns_verbs/test_adj.txt',
#                  '/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/test_adjs_nouns_verbs/test_noun.txt',
#                  '/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/test_adjs_nouns_verbs/test_verb.txt']
# path_to_librispeech_text = '/Data/models/topline_word_smallbert/construction/quantized/train_text_librispeech.txt'
# path_to_phonemes = ['/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/test_adjs_nouns_verbs/test_adj_phonemes_processed.txt',
#                     '/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/test_adjs_nouns_verbs/test_noun_phonemes_processed.txt',
#                     '/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/test_adjs_nouns_verbs/test_verb_phonemes_processed.txt']
# path_save = ['/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/test_adjs_nouns_verbs/test_full_adj.txt',
#              '/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/test_adjs_nouns_verbs/test_full_noun.txt',
#              '/Data/tasks_quantized_scores/similarity_tasks/syn/task/construction/test_adjs_nouns_verbs/test_full_verb.txt']
# freq_sim = 2
# len_sim = 1/3
# edit_sim = 1
# create_B_words(path_to_pairs,
#                path_to_librispeech_text,
#                path_to_phonemes,
#                path_save,
#                freq_sim,
#                len_sim,
#                edit_sim)





