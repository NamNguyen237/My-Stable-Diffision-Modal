string =input('enter danbooru tags: ')
results = string.replace("watermark","").replace(" ",", ").replace("_"," ").replace("(","\(").replace(")","\)")
print(" ")
print(results+", masterpiece, best quality, good quality")