string =input('enter converted danbooru tags: ')
result = string
#breasts: "đồi núi"
result = result.replace(" large breasts,","")
result = result.replace(" breasts,","")
#boobs
result = result.replace(" underboob,","")
result = result.replace(" sideboob,","")

#armpit
result = result.replace(" armpit crease,","")

#ass
result = result.replace(" ass,","")

#cleavage: "khe thung lũng"
result = result.replace(" cleavage,","")

#collarbone: xương quai xanh
result = result.replace(" collarbone,","")
#bangs: tóc mái
result = result.replace(" crossed bangs,","")

#pantyhose
result = result.replace(" pantyhose,","")
result = result.replace(" black pantyhose,","")

#trigger tag for chibi:
result = result + ", small breasts, big head, short limbs, cute, big eyes, small mouth, round face, short stature, tiny hands, tiny feet, cute outfit, oversized head, sparkles, blush stickers, simple shading, pastel colors"
result = result + ", chibi"
print(" ")
print(result)
import pyperclip
pyperclip.copy(result)
print("Dữ liệu đã được sao chép vào bộ nhớ tạm.")