import socket

"""
Funciones auxiliares
"""

"""
parse_HTTP_message :: str -> dict
parseo de mensaje http, recibe texto plano y separa contenido según saltos
de linea, devuelve datos del http en un diccionario con claves 'start-line',
'headers', 'body'
"""
def parse_HTTP_message(http_msg):
    dict_http = {}

    #separacion de head y body
    head_body = http_msg.split("\r\n\r\n")
    head = head_body[0].split("\r\n")
    head_start_line = head[0] #start line del mensaje
    head_headers = head[1:] #lista con headers del mensaje

    dict_http["start-line"] = head_start_line

    #diccionario que irá anidado al dict_http
    dict_headers = {}
    for h in head_headers:
        clave_valor = h.split(":")
        dict_headers[clave_valor[0]] = clave_valor[1]

    dict_http["headers"] = dict_headers
    dict_http["body"] = head_body[1]

    return dict_http

"""
create_HTTP_message :: dict -> text
recibe datos de http en formato diccionario y los traspasa a texto plano
"""
def create_HTTP_message(structure):
    http_msg = ""

    http_msg += structure["start-line"]+"\r\n"

    for c, v in structure["headers"].items():
        text = f"{c}: {v}\r\n" #agregar header con valor al texto plano
        http_msg += text

    http_msg += "\r\n"+structure["body"] #se agrega el salto de linea adicional

    return http_msg




buf_size = 1024
address = ('localhost', 8000)

print('(Servidor) Creando socket')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(address)
server_socket.listen()

print("Esperando Clientes ...")

while True:
    client_socket, client_socket_ad = server_socket.accept()

    """
    mensaje_rcv = funcion_recibir_mensaje()"""






    
    



