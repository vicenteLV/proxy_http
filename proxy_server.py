import socket
from datetime import datetime

#cttes para metodos del servidor
CODIGOS = {
    "200": "OK"
}
VERSION_HTTP = "HTTP/1.1"
CHARSET = "utf-8"
NOMBRE = "Vicente López Vergara"

"""
str -> str
recibe ruta a html y lo transforma a texto plano"""
def html_to_str(ruta):
    with open(ruta, "r", encoding=CHARSET) as file:
        contenido = file.read()

    return contenido


"""
str-> dict
parseo de mensaje http a diccionario"""
def parse_HTTP_message(http_msg):
    print("--- PARSE INICIADO ---\n")

    dict_http = {}
    #dividir entre HEAD y BODY
    http_split = http_msg.split("\r\n\r\n")
    http_head = http_split[0]
    http_body = http_split[1]

    #separar startline de headers
    http_head_split = http_head.split("\r\n")

    #para diccionario
    dict_http["startline"] = http_head_split[0]
    dict_http["headers_dict"] = {}
    dict_http["BODY"] = http_body

    headers_list = http_head_split[1:]
    for h in headers_list:
        partes = h.split(":")
        header_name = partes[0].strip()
        header_desription = partes[1].strip()
        dict_http["headers_dict"][header_name] = header_desription

    print("--- PARSE TERMINADO ---\n")

    return dict_http

"""
dict -> str
lee diccionario de http y lo pasa a formato mensaje"""
def create_http_message(dicc):
    startline = dicc["startline"]
    headers = dicc["headers_dict"] #diccionario

    texto_headers = ""
    for nombre, descripcion in headers.items():
        texto_headers += f"{nombre}: {descripcion}\r\n"

    texto_headers += "\r\n"

    body = dicc["BODY"]

    HTTP_msg = startline + "\r\n" + texto_headers + body

    return HTTP_msg

"""
str str (str) (str) (str)-> str
crea respuesta en formato http"""
def create_response(codigo, ruta_response, version=VERSION_HTTP, charset=CHARSET, server="proxy_server/1.0", content_type="text/html", connection="keep-alive"):
    #para fecha
    now = datetime.now()
    diccionario_response = {}

    #startline
    startline = f"{version} {codigo} {CODIGOS[codigo]}"
    diccionario_response["startline"] = startline

    #headers
    diccionario_headers_response = {}
    diccionario_headers_response["Server"] = server

    #fecha
    day_name = now.strftime("%A")[0:3]
    month_name = now.strftime("%B")[0:3]
    time = now.strftime("%H:%M:%S GMT")
    diccionario_headers_response["Date"] = f"{day_name}, {now.day} {month_name} {now.year} {time}"

    diccionario_headers_response["Content_Type"] = f"{content_type}: charset={charset}"      #Content-Type

    #largo
    response_text = html_to_str(ruta_response)
    response_len = len(response_text.encode())
    diccionario_headers_response["Content-Length"] = f"{response_len}"

    diccionario_headers_response["Connection"] = connection
    diccionario_headers_response["Acces-Control-Allow-Origin"] = "*"
    diccionario_headers_response["X-ElQuePregunta"] = NOMBRE

    diccionario_response["headers_dict"] = diccionario_headers_response
    diccionario_response["BODY"] = response_text

    response = create_http_message(diccionario_response)

    return response 
    



if __name__ == "__main__" :
    buffer_size = 1024
    proxy_socket_address = ("localhost", 5000)

    print("##### Creando socket de servidor #####\n")

    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(proxy_socket_address)
    proxy_socket.listen(3)

    print("##### Esperando clientes #####\n")

    while True:
        client_socket, client_socket_address = proxy_socket.accept()
        recvd_msg = client_socket.recv(1024)

        print(recvd_msg)
        diccionario = parse_HTTP_message(recvd_msg.decode())
        version_http_consulta = diccionario["startline"].split(" ")[2]

        #print(diccionario)
        print("-----------------")
        mensaje_reverse = create_http_message(diccionario)
        print(f"HTTP:\n{mensaje_reverse}")

        response = create_response("200", "html/index.html", version=version_http_consulta)
        print(response)

        client_socket.send(response.encode())
        client_socket.close()

        print(f"Conexión con {client_socket_address} ha sido cerrada\n")



    
    


