string =input('enter danbooru tags: ')
result = string.replace("absurdres ","")
result = result.replace("highres ","")
result = result.replace("watermark ","")
result = result.replace("artist_name ","")
result = result.replace("md5_mismatch ","")
result = result.replace("animated ","")

result = result.replace("translation_request ","")
result = result.replace("translated ","")

result = result.replace("chinese_commentary ","")
result = result.replace("english_commentary ","")
result = result.replace("symbol-only_commentary ","")
result = result.replace("commentary_request ","")
result = result.replace("commentary ","")

result = result.replace("korean ","")

result = result.replace("paid_reward_available ","")

result = result.replace("large_variant_set ","")
result = result.replace("variant_set ","")

result = result.replace("sound_effects ","")
result = result.replace("speech_bubble ","")

result = result.replace(" ",", ").replace("_"," ").replace("(","\(").replace(")","\)")

result = result+", masterpiece, best quality, good quality"
print(" ")
print(result)
import pyperclip
pyperclip.copy(result)
print("Dữ liệu đã được sao chép vào bộ nhớ tạm.")