from scipy import spatial
import gensim.downloader as api
import numpy as np
from events_formatter import FormatEvents
import spacy

# call `python -m spacy download en_core_web_md` on terminal
nlp = spacy.load("en_core_web_md")

compare_to = '''The American College of Clinical Pharmacy International Symposium educates and engage pharmacists in applying scientific and clinical evidence to real-world patient cases on the management of antimicrobial resistance to optimize patient care and outcomes. this event will cover areas like Discuss the evolution and current understanding of the mechanisms of antimicrobial resistance, Evaluate the effectiveness of antimicrobial therapy for multi-drug resistant gram-positive and gram-negative pathogens, Recommend management strategies for multi-drug resistant gram-positive and gram-negative infections.'''
compare_to_vector = nlp(compare_to)


fe = FormatEvents("./data/events.csv")
fe.format_columns()
events = fe.get_dataframe()
print(events.head())

events['similarity'] = events.loc[events['visitors'] != -1].apply(
    lambda row: compare_to_vector.similarity(nlp(row.description)), axis=1
)
events = events.sort_values(by='similarity', ascending=False)

print(len(events.loc[events.visitors == -1]))


print(events[['description', 'similarity']])
print(events.iloc[0])
