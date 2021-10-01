# Word-boundaries-information
The goal of this project is to measure the impact of word boundary knowledge for machine learning models in NLP, in order to then transpose this study to speech models.

# Dependencies

Several repositories are required to use this one.

## Fairseq

We use a slightly modified version of fairseq. The only modifications are a registration of a small roberta architecture in the file ```fairseq/fairseq/models/roberta/model.py```, and the addition of the files ```wwm_phoneme.py``` and ```wwm_phoneme_plus_word.py```, which are only used for the whole word masking training, to the directory ```fairseq/fairseq/data/encoders/```.

```bash
git clone https://github.com/HugoLaurencon/fairseq.git
```

## Baseline Zero Speech 2021

Compared to the original version of the code for the baseline of the Zero Speech Challenge 2021, we added the files ```compute_proba_BERT_exact_masking.py``` and ```compute_score_BERT.py``` to the directory ```zerospeech2021_baseline/scripts/```, and the files ```lm_scoring_exact_masking.py``` and ```lm_score_BERT.py``` to the directory ```zerospeech2021_baseline/scripts/utils/```, which are useful for the evaluation of the models on score tasks.

```bash
git clone https://github.com/HugoLaurencon/zerospeech2021_baseline.git
```

Do not forget to download the checkpoints and place them in the main directory ```zerospeech2021_baseline/```.

```bash
curl https://download.zerospeech.com/2021/baseline_checkpoints.tar.gz | tar xz
```

## CPC audio

The repository CPC_audio is required to create the quantized for audio files for the model CPC+kmeans+BERT.

```bash
git clone https://github.com/HugoLaurencon/CPC_audio.git
```

One simply needs to move the directory ```CPC_audio/cpc/``` to ```zerospeech2021_baseline/scripts/```, but executing the above command should not be necessary since this is already done in the forked version of ```zerospeech2021_baseline```.



# Organization of this repository

This repository contains the code used to create the different tasks and evaluate the models on them.

For almost every file, some commented lines at the end show examples of how functions were called.

A folder containing the checkpoints for every model, the files necessary for the construction of the tasks, the quantized and the scores for every task and model, will be released soon.



# Construction of the tasks

## Types of tasks and formats

The are two types of tasks, the similarity tasks and the score tasks.

### Similarity tasks

The similarity tasks consist of ABX tests stored in a ```.txt``` file, where each line represents a different test.

On each line, a certain number of words, each separated by a space, are written.

The first word corresponds to the word A, the second word to the word X, and all the following words to potential word B for the ABX test.

The text is always written in lowercase letters.

### Score tasks

The scores tasks consist of comparision of pairs including a correct sentence and an incorrect one.

The task is stored in a ```.txt``` file, where each line represents a different pair.

Each line is written in the format ```code_correct_sentence,code_incorrect_sentence,correct_sentence,incorrect_sentence```, where the code is unique for a sentence, correct or incorrect, and allows to identify it.

Pairs are organized by blocks such that they are balanced, which means that it is not possible to find a biais to obtain a better score than random within a block.
The text is always written in lowercase letters.



## Construction

The scripts used to construct the different tasks are in the directory ```Word-boundaries-information/construction_tasks/```.

Note that some scripts are made with random choices inside them, so running twice the same script will produce two different outputs.



# Evaluation of models on tasks

## Creation of quantized

To evaluate the different models on the tasks, the first step is to compute the quantized tasks, which are the inputs given to the language models (LM).

The format of the quantized will always be ```code  token_1,token_2,token_3,...```, where the code is unique and allows to identify a test, the code is separated from the tokens by a tabulation, and tokens are separated with each other by a comma.

For the same task, the quantized will be different depending on the model we consider. We can distinguish two main categories, speech models and text models.

### Creation of quantized for speech models

#### Google Text-to-Speech API

Speech models, like the CPC+kmeans+BERT model, take as input audio files instead of text, so we first need to convert the task in a text format into an audio format. For this aim, we use the Google Text-to-Speech API. All the audios in this study were generated with the trial version of the API.

The way to setup everything and get a key for the API is explained on [this tutorial](https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries).

Once this is done, one can use the script ```Word-boundaries-information/text_to_speech/text_to_speech.py``` to start generating wav files corresponding to the words or sentences of the tests of the given task.

