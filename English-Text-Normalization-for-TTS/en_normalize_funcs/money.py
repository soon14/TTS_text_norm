import re
from num2words import num2words
import numpy as np

from .decimal_ import decimal
from .cardinal import cardinal
from .currency_dicts import currency_code_dict, number_abbrev_dict

def money(a):
    combined_dict = {**currency_code_dict, **number_abbrev_dict}
    # output= np.empty(shape=(len(a),1),dtype=object)
    output=['AAAis is wrong!'] * len(a)
    #money=pd.read_csv("money_trans.csv")
    #money=money.as_matrix()
    #inputx=money[:,1]
    #outputx=money[:,2]
    currency_dict = {"$": "dollars", "¢": "cents", "£": "pounds", "¥": "yens", "₣": "francs", "₤": "liras", 
"₧": "pesetas", "€": "euros", "₹": "rupees", "₩": "wons", "₴": "hryvnias", "₯": "drachmas",
"₮": "tugriks", "₰": "german pennys", "₲": "guaranis", "₱": "pesos", "₳": "australs",
"₵": "cedis", "₭": "kips", "₪": "new sheqels", "₫": "dong"}

    for i in range(len(a)):
        if str(a[i]) in currency_dict:
            output[i]=currency_dict[str(a[i])]
            continue
        try:
            word=str(a[i]) #$9.5 million CAD 
            dec_comp=re.sub("[^0-9.]+","",word)  #9.5
            #match_comp=re.sub("[0-9a-z,.]+","",word).strip() 
            letters=re.sub("[^a-zA-Z\s]+","",word).lower().rstrip().lstrip() #million CAD
            parts = letters.split()
            expanded_parts = [combined_dict[p] if p in combined_dict else p for p in parts]
            if len(letters)>0:
                if len(letters.split()) == 2:
                    if parts[0] in number_abbrev_dict or parts[0] not in combined_dict:
                        first, second = expanded_parts[0], expanded_parts[1]
                    else:
                        first, second = expanded_parts[1], expanded_parts[0]
                    letters = first + " " + second
                else:
                    letters = expanded_parts[0]
            #letters = abbrev_dict[letters] if letters in abbrev_dict else letters
            symbol = re.sub("[0-9a-zA-Z,.]+","",word).strip() # $
            code = currency_dict[symbol] if symbol in currency_dict else ""
            
            if "." in dec_comp and letters == "":
                amounts = dec_comp.split(".")
                if int(dec_comp.split(".")[-1])>0:  # if cents part is bigger than 0
                    output_temp = " ".join(cardinal([amounts[0]])) + " " + code + " and " + " ".join(cardinal([amounts[1]])) + " cents"
                else: # if 0 cents
                    output_temp = " ".join(cardinal([dec_comp.split(".")[0]])) + " " + code
            else:
                if letters != "":
                    num_part = " ".join(decimal([dec_comp])[0]) if "." in dec_comp else " ".join(cardinal([dec_comp]))
                    output_temp = num_part + " " + letters
                    output_temp = output_temp  + " " + code if code not in letters else output_temp
                else: # no letters, no decimals (cents)
                    output_temp = " ".join(cardinal([dec_comp])) + " " + code
            '''
            try:
                if round(float(dec_comp))==float(dec_comp):
                    output_temp=decimal([str(round(float(dec_comp)))])[0][0]
                else:
                    output_temp=decimal([dec_comp])[0][0]
            except ValueError:
                output_temp=decimal([dec_comp])[0][0]
            '''
            ''' 
            if match_comp in inputx:
                k=np.where(inputx==match_comp)
                index=k[0][0]
                output_temp += " "
                output_temp +=outputx[index]
            '''
            #if match_comp in currency_dict:
            #    output_temp += " " + currency_dict[match_comp]
            try:
                if float(dec_comp.replace(",",""))==1 and output_temp[-1]=="s" and "million" not in output_temp and "billion" not in output_temp and "thousand" not in output_temp:
                    output_temp=output_temp[:-1]
            except ValueError:
                output_temp=output_temp
            
            output[i]=output_temp
        except ValueError:
            output[i]='AAAis is wrong!'
        except TypeError:
            output[i]='AAAis is wrong!'
    return output    
