import re
from tools_english.abbrev_list import _abbreviations
from tools_english.greek_letter_dict import greek_dict
from tools_english.roman_numerals import roman_to_words
from en_normalize_funcs.units_dict import units_dict, units_dict_special, units_dict_case_sensitive
import nltk
from nltk.corpus import words
# nltk.download('words')

units = units_dict.keys()

month_full = ['january', 'february','march','april','may','june','july','august','september','october','november','december']   
month_sim = {'jan':'january', 'feb':'february','mar':'march','apr':'april','may':'may', 'jun': 'june','jul':'july','aug':'august','sept':'september','sep':'september','oct':'october','nov':'november','dec':'december'}
month_short = list(month_sim.keys())
month_num = {'01':'january', '02':'february','03':'march','04':'april','05':'may', '06': 'june','07':'july','08':'august','09':'september','1':'january', '2':'february','3':'march','4':'april','5':'may', '6': 'june','7':'july','8':'august','9':'september','10':'october','11':'november','12':'december'}

currency_codes = ['$', '¢', '£', '¥', '₣', '₤', '₧', '€', '₹', '₩', '₴', '₯', '₮', '₰', '₲', '₱', '₳', '₵', '₭', '₪', '₫']
currency_units = ["k", "thousand", "m", "million", "b", "billion", "t", "trillion", "q", "quadrillion"]
country_codes = ['aed', 'afn', 'all', 'amd', 'ang', 'aoa', 'ars', 'aud', 'awg', 'azn', 'bam', 'bbd', 'bdt', 'bgn', 'bhd', 'bif', 'bmd', 'bnd', 'bob', 'bov', 'brl', 'bsd', 'btn', 'bwp', 'byn', 'bzd', 'cad', 'cdf', 'che', 'chf', 'chw', 'clf', 'clp', 'cny', 'cop', 'cou', 'crc', 'cuc', 'cup', 'cve', 'czk', 'djf', 'dkk', 'dop', 'dzd', 'egp', 'ern', 'etb', 'eur', 'fjd', 'fkp', 'gbp', 'gel', 'ghs', 'gip', 'gmd', 'gnf', 'gtq', 'gyd', 'hkd', 'hnl', 'hrk', 'htg', 'huf', 'idr', 'ils', 'inr', 'iqd', 'irr', 'isk', 'jmd', 'jod', 'jpy', 'kes', 'kgs', 'khr', 'kmf', 'kpw', 'krw', 'kwd', 'kyd', 'kzt', 'lak', 'lbp', 'lkr', 'lrd', 'lsl', 'lyd', 'mad', 'mdl', 'mga', 'mkd', 'mmk', 'mnt', 'mop', 'mru', 'mur', 'mvr', 'mwk', 'mxn', 'mxv', 'myr', 'mzn', 'nad', 'ngn', 'nio', 'nok', 'npr', 'nzd', 'omr', 'pab', 'pen', 'pgk', 'php', 'pkr', 'pln', 'pyg', 'qar', 'ron', 'rsd', 'rub', 'rwf', 'sar', 'sbd', 'scr', 'sdg', 'sek', 'sgd', 'shp', 'sll', 'sos', 'srd', 'ssp', 'stn', 'svc', 'syp', 'szl', 'thb', 'tjs', 'tmt', 'tnd', 'top', 'try', 'ttd', 'twd', 'tzs', 'uah', 'ugx', 'usd', 'usn', 'uyi', 'uyu', 'uyw', 'uzs', 'ves', 'vnd', 'vuv', 'wst', 'xaf', 'xag', 'xau', 'xba', 'xbb', 'xbc', 'xbd', 'xcd', 'xdr', 'xof', 'xpd', 'xpf', 'xpt', 'xsu', 'xts', 'xua', 'xxx', 'yer', 'zar', 'zmw', 'zwl', 'cnh', 'ggp', 'imp', 'jep', 'kid', 'nis', 'ntd', 'prb', 'sls', 'rmb', 'tvd', 'zwb', 'dash', 'eth', 'vtc', 'xbt', 'xlm', 'xmr', 'xrp', 'zec', 'adf', 'adp', 'afa', 'aok', 'aon', 'aor', 'arl', 'arp', 'ara', 'ats', 'azm', 'bad', 'bef', 'bgl', 'bop', 'brb', 'brc', 'brn', 'bre', 'brr', 'byb', 'byr', 'csd', 'csk', 'cyp', 'ddm', 'dem', 'ecs', 'ecv', 'eek', 'esa', 'esb', 'esp', 'fim', 'frf', 'gne', 'ghc', 'gqe', 'grd', 'gwp', 'hrd', 'iep', 'ilp', 'ilr', 'isj', 'itl', 'laj', 'ltl', 'luf', 'lvl', 'maf', 'mcf', 'mgf', 'mkn', 'mlf', 'mvq', 'mro', 'mxp', 'mzm', 'mtl', 'nic', 'nlg', 'peh', 'pei', 'plz', 'pte', 'rol', 'rur', 'sdd', 'sdp', 'sit', 'skk', 'sml', 'srg', 'std', 'sur', 'tjr', 'tmm', 'tpe', 'trl', 'uak', 'ugs', 'uss', 'uyp', 'uyn', 'val', 'veb', 'vef', 'xeu', 'xfo', 'xfu', 'ydd', 'yud', 'yun', 'yur', 'yuo', 'yug', 'yum', 'zal', 'zmk', 'zrz', 'zrn', 'zwc', 'zwd', 'zwn', 'zwr', 'united arab emirates dirhams', 'afghan afghanis', 'albanian leks', 'armenian drams', 'netherlands antillean guilders', 'angolan kwanzas', 'argentine pesos', 'australian dollars', 'aruban florins', 'azerbaijani manats', 'bosnia and herzegovina convertible marks', 'barbados dollars', 'bangladeshi takas', 'bulgarian levs', 'bahraini dinars', 'burundian francs', 'bermudian dollars', 'brunei dollars', 'bolivianos', 'bolivian mvdol s', 'brazilian reals', 'bahamian dollars', 'bhutanese ngultrums', 'botswana pulas', 'belarusian rubles', 'belize dollars', 'canadian dollars', 'congolese francs', 'w i r euros', 'swiss francs', 'wirfrancs', 'unidad de fomentos', 'chilean pesos', 'chinese yuans', 'colombian pesos', 'unidad de valor reals', 'costa rican colons', 'cuban convertible pesos', 'cuban pesos', 'cape verdean escudos', 'czech korunas', 'djiboutian francs', 'danish krones', 'dominican pesos', 'algerian dinars', 'egyptian pounds', 'eritrean nakfas', 'ethiopian birrs', 'euros', 'fiji dollars', 'falkland islands pounds', 'pound sterlings', 'georgian laris', 'ghanaian cedis', 'gibraltar pounds', 'gambian dalasis', 'guinean francs', 'guatemalan quetzals', 'guyanese dollars', 'hong kong dollars', 'honduran lempiras', 'croatian kunas', 'haitian gourdes', 'hungarian forints', 'indonesian rupiahs', 'israeli new shekels', 'indian rupees', 'iraqi dinars', 'iranian rials', 'icelandic kronas', 'jamaican dollars', 'jordanian dinars', 'japanese yens', 'kenyan shillings', 'kyrgyzstani soms', 'cambodian riels', 'comoro francs', 'north korean wons', 'south korean wons', 'kuwaiti dinars', 'cayman islands dollars', 'kazakhstani tenges', 'lao kips', 'lebanese pounds', 'sri lankan rupees', 'liberian dollars', 'lesotho lotis', 'libyan dinars', 'moroccan dirhams', 'moldovan leus', 'malagasy ariarys', 'macedonian denars', 'myanmar kyats', 'mongolian togrogs', 'macanese patacas', 'mauritanian ouguiyas', 'mauritian rupees', 'maldivian rufiyaas', 'malawian kwachas', 'mexican pesos', 'mexican unidad de inversions', 'malaysian ringgits', 'mozambican meticals', 'namibian dollars', 'nigerian nairas', 'nicaraguan cordobas', 'norwegian krones', 'nepalese rupees', 'new zealand dollars', 'omani rials', 'panamanian balboas', 'peruvian sols', 'papua new guinean kinas', 'philippine pesos', 'pakistani rupees', 'polish zlotys', 'paraguayan guaranis', 'qatari riyals', 'romanian leus', 'serbian dinars', 'russian rubles', 'rwandan francs', 'saudi riyals', 'solomon islands dollars', 'seychelles rupees', 'sudanese pounds', 'swedish kronas', 'singapore dollars', 'saint helena pounds', 'sierra leonean leones', 'somali shillings', 'surinamese dollars', 'south sudanese pounds', 'sao tomae and principe dobras', 'salvadoran colons', 'syrian pounds', 'swazi lilangenis', 'thai bahts', 'tajikistani somonis', 'turkmenistan manats', 'tunisian dinars', 'tongan paʻangas', 'turkish liras', 'trinidad and tobago dollars', 'new taiwan dollars', 'tanzanian shillings', 'ukrainian hryvnias', 'ugandan shillings', 'u s dollars', 'u s dollar next days', 'uruguay peso en unidades indexadas', 'uruguayan pesos', 'unidad previsionals', 'uzbekistan soms', 'venezuelan bolivar soberanos', 'vietnamese dongs', 'vanuatu vatus', 'samoan talas', 'central african c f a francs', 'silver ounces', 'gold ounces', 'european composite units', 'european monetary units', 'bitcoin plus', 'european unit of account seventeens', 'east caribbean dollars', 'special drawing rights', 'west african c f a francs', 'palladiums', 'c f p francs', 'platinums', 'sucres', 'code reserved for testings', 'a d b unit of accounts', 'no currencys', 'yemeni rials', 'south african rands', 'zambian kwachas', 'zimbabwean dollars', 'chinese yuans', 'guernsey pounds', 'isle of man pounds', 'jersey pounds', 'kiribati dollars', 'israeli new shekels', 'new taiwan dollars', 'transnistrian rubles', 'somaliland shillings', 'chinese yuans', 'tuvalu dollars', 'zimbabwean bonds', 'dashs', 'ethers', 'vertcoins', 'bitcoins', 'stellar lumens', 'moneros', 'x r ps', 'z cashs', 'andorran francs', 'andorran pesetas', 'afghan afghanis', 'angolan kwanzas', 'angolan new kwanzas', 'angolan kwanza reajustados', 'argentine peso leys', 'argentine peso argentinos', 'argentine australs', 'austrian schillings', 'azerbaijani manats', 'bosnia and herzegovina dinars', 'belgian francs', 'bulgarian levs', 'bolivian pesos', 'brazilian cruzeiros', 'brazilian cruzados', 'brazilian cruzado novos', 'brazilian cruzeiros', 'brazilian cruzeiro reals', 'belarusian rubles', 'belarusian rubles', 'serbian dinars', 'czechoslovak korunas', 'cypriot pounds', 'east german marks', 'german marks', 'ecuadorian sucres', 'ecuadorunidad de valor constantes', 'estonian kroons', 'spanish peseta account as', 'spanish peseta account bs', 'spanish pesetas', 'finnish markkas', 'french francs', 'guinean sylis', 'ghanaian cedis', 'equatorial guinean ekweles', 'greek drachmas', 'guinea-bissau pesos', 'croatian dinars', 'irish pounds', 'israeli liras', 'israeli shekels', 'icelandic old kronas', 'italian liras', 'lao kips', 'lithuanian litas', 'luxembourg francs', 'latvian lats', 'moroccan francs', 'monegasque francs', 'malagasy francs', 'old macedonian denars', 'mali francs', 'maldivian rupees', 'mauritanian ouguiyas', 'mexican pesos', 'mozambican meticals', 'maltese liras', 'nicaraguan cordobas', 'dutch guilders', 'peruvian old sols', 'peruvian intis', 'polish zlotys', 'portuguese escudos', 'romanian leus', 'russian rubles', 'sudanese dinars', 'sudanese old pounds', 'slovenian tolars', 'slovak korunas', 'san marinese liras', 'suriname guilders', 'sao tome and principe dobras', 'soviet union rubles', 'tajikistani rubles', 'turkmenistani manats', 'portuguese timorese escudos', 'turkish liras', 'ukrainian karbovanets', 'ugandan shillings', 'u s dollar same days', 'uruguay pesos', 'uruguay new pesos', 'vatican liras', 'venezuelan bolivars', 'venezuelan bolivar fuertes', 'european currency units', 'gold francs', 'u i c francs', 'south yemeni dinars', 'yugoslav dinars', 'yugoslav dinars', 'yugoslav dinars', 'yugoslav dinars', 'yugoslav dinars', 'yugoslav dinars', 'south african financial rands', 'zambian kwachas', 'zairean zaires', 'zairean new zaires', 'rhodesian dollars', 'zimbabwean dollars', 'zimbabwean dollars', 'zimbabwean dollars']
currencies = currency_codes + currency_units + country_codes

