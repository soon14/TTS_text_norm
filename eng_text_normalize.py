# text_normalize.py
# from . import cleaners
from eng_text_norm import cleaners

raw_text = 'English 1234 qaba'
text = cleaners.english_cleaners(raw_text)
print(text)