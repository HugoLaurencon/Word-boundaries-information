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

The file ```Word-boundaries-information/get_quantized/get_quantized.ipynb``` is a jupyter notebook file, and can be ideally opened with Google Colab, which makes it very easy to install all the dependencies.

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

Each word or sentence corresponding to a test of a task will be generated by 4 different speakers, using the codes ```en-US-Wavenet-A```, ```en-US-Wavenet-C```, ```en-US-Wavenet-H```, ```en-US-Wavenet-J```. Therefore, for the same task, there will be four times more quantized for speech models than for text models. The codes used for the reference of a test will remain the same, but is appended by ```_A```, ```_C```,```_H``` or ```_J``` for the speech models.




