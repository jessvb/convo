# Rasa
Rasa is an open-source conversational AI framework for building context assistants. Rasa includes [Rasa Core](https://rasa.com/docs/rasa/core/about/) which handles their logic and conversation manager and [Rasa NLU](https://rasa.com/docs/rasa/nlu/about/) which does user intent recognition and entity extraction.

Because Convo will be handling the logic and conversation tracking and managing, only the Rasa NLU is needed in our case. The Rasa NLU trains a model (whether from scratch or on top of a pre-trained model like BERT) given training examples that we define. The model is hosted on a Python server where you input text using REST API and the model outputs intent and possible detected entities.

## Installation
Install Rasa using their [guide](https://rasa.com/docs/rasa/user-guide/installation/). On the guide, you have to option to install spacCy and MITIE but it's not necessary. 

## Introduction
The Rasa installation comes with a series of CLI (command-line interface) commands that you can use. You can view all the commands [here](https://rasa.com/docs/rasa/user-guide/command-line-interface/). We will use CLI commands to get Rasa up, so Convo can use it.

To initialize a Rasa project, you can run
```bash
rasa init
```
but we have set up the project already at `backend/rasa`. Because we are only using the Rasa NLU, the relevant files are `data/nlu.md` and `config.yml`. 

File `nlu.md` contain the training examples that are used to train a model. Read about the training data format [here](https://rasa.com/docs/rasa/nlu/training-data-format/). Each intent in the training examples corresponds to a `Goal` in Convo. 

File `config.yml` contains the pipeline that Rasa will use to preprocess and ingest the training data to produce the pipeline. Read about pipelines in general [here](https://rasa.com/docs/rasa/nlu/choosing-a-pipeline/) and all the differnt possible componenets you can use [here](https://rasa.com/docs/rasa/nlu/components). Note the component [`HFTransformersNLP`](https://rasa.com/docs/rasa/nlu/components/#hftransformersnlp). This is what allows Rasa to leverage existing language models like BERT or GPT-2 to train a model. You can specify the language model via the parameter `model_name` and specify the particular weights to use via parameter `model_weights`. Below (taken from [here](https://rasa.com/docs/rasa/nlu/components/#hftransformersnlp)) are some of the different model and weights you can use.
```
+----------------+--------------+-------------------------+
| Language Model | Parameter    | Default value for       |
|                | "model_name" | "model_weights"         |
+----------------+--------------+-------------------------+
| BERT           | bert         | bert-base-uncased       |
+----------------+--------------+-------------------------+
| GPT            | gpt          | openai-gpt              |
+----------------+--------------+-------------------------+
| GPT-2          | gpt2         | gpt2                    |
+----------------+--------------+-------------------------+
| XLNet          | xlnet        | xlnet-base-cased        |
+----------------+--------------+-------------------------+
| DistilBERT     | distilbert   | distilbert-base-uncased |
+----------------+--------------+-------------------------+
| RoBERTa        | roberta      | roberta-base            |
+----------------+--------------+-------------------------+
```

## Training and Running with Convo
Now, to start using Rasa with Convo, we need to train a NLU-only model. To train and test a NLU-only model, read the guide [here](https://rasa.com/docs/rasa/nlu/using-nlu-only/). The guide tells you how to train and test a model using CLI commands. Created and trained models are added to the `models` directory in `rasa`. To interact with and use your newly trained model, you have to start a server with the model, like so
```bash
rasa run --enable-api
```
If you have multiple models, you can specify a model
```bash
rasa run --enable-api -m models/<name>.tar.gz
```
With the server running, you can request predictions from your model using the `/model/parse` endpoint of the server like so
```bash
curl localhost:5005/model/parse -d '{"text":"hello"}'
```
The guide referenced above contains more information about running the NLU server.

This is how Convo interacts with Rasa (through the endpoint). Convo has a file called `rasa_nlu.py` in `server` where this takes place.
