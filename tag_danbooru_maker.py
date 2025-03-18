string =input('enter danbooru tags: ')
result = string.replace("original ","")
result = string.replace("corrupted_twitter_file ","")
result = string.replace("absurdres ","")
result = result.replace("highres ","")
result = result.replace("lowres ","")
result = result.replace("watermark ","")
result = result.replace("variant_set ","")
result = result.replace("alt_text ","")
result = result.replace("revision ","")

result = result.replace("comiket_104 ","")

result = result.replace("bad_source ","")
result = result.replace("bad_id ","")
result = result.replace("bad_pixiv_id ","")

result = result.replace("artist_name ","")
result = result.replace("twitter_username ","")
result = result.replace("twitter_username","")
result = result.replace("signature ","")

result = result.replace("md5_mismatch ","")
result = result.replace("animated ","")
result = result.replace("patreon_logo ","")
result = result.replace("patreon_username ","")
result = result.replace("artist_name ","")

result = result.replace("translation_request ","")
result = result.replace("check_translation ","")
result = result.replace("partially_translated ","")
result = result.replace("translated ","")

result = result.replace("novel_illustration ","")
result = result.replace("official_art ","")
result = result.replace("cover_image ","")
result = result.replace("cover ","")
result = result.replace("subscribestar_username ","")
result = result.replace("web_address ","")

result = result.replace("pixiv_commission ","")
result = result.replace("commission ","")


result = result.replace("mixed-language_commentary ","")
result = result.replace("partial_commentary ","")
result = result.replace("hashtag-only_commentary ","")
result = result.replace("chinese_commentary ","")
result = result.replace("english_commentary ","")
result = result.replace("korean_commentary ","")
result = result.replace("symbol-only_commentary ","")
result = result.replace("commentary_request ","")
result = result.replace("commentary ","")

result = result.replace("korean ","")
result = result.replace("english_text ","")

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