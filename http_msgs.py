"""
funciones auxiliares para parseo de mensajes http
"""

#convertir mensaje http a diccionario
#str -> dict
def parse_HTTP_message(http_message):
    http_msg = {}

    #dividir entre HEAD y BODY
    head_body = http_message.split("\r\n\r\n")

    #dividir HEAD en sus headers individuales
    head_split = head_body[0].split("\r\n")

    for i in range(len(head_split)):
        if i==0: #para i=0 es la startline
            http_msg["Start-Line"] == head_split[i]
        else:
            line_breakdown = head_split[i].split(":")
            llave = line_breakdown[0]
            valor = line_breakdown[1]
            http_msg[llave] = valor

    if len(head_body) > 1:
        http_msg['Body'] = head_body[1]

    return http_msg

    