############################## helper functions ###############################
def extract_letter_only(string, lower=True):
    s = re.sub(r'[^\w\s]',""," ".join(re.findall("[a-zA-Z]+", string.strip())))
    return s.lower() if lower else s

def extract_number_only(string, consider_negative=False):
    if consider_negative:
        return re.sub('[^(-?\d+\.*\d*)]',"",string.strip())
    else:
        return re.sub('[^(\d+\.*\d*)]',"",string.strip())

def extract_special_ch_only(string):
    return re.sub(r'[^\W]',""," ".join(re.findall("[%&=+]+", string.strip())))

def remove_punc(string):
    return re.sub(r'[^\w\s]',"", string)

def remove_eos_punc(string): # remove >=1 SOS & EOS puncs
    return re.sub('\W+$',"", string)

def remove_num(string):
    return re.sub('-[\d]+',"", string)

def return_None_if_not_date(string):
    return string if extract_number_only(string) and (int(extract_number_only(string))<=31 or len(extract_number_only(string))==4) else None

def if_no_is_number(tokens_list, token, token_i, attached=False):
    ''' Check if "no" is an abbreviation for 'number', by checking if the next token is a number
        :param tokens_list: list of all tokens in the sentence
        :param token: token in question 
        :param token_i: index of token in tokens_list
        :param combined: (bool) if checking for "no" & number attached or not (i.e. No.2 or No. 2)'''
    if token == "no" or token.split(".")[0] == "no":
        if attached:
            if extract_number_only(token.split(".")[1]): 
                return True
            else:
                return False
        else:
            if token_i<len(tokens_list)-1 and extract_number_only(tokens_list[token_i+1]).isdigit():
                return True
            else:
                return False
    else:
        return True

