with open("tmp.txt", "r") as f:
    k = f.read().split("\n")

k = ['"'+kk+'"' for kk in k]

with open('out1.txt', 'w') as f:
    for kk in k:    
        f.write(kk)
        f.write("\n")
