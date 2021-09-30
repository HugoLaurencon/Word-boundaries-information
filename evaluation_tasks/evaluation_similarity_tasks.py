import numpy as np


def open_file(path_to_txt):
    f = open(path_to_txt, 'r')
    txt = [el for el in f.read().split('\n') if el != '']
    f.close()
    return txt


def load_feature(paths_to_features, pooling):
     
        features = [list(map(float, el.split(' '))) for path in paths_to_features
                    for el in open_file(path)]
        features = np.array(features)
        
        if pooling == 'max':
            return np.amax(features, axis=0)
        elif pooling == 'mean':
            return np.mean(features, axis=0)
        else:
            raise ValueError('Please specify a pooling between max and mean.')


def evaluate_similarity_task(path_to_similarity_task,
                             paths_to_dir_features,
                             pooling,
                             cpc_km_bert = False):
                
    task = open_file(path_to_similarity_task)
    task = [el.split(' ') for el in task]
        
    voices_code = ['']
    if cpc_km_bert:
        voices_code = ['_A', '_C', '_H', '_J']
    
    scores_tot = []
    for test in task:
        scores_test = []
        for voice_code in voices_code:
            
            paths_to_features_A = [el + test[0] + voice_code + '.txt' for el in paths_to_dir_features]
            A = load_feature(paths_to_features_A, pooling)
            
            paths_to_features_X = [el + test[1] + voice_code + '.txt' for el in paths_to_dir_features]
            X = load_feature(paths_to_features_X, pooling)
            
            simi_A_X = np.dot(A, X) / (np.linalg.norm(A) * np.linalg.norm(X))
            
            for i in range(2, len(test)):
                
                paths_to_features_B = [el + test[i] + voice_code + '.txt' for el in paths_to_dir_features]
                B = load_feature(paths_to_features_B, pooling)
                
                simi_B_X = np.dot(B, X) / (np.linalg.norm(B) * np.linalg.norm(X))
                
                if simi_A_X > simi_B_X:
                    scores_test.append(1)
                else:
                    scores_test.append(0)
                    
        scores_test = np.mean(scores_test)
        scores_tot.append(scores_test)
        
    scores_tot = 100 * np.mean(scores_tot)
    print(f'The average score for these features and pooling for this task is {scores_tot:.1f}.')



# path_to_similarity_task = '/scratch2/hlaurencon/data/syn/syn_test.txt'
# paths_to_dir_features = ['/scratch2/hlaurencon/data/topline_phoneme_libri/no_boundaries_onehot_bpe/no_boundaries_onehot_bpe_1000/syn/layer' + str(i) + '/' for i in range(0, 9)]
# pooling = 'mean'
# cpc_km_bert = True # It should be False for the quantized generated with the current get_quantized.py script
# evaluate_similarity_task(path_to_similarity_task, paths_to_dir_features, pooling, cpc_km_bert)