########################### preprocessing functions ###########################  
def replace_colons(text):
    '''replace colon with comma ONLY if it's between 2 letters (colon btwn 2 numbers is time)'''
    return re.sub('(?<=\D) *: *(?=\D)', ', ', text)     

def fix_slashes(text):
    ''' repalce slash with a space ONLY IF it's between letters 
        -if not, it will be deleted & 2 letters will be combined
        - not replacing slash between numbers, because they can be dates, fractions, etc'''
    return re.sub('(?<=\D)/(?=\D)', " ", text)

def fix_x(text):
    ''' replace 'x' or 'X' between 2 numbers with 'by' '''
    return re.sub('(?<=\d) *[xX] *(?=\d)', ' by ', text)

def fix_quotations(text):
    '''replace all quotations except a standard single quotation mark: ' & delete double quotation'''
    return text.replace('’', "'").replace('`', "'").replace('‘', '').replace('’', "'").replace('“', '').replace('”', '').replace('"','') 

def fix_AM_PM(text):
    '''replace am->a.m., AM->A.M. pm->p.m. PM->P.M. if it follows an integer.'''
    text = re.sub('(?<=\d) *am', ' A.M.', text)
    text = re.sub('(?<=\d) *AM', ' A.M.', text)
    text = re.sub('(?<=\d) *pm', ' P.M.', text)
    text = re.sub('(?<=\d) *PM', ' P.M.', text) 
    return text