Each word (for the similarity tasks) or sentence (for the score tasks) corresponding to a test of a task will be generated by 4 different speakers, using the codes ```en-US-Wavenet-A```, ```en-US-Wavenet-C```, ```en-US-Wavenet-H``` and ```en-US-Wavenet-J```. Therefore, for the same task, there will be four times more quantized for speech models than for text models. The codes used for the reference of a test will remain the same, but are appended by ```_A```, ```_C```,```_H``` or ```_J``` for the speech models.


#### Get quantized

Once the audio files are generated, we can start computing the quantized by applying the CPC+kmeans model on them with the following command:

```bash
python zerospeech2021_baseline/scripts/quantize_audio.py \
    zerospeech2021_baseline/checkpoints/CPC-big-kmeans50/clustering_kmeans50/clustering_CPC_big_kmeans50.pt \
    ../audio_files/ \
    ../quantized_audio_files/ \
    --file_extension wav
```

and the quantized units will be written in the ```quantized_outputs.txt``` file in the output directory.


### Creation of quantized for text models

The creation of quantized for text models is done with the jupyter notebook file ```Word-boundaries-information/get_quantized/get_quantized.ipynb```.

It can be ideally opened with Google Colab, which makes it very easy to install all the dependencies written at the beginning of the file.

In this notebook, there are different sections corresponding to the different models as well as examples of commands we used to obtain the quantized.

Make sure to run each cell of the notebook first, because some functions used to obtain quantized for a certain model are often reused in functions to obtain quantized for other models.


### Creation of quantized for the training of text models

The file ```Word-boundaries-information/get_quantized/get_quantized.ipynb``` is used to generate quantized for tasks for text models, but it can also be used to generate quantized for the training of text models, which are basically the train, dev, ant test sets of the corpus of LibriSpeech in the format of the text model considered (for example, sequences of phonemes with no boundaries between the words for the phone nobound model).

This can be easily done with a small hack of transforming the text corpus of LibriSpeech into the format of a score task, where each line contains two random codes and two sentences of Librispeech. We can then compute the quantized and remove the codes to obtain the results used to train a model.

The format of inputs for training text models is ```.txt``` files organized by lines, where on each line tokens are separated by a space.

Then, the first thing is to do is to preprocess this data with the following command:

```bash
fairseq-preprocess --only-source \
    --trainpref ../quantized/quantized_train.txt \
    --validpref ../quantized/quantizd_dev.txt \
    --testpref ../quantized/quantized_test.txt \
    --destdir ../data-bin \
    --workers 20
```

and finally the training is done with the following command (hyperparameters may vary regarding the model considered):

```bash
fairseq-train --fp16 /data-bin \
    --task masked_lm --criterion masked_lm \
    --save-dir /checkpoints \
    --keep-last-epochs 1 \
    --num-workers 1 \
    --arch roberta_small \
    --optimizer adam --adam-betas '(0.9, 0.98)' --adam-eps 1e-06 --clip-norm 0.0 \
    --lr-scheduler polynomial_decay --lr 0.0005 --total-num-update 150000 --warmup-updates 15000 \
    --dropout 0.1 --attention-dropout 0.1 --weight-decay 0.01 \
    --sample-break-mode eos --tokens-per-sample 110 --max-positions 110 \
    --batch-size 16  --update-freq 16 --max-update 150000 \
    --log-format simple --log-interval 1 --skip-invalid-size-inputs-valid-test
```

where ```--update-freq``` should be equal to ```128/n``` with ```n``` the number of GPU (we used 8 GPU), ```--tokens-per-sample``` and ```--max-positions``` should be almost equal to the maximum number of tokens occurring in a sentence of the training set, ```--total-num-update``` and ```--max-update``` is ```150000``` for the phoneme models and ```50000``` for the word model, ```--warmup-updates``` is  ```--total-num-update/10```.

On this notebook ```Word-boundaries-information/get_quantized/get_quantized.ipynb```, there are also the codes used to train the different tokenizers for BPE models, and to obtain the different encodings for onehot and dp parse models. 



## Evaluations

### Evaluations of similarity tasks

simi puis script


### Evaluations of score tasks

scores puis script
