with open("units.txt", "r") as f:
    k = f.read().strip().split("\n")
    case_sensitive_chars = ["m", "M", "n", "N", "s", "S", "t", "T"]
    k = [kk.lower() if sum([ch in kk.split("\t")[1] for ch in case_sensitive_chars])==0 else kk for kk in k]
    k = [kk.split("\t") for kk in k]
    #f = {kk[1].lower() : kk[0].lower()+'s' for kk in k}
    f = {kk[1] : kk[0]+'s' for kk in k}

print(f)