def fix_foreign_chars(text):
    '''replace foreign characters (with diacritic marks) with corresponding english pronunciation'''
    foreign_char_dict = {"ä":"eh", "á":"a", "â":"aa", "à":"ah", "é":"eh", "è":"eh", "ê":"e", "ë":"e", "î":"i", 
                         "í":"i", "ï":"i", "ö":"o", "ô":"o", "ü":"ue", "û":"eu", "eu":"oi", "äu":"oi", "oû":"oo", 
                         "æ":"ae", "œ":"eu", "eû":"eu", "jä":"yeh", "nyi":"ni", "ály":"aai", "ç":"s","çs":"ts", "szé":"se"}
    return "".join([foreign_char_dict[ch.lower()] if ch.lower() in foreign_char_dict else ch for ch in list(text)]) 

def replace_special_chars(text):
    '''replace special characters, %&+=, with equivalent words'''
    special_ch_dict = {"%":"percent", "&":"and", "+":"plus", "=":"equals"}  
    str_wt_special_ch = re.findall("\w?[%&+=][^\w]?", text)
    str_wt_special_ch = sorted(str_wt_special_ch, key=len)[::-1] # sort list by longest to shortest string length (3->2->1)   

    for s in str_wt_special_ch:
        if len(s)==3:   # replace <alphanumeric + special char + other punctuation> strings first; e.g. "30%."
            text = text.replace(s, s[0]+" "+special_ch_dict[s[1]]+s[2])
        elif len(s)==2: # then replace <alphanumeric + special char> strings; e.g. "30%"
            if s[1] in "%&+=":
                text = text.replace(s, s[0]+" "+special_ch_dict[s[1]]+" ")
            elif s[0] in "%&+=": 
                text = text.replace(s, special_ch_dict[s[0]]+s[1])
        elif len(s)==1: # then replace <special char> strings; e.g. "%"
            text = text.replace(s, special_ch_dict[s[0]])
    return text

