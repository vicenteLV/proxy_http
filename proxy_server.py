import socket

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

        #print(diccionario)
        print("-----------------")
        mensaje_reverse = create_http_message(diccionario)
        print(f"HTTP:\n{mensaje_reverse}")

        response = ""

        client_socket.send(response.encode())
        client_socket.close()

        print(f"Conexión con {client_socket_address} ha sido cerrada\n")



    
    


