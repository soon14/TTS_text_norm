import re
from num2words import num2words
import numpy as np

from .decimal_ import decimal
from .units_dict import units_dict

def measure(a):
    output=['AAAis is wrong!'] * len(a)
    for i in range(len(a)):
        try:
            word=str(a[i])
            word=word.replace(",","")
            if "-" in word:
                output_temp="minus "
            else:
                output_temp=""
            comp=re.findall(r'[0-9.]+|[A-Za-zå$°µ/%\u0374-\u03FF\'\"]+[ /A-Za-z0-9⁰¹²³⁴⁵⁶⁷⁸⁹]?', word)

            comp = [c.replace("⁰","0").replace("¹","1").replace("²","2").replace("³","3").replace("⁴","4").replace("⁵","5").replace("⁶","6").replace("⁷","7").replace("⁸","8").replace("⁹","9") for c in comp]

            case_sensitive_chars = ["m", "M", "n", "N", "s", "S", "t", "T"]
            comp = [c.lower() if not sum([ch in c for ch in case_sensitive_chars])>0 else c for c in comp]
            comp = [re.sub(r'[^\w\s]','',c).lower() if "us" in re.sub(r'[^\w\s]','',c).lower() else c for c in comp]
            if len(comp)>0:
                for k in range(len(comp)):
                    comp[k]=comp[k].replace(" ","")
                try:
                    num_temp=decimal([comp[0]])[0][0]
                    output_temp += num_temp
                    if len(comp)>1:
                        for j in range(1, len(comp)):
                            if comp[j] in units_dict:
                                output_temp += " " + units_dict[comp[j]]
                    else:
                        output_temp += " " + word
                    if float(comp[0])==1 and output_temp[-1]=="s":
                        output_temp=output_temp[:-1]
                except ValueError:
                    output_temp=""
                    for j in range(len(comp)):
                        if comp[j] in units_dict:
                            if j>0:
                                output_temp +=" "
                            output_temp += units_dict[comp[j]]
                    if len(output_temp)>0:
                        if output_temp[-1]=="s":
                            output_temp=output_temp[:-1]
                output_temp=re.sub( '\s+', ' ', output_temp)
            output[i]=output_temp
        except ValueError:
            output[i]='AAAis is wrong!'
        except TypeError:
            output[i]='AAAis is wrong!'
    return output