def replace_brackets(text):
    '''replace brackets with comma, where appropriate.'''
    str_wt_bracket = re.findall("[\w\s]?[()][^\w]?", text)
    str_wt_bracket = sorted(str_wt_bracket, key=len)[::-1] # sort list by longest to shortest string length (3->2->1)   

    for s in str_wt_bracket:
        if len(s)==3:   # replace <alphanumeric + special char + other punctuation> strings first; e.g. "e) " or "e)."
            if s[2]==" ":
                text = text.replace(s, s[0]+", ")
            else:
                text = text.replace(s, s[0]+s[2])
        elif len(s)==2: # then replace <alphanumeric + special char> strings; e.g. "e("
            if s[1] in "()":
                if s[0] == "\n":    # if starting bracket is in the beginning of a paragraph, remove it.
                    text = text.replace(s, "\n")
                elif s[0] == " ":   # if a space before starting bracket
                    text = text.replace(s, ", ")
                else:               # if alphanumeric ch before starting bracket
                    text = text.replace(s, s[0]+", ")
            elif s[0] in "()":     # rare case  
                text = text.replace(s, "")
        elif len(s)==1:             # rare case: if starting bracket is at the start of the text or either bracket stands alone, just delete it
            text = text.replace(s, "")  
    return text
    
def fix_dash_and_tilde_btwn_two_nums(text):
    '''replace dash between 2 numbers ONLY with "to" 
    (if >2 nums with dash in between, it's telephone number and should NOT be replaced with "to")'''
    btwn_2_nums_dash = re.findall("(?<=[^-\d\s]) *[0-9]+ *[-~] *[0-9]+ *(?=[^-\d\s])", text)
    for d in btwn_2_nums_dash:
        text = text.replace(d, re.sub(" *[-~] *", " to ", d))  
    text = re.sub('(?<=\D) *[-~] *(?=\D)', ', ', text)     # replace dash between 2 words with a comma
    return text

def delete_citations(text):
    ''' delete any citation, e.g. [23] '''
    return re.sub('\[\d*\]', ' ', text)   

def fix_2_d_3_d(text):
    ''' replace 2-D, 3-D, etc with 2 D, 3 D, etc. '''
    return re.sub('(?<=\d) *-? *[dD]', ' d', text)  

def fix_k_thousand(text):
    ''' if letter 'k' or 'K' follows a number without space, insert space in between'''
    return re.sub('(?<=\d)[kK]', ' k', text)
    
def fix_greek_letters(text):
    '''replace greek letters (except lowercase miu - can be "micro" of unit)'''
    greek_chs = re.findall("[ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλνξοπρσςτυφχψω]", text)
    if len(greek_chs)>0:
        for g in greek_chs:
            text = text.replace(g, " " + greek_dict[g] + " ")  
    return text

