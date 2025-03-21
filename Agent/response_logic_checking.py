import json
import requests
import spacy
import pronouncing
from collections import Counter


# cross checking for factual question


def search_serper(query):
    response_list = []
    url = "https://google.serper.dev/search"

    payload = json.dumps({"q": query})
    headers = {
        "X-API-KEY": "f7763502031addae6ffa57b1b3afc25ef2a35b5d",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = json.loads(response.text)

    # if search reach to a unique answer
    if "answerBox" in json_response:
        if "answer" in json_response["answerBox"]:
            return json_response["answerBox"]["answer"]
        elif "snippetHighlighted" in json_response["answerBox"]:
            return json_response["answerBox"]["snippetHighlighted"][0]
    else:
        # if search does not reach to a unique answer
        # use snippet of 10 searchs to find answer
        propositions = [organic["snippet"] for organic in json_response["organic"]]
        answer = answer_extraction(json_response["searchParameters"]["q"], propositions)
        return answer


def answer_extraction(query, propositions):
    # apply NER to propositions about the query and
    # find the most frequent word in the propositions nnd set it as answer
    nlp = spacy.load("en_core_web_sm")
    entity_counts = Counter()
    relevant_entities = {
        "PERSON",
        "GPE",
        "NORP",
        "LOC",
        "ORG",
        "CARDINAL",
        "WORK_OF_ART",
    }
    for proposition in propositions:
        doc = nlp(proposition)
        for ent in doc.ents:
            if ent.label_ in relevant_entities:
                entity_counts[ent.text] += 1

    for token in list(entity_counts):
        if token in query:
            entity_counts.pop(token, None)
    answer = entity_counts.most_common(1)[0][0]
    return answer


# check the rhyme of the poet


def cross_checking_factual_questions(query, llm_ans):

    check_answer = search_serper(query)
    return check_answer.lower() == llm_ans.lower(), check_answer


def get_last_syllables(word):

    pronunciations = pronouncing.phones_for_word(word)
    if not pronouncing:
        return None
    syllables = pronunciations[0].split()
    return tuple(syllables[-1:])


def get_rhyme_scheme(poem):
    # extract the rhyme of the last syllable of the each stanza

    last_words = [line.split()[-1].lower() for line in poem]
    last_syllables = [get_last_syllables(word) for word in last_words]

    if None in last_syllables:
        return ""

    rhyme_groups = {}
    rhyme_labels = []

    for syllable in last_syllables:
        if syllable not in rhyme_groups:
            rhyme_groups[syllable] = len(rhyme_groups)
        rhyme_labels.append(rhyme_groups[syllable])

    rhyme_string = "".join([chr(label + 65) for label in rhyme_labels])

    return rhyme_string


def rhyme_checking_poem(llm_poem):

    rhyme_string = get_rhyme_scheme(llm_poem)
    for i in range(0, len(rhyme_string) - 1, 2):
        if rhyme_string[i] != rhyme_string[i + 1]:
            return False
    return True
