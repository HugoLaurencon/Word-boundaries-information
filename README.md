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

We added the files ```compute_proba_BERT_exact_masking.py``` and ```compute_score_BERT.py``` to the directory ```zerospeech2021_baseline/scripts/```, and the files ```lm_scoring_exact_masking.py``` and ```lm_score_BERT.py``` to the directory ```zerospeech2021_baseline/scripts/utils/```, which are useful for the evaluation of the models on score tasks.

```bash
git clone https://github.com/HugoLaurencon/zerospeech2021_baseline.git
```

Do not forget to download the checkpoints and place them in the main directory ```zerospeech2021_baseline/```.

```bash
curl https://download.zerospeech.com/2021/baseline_checkpoints.tar.gz | tar xz
```

## CPC audio







