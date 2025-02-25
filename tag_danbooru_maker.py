string =input('enter danbooru tags: ')
result = string.replace("absurdres ","")
result = result.replace("highres ","")
result = result.replace("watermark ","")
result = result.replace("artist_name ","")

result = result.replace("chinese_commentary ","")
result = result.replace("english_commentary ","")
result = result.replace("commentary_request ","")
result = result.replace("commentary ","")

result = result.replace("translated ","")
speech = input("Delete Speech bubbles? (y/n): ")
if speech == "y":
    result.replace("speech bubble ","")
result = result.replace(" ",", ").replace("_"," ").replace("(","\(").replace(")","\)")
print(" ")
print(result+", masterpiece, best quality, good quality")