import re
from num2words import num2words


numerals = [{'letter': 'M', 'value': 1000},
            {'letter': 'D', 'value': 500},
            {'letter': 'C', 'value': 100},
            {'letter': 'L', 'value': 50},
            {'letter': 'X', 'value': 10},
            {'letter': 'V', 'value': 5},
            {'letter': 'I', 'value': 1}]

def roman_to_arabic(number):
    index_by_letter = {}
    for index in (range(len(numerals))):
        index_by_letter[numerals[index]['letter']] = index

    result = 0
    previous_value = None
    for letter in reversed(number):
        index = index_by_letter[letter.upper()]
        value = numerals[index]['value']
        if (previous_value is None) or (previous_value <= value):
            result += value
        else:
            result -= value
        previous_value = value
    
    return result

    
def roman_to_words(string):
    match = re.findall(r'\b(?=[MDCLXVI]+\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b', string)#, re.IGNORECASE)
    match = ["".join(m) for m in match]
    arabic = [roman_to_arabic(m) for m in match]
    words = ['the ' + str(num2words(a, ordinal = True)) for a in arabic]

    roman_i = 0
    new_s = []
    for t_i, token in enumerate(string.split()):
        token_no_punc = re.sub(r'[^\w\s]',"", token)
        if roman_i < len(match) and token_no_punc == match[roman_i] and len(token_no_punc)>1: # exclude single letter numerals
            if t_i==0:
                new_s.append(words[roman_i][4:] + ",") # if a roman numeral is in the start of sentence, delete "the" in the beginning & add a comma at the end
            else:
                if token.isupper(): # only substitue roman numerals all in caps (if not in caps & not in the beginning of sentence, might NOT be a roman numeral)
                    new_s.append(words[roman_i])
                else:
                    new_s.append(token)
            roman_i += 1
        else:
            new_s.append(token)

    return ' '.join(new_s)

'''
ex = ["henry vi and george viii",
      "henry III and william II",
      "everyone loves henry III the most.",
      "henry IV",
      "henry VII",
      "henry VIII",
      "henry XII",
      "IX. do this",
      "II. do that",
      "do dee do I went to school today"]

for s in ex:
    print(roman_to_words(s))
'''