def fix_hashtag(text):
    text = re.sub('# *(?=\d)', 'number ', text) # if a number follows, fix with "number" (e.g. #1 in Canada)
    text = re.sub('# *(?=[a-zA-Z])', 'hashtag ', text) # if a word follows, fix with "hashtag" (e.g. #blackmirror is on the rise.)
    text = re.sub('(?<=[abcdefgABCDEFG]) ?#', ' sharp', text) # if a single character among abcdefg precedes, fix with "sharp" (e.g. this note is b#)
    return text

def remove_repeated_symbols_and_spaces(text):
    reg_spacedSymbols = re.compile(r'(\W+?)\1+')
    return reg_spacedSymbols.sub(r'\1',text)

def fix_comma_and_another_punc(text):
    '''replace comma + another punc with the another punc only'''
    comma_be4_puncs = re.findall(",[^\w\s]", text)
    for p in comma_be4_puncs:
        text = text.replace(p, p[1])
    return text

def fix_comma_and_letters(text):
    '''replace comma between 2 letters with no space (cat,dog) with comma and space (cat, dog)
       this is because if 1st case (cat,dog), normalizer model incorrectly predicts the class of the word as a web address'''
    return re.sub('(?<=\D),(?=\D)', ', ', text)     

def _normalize_with_dictionary(text, dic, case_sensitive=False):
    '''replace UNIT SYMBOLS with their spoken words'''
    if any(key in text for key in list(dic.keys()) + [k.lower() for k in dic.keys()] + [k.upper() for k in dic.keys()]):
        if case_sensitive: # whether the unit has lower/uppercase MATTERS (e.g. mm vs. Mm)
            pattern = re.compile('|'.join(r'(-?\d+\.*\d*) *' + re.escape(key) + r'(?!\w)' for key in dic.keys()))
            return pattern.sub(lambda x:re.sub(re.sub(r'-?\d+\.*\d*', '', x.group()), '', x.group()) + ' ' + dic[re.sub(r'-?\d+\.*\d*\s*','',x.group())], text)
        else:
            # include both lowercase & uppercase versions of the units
            pattern = re.compile('|'.join(r'(-?\d+\.*\d*) *' + re.escape(key).lower() + r'(?!\w)' + '|' + r'(-?\d+\.*\d*) *' + re.escape(key).upper() + r'(?!\w)' for key in dic.keys()))
            return pattern.sub(lambda x:re.sub(re.sub(r'-?\d+\.*\d*', '', x.group()), '', x.group()) + ' ' + dic[re.sub(r'-?\d+\.*\d*\s*','',x.group().lower())], text)
    else:
        return text

def expand_abbreviations(text):
    '''expand abbreviations with a period in front (e.g. Mrs. Mr.)'''
    for regex, replacement in _abbreviations:
        text = re.sub(regex, replacement, text)
    return text


