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

For almost every file, some commented lines at the end show examples of how functions were called to obtained what we have.

The file ```Word-boundaries-information/get_quantized/get_quantized.ipynb``` is a jupyter notebook file, and can be ideally opened with Google Colab, which makes it very easy to install all the dependencies.

A folder containing the checkpoints for every model, the files necessary for the construction of the tasks, the quantized and the scores for every task and model, will be released soon.




