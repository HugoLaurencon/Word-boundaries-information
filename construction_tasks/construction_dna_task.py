from random import choice, sample


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


def create_dna_task(path_to_nouns,
                    path_to_det_sing,
                    path_to_det_plur,
                    path_to_adj,
                    path_to_librispeech_txt,
                    path_dir_save_task,
                    with_adj = True):
    
    nouns = open_file(path_to_nouns)
    
    det_sing = open_file(path_to_det_sing)
    det_plur = open_file(path_to_det_plur)
    
    adjs = open_file(path_to_adj)
    
    f = open(path_to_librispeech_text, 'r')
    libri_txt = f.read()
    f.close()
    
    blocks = []
    
    if with_adj:
        # Dna task with an adjective between the determinant and the noun
        assert len(det_sing) == len(det_plur)
        
        for noun in nouns:
            for det_s, det_p in zip(det_sing, det_plur):
                #for adj in adjs:
                for adj in sample(adjs, 3):
                    r1 = det_s + ' ' + adj + ' ' + noun
                    w1 = det_p + ' ' + adj + ' ' + noun
                    r2 = det_p + ' ' + adj + ' ' + noun + 's'
                    w2 = det_s + ' ' + adj + ' ' + noun + 's'
                    
                    pair1 = r1 + ',' + w1
                    pair2 = r2 + ',' + w2
                    pair3 = r1 + ',' + w2
                    pair4 = r2 + ',' + w1
                    
                    blocks.append([pair1, pair2, pair3, pair4])
    
    else:
        # Dna task without the adjective
        for noun in nouns:
            valid_det_sing = [False] * len(det_sing)
            valid_det_plur = [False] * len(det_plur)
            
            for i, det_s in enumerate(det_sing):
                if (det_s + ' ' + noun not in libri_txt):
                    valid_det_sing[i] = True
            for i, det_p in enumerate(det_plur):
                if (det_p + ' ' + noun + 's' not in libri_txt):
                    valid_det_plur[i] = True
            
            if any(valid_det_sing) and any(valid_det_plur):
                valid_det_sing = [el for i, el in enumerate(det_sing) if valid_det_sing[i]]
                valid_det_plur = [el for i, el in enumerate(det_plur) if valid_det_plur[i]]
                
                det_s = choice(valid_det_sing)
                det_p = choice(valid_det_plur)
                
                r1 = det_s + ' ' + noun
                w1 = det_p + ' ' + noun
                r2 = det_p + ' ' + noun + 's'
                w2 = det_s + ' ' + noun + 's'
                
                pair1 = r1 + ',' + w1
                pair2 = r2 + ',' + w2
                pair3 = r1 + ',' + w2
                pair4 = r2 + ',' + w1
                
                blocks.append([pair1, pair2, pair3, pair4])
        
    blocks_dev = blocks[:len(blocks)//2]
    blocks_test = blocks[len(blocks)//2:]
    
    to_write_dev = ''
    to_write_test = ''
    
    for i in range(len(blocks_dev)):
        block_id = 'dna_dev_' + str(i)
        blocks_dev[i][0] = block_id + '_r1,' + block_id + '_w1,' + blocks_dev[i][0]
        blocks_dev[i][1] = block_id + '_r2,' + block_id + '_w2,' + blocks_dev[i][1]
        blocks_dev[i][2] = block_id + '_r1,' + block_id + '_w2,' + blocks_dev[i][2]
        blocks_dev[i][3] = block_id + '_r2,' + block_id + '_w1,' + blocks_dev[i][3]
        to_write_dev += '\n'.join(blocks_dev[i]) + '\n'
        
    for i in range(len(blocks_test)):
        block_id = 'dna_test_' + str(i)
        blocks_test[i][0] = block_id + '_r1,' + block_id + '_w1,' + blocks_test[i][0]
        blocks_test[i][1] = block_id + '_r2,' + block_id + '_w2,' + blocks_test[i][1]
        blocks_test[i][2] = block_id + '_r1,' + block_id + '_w2,' + blocks_test[i][2]
        blocks_test[i][3] = block_id + '_r2,' + block_id + '_w1,' + blocks_test[i][3]
        to_write_test += '\n'.join(blocks_test[i]) + '\n'
    
    write_file(path_dir_save_task + 'dna_dev' + '.txt', to_write_dev)
    write_file(path_dir_save_task + 'dna_test' + '.txt', to_write_test)
    



# path_to_nouns = '/Data/tasks_quantized_scores/score_tasks/dna/task/construction/nouns.txt'
# path_to_det_sing = '/Data/tasks_quantized_scores/score_tasks/dna/task/construction/det_sing.txt'
# path_to_det_plur = '/Data/tasks_quantized_scores/score_tasks/dna/task/construction/det_plur.txt'
# path_to_adj = '/Data/tasks_quantized_scores/score_tasks/dna/task/construction/adj.txt'
# path_to_librispeech_text = '/Data/models/topline_word_smallbert/construction/quantized/train_text_librispeech.txt'
# path_dir_save_task = '/Stage_CoML/Data/tasks_quantized_scores/score_tasks/dna/task/'
# with_adj = True
# create_dna_task(path_to_nouns, path_to_det_sing, path_to_det_plur, path_to_adj, path_to_librispeech_text, path_dir_save_task, with_adj)