def tokenize(text):
    # replace special characters with appropriate punctuations
    text = text.replace("–", "-").replace(";", ",")
    text = replace_colons(text)
    text = _normalize_with_dictionary(text, units_dict_special)
    text = _normalize_with_dictionary(text, units_dict_case_sensitive, case_sensitive=True)
    text = _normalize_with_dictionary(text, units_dict)
    text = fix_slashes(text)
    text = fix_x(text)
    text = fix_quotations(text)
    text = fix_AM_PM(text)     
    text = fix_foreign_chars(text)
    text = replace_special_chars(text)
    text = replace_brackets(text)                  
    text = fix_dash_and_tilde_btwn_two_nums(text)     # replace dash (-) or tilde (~) between 2 nums to "to"
    text = delete_citations(text) # delete any citation, e.g. [23] 
    text = fix_2_d_3_d(text)      # replace 2-D, 3-D, etc with 2 D, 3 D, etc. 
    text = fix_k_thousand(text)
    text = roman_to_words(text)    # substitue roman numerals into equivalent words
    text = fix_greek_letters(text) # substitute greek letters except lowercase miu - can be "micro" of units
    text = fix_hashtag(text)
    text = remove_repeated_symbols_and_spaces(text)
    text = fix_comma_and_another_punc(text)
    text = fix_comma_and_letters(text)
    text = expand_abbreviations(text)

    tokens_list = []
    tokens = text.split()
    
    i=0
    processed_date_tokens_idxs = []
    
    while i < len(tokens):
        token = tokens[i]
            
        ###### ACRONYMS VS. ALL-UPPERCASE WORDS ######
        # if a normal word is written in all-uppercase letters, normalizer might predict it to be acronym, thus separating each alphabet
        token_no_punc = extract_letter_only(token, lower=False)
        if token_no_punc.isupper():
            if token_no_punc.lower()!="us" and token_no_punc.lower() in words.words():
                token = token.lower()
        
        ###### MONEY ######   
        if token in currency_codes or extract_letter_only(token) in country_codes:
            money_list = [tokens[i]]
            # check if more money terms are after this token
            plus_i = i+1
            while plus_i<len(tokens) and (extract_number_only(tokens[plus_i]).isdigit() or extract_letter_only(tokens[plus_i]) in currencies or tokens[plus_i] in currency_codes):
                money_list.append(tokens[plus_i])
                plus_i += 1
            # check if more money terms are before this token
            minus_i = i - 1
            while minus_i>=0 and (extract_number_only(tokens[minus_i]).isdigit() or extract_letter_only(tokens[minus_i]) in currencies or tokens[minus_i] in currency_codes):
                money_list = [tokens[minus_i]] + money_list
                minus_i -= 1
                tokens_list = tokens_list[:-1]
            tokens_list.append(" ".join(money_list))
            i = plus_i

        ###### DATE ######
        elif extract_letter_only(token) in month_full+month_short: #or 1<= int_part <=12: # if a month found,
            done=False
            nxt = return_None_if_not_date(remove_punc(tokens[i+1])) if i<len(tokens)-1 and i+1 not in processed_date_tokens_idxs else None
            if nxt:
                processed_date_tokens_idxs.append(i+1)
            nxtnxt = return_None_if_not_date(remove_punc(tokens[i+2])) if i<len(tokens)-2 and i+2 not in processed_date_tokens_idxs else None
            if nxtnxt:
                processed_date_tokens_idxs.append(i+2)
            prev = return_None_if_not_date(remove_punc(tokens[i-1])) if i>0 and i-1 not in processed_date_tokens_idxs else None
            if prev:
                processed_date_tokens_idxs.append(i-1)

            if nxt: # if next word is date
                if prev:
                    # if (Nov 09 '19 next word = year) or (next word = date & previous word = year) or (next word = year & previous word = date)
                    if (tokens[i+1][0] == "'" and len(nxt)==2) or (int(extract_number_only(nxt))<=31 and len(prev)==4) or (int(extract_number_only(prev))<=31 and len(nxt)==4):     
                         tokens_list = tokens_list[:-1]
                         tokens_list.append(" ".join([prev, token, tokens[i+1]]))
                         i+=2
                         done=True
                         
                elif nxtnxt:
                    if len(nxtnxt) == 4:
                        tokens_list.append(" ".join([token, tokens[i+1], tokens[i+2]]))  # Nov 30 2019
                        i+=3
                        done=True
                        
                elif (tokens[i+1][0] == "'" and len(nxt)==2) or int(extract_number_only(nxt))<=31 or len(nxt)==4:  # 
                    tokens_list.append(" ".join([token, tokens[i+1]]))  # Nov '19
                    i+=2
                    done=True
           
            elif prev:
                if int(extract_number_only(prev))<=31:
                    tokens_list = tokens_list[:-1]
                    tokens_list.append(" ".join([tokens[i-1], token]))  # 30 Nov
                    i+=1
                    done=True
                    
                elif len(prev)==4:
                    tokens_list = tokens_list[:-1]
                    tokens_list.append(" ".join([token, tokens[i-1]]))  # 2019 Nov -> Nov 2019
                    i+=1
                    done=True
            
            if done==False: # November
                tokens_list.append(token)
                i+=1

        # if token is NOT one of unit, money, or date AND contains both letter and number
        elif extract_letter_only(token) and extract_number_only(token):
            split_by_ch_and_num = [t for t in re.split('(\d+)',token) if t!=''] # split the token into separate letter & number parts
            tokens_list.extend(split_by_ch_and_num)
            i+=1

        else:
            tokens_list.append(token)
            i+=1

    return [token for token in tokens_list if token!=""]
