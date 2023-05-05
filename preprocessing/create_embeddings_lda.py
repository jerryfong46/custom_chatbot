import json
from gensim.corpora import Dictionary
from gensim.models import LdaModel


# Load the preprocessed data from a JSON file
def load_processed_data(input_file):
    with open(input_file, "r") as f:
        return json.load(f)


processed_data_file = "processed_data.json"
processed_data = load_processed_data(processed_data_file)


# Create a dictionary of words from the preprocessed data
def create_gensim_dictionary(processed_data):
    all_tokens = []
    for bank_data in processed_data.values():
        for item in bank_data:
            all_tokens.append(item["tokens"])

    dictionary = Dictionary(all_tokens)
    # Remove rare and common words from the dictionary
    dictionary.filter_extremes(no_below=5, no_above=0.5)
    return dictionary


dictionary = create_gensim_dictionary(processed_data)


# Create a corpus of documents from the preprocessed data using the dictionary
def create_gensim_corpus(processed_data, dictionary):
    corpus = []

    for bank_data in processed_data.values():
        for item in bank_data:
            bow = dictionary.doc2bow(item["tokens"])
            corpus.append(bow)

    return corpus


corpus = create_gensim_corpus(processed_data, dictionary)


# Train an LDA topic model using the corpus and dictionary
def train_lda_model(corpus, dictionary, num_topics=10, passes=20):
    lda_model = LdaModel(
        corpus, num_topics=num_topics, id2word=dictionary, passes=passes
    )
    return lda_model


lda_model = train_lda_model(corpus, dictionary)


# Save the trained LDA model to a file
def save_lda_model(lda_model, output_file):
    lda_model.save(output_file)


lda_model_output_file = "lda_model"
save_lda_model(lda_model, lda_model_output_file)
