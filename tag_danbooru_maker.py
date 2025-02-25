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
result = result.replace("speech bubble ","")

result = result.replace(" ",", ").replace("_"," ").replace("(","\(").replace(")","\)")

result = result+", masterpiece, best quality, good quality"
print(" ")
print(result)
import pyperclip
pyperclip.copy(result)
print("Dữ liệu đã được sao chép vào bộ nhớ tạm.")