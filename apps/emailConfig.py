from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str





data_code=b"Bonjour"
encode_data=urlsafe_base64_encode(data_code)
#print(encode_data)

decode_data=urlsafe_base64_decode(encode_data)
print(decode_data)

#convertir une chaine en octest (byte):
text_="bonjour"
text_bytes=force_bytes(text_)
print(text_bytes)
