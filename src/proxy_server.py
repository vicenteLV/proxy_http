import socket
import proxy_aux
from datetime import datetime


data = proxy_aux.json_load("../json/data.json")
forbidden = proxy_aux.json_load("../json/prohibidos.json")

#cttes para metodos del servidor
CODIGOS = data["Codigos"]
VERSION_HTTP = data["VERSION_HTTP"]
CHARSET = data["CHARSET"]
NOMBRE = data["NOMBRE"]

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
    response_text = proxy_aux.html_to_str(ruta_response)
    response_len = len(response_text.encode())
    diccionario_headers_response["Content-Length"] = f"{response_len}"

    diccionario_headers_response["Connection"] = connection
    diccionario_headers_response["Acces-Control-Allow-Origin"] = "*"
    diccionario_headers_response["X-ElQuePregunta"] = NOMBRE

    diccionario_response["headers_dict"] = diccionario_headers_response
    diccionario_response["BODY"] = response_text

    response = proxy_aux.create_http_message(diccionario_response)

    return response 
    



if __name__ == "__main__" :
    buffer_size = 1024
    proxy_socket_address = ("localhost", 5000)

    print("##### Creando sockets #####\n")
    #socket para escuchar a cliente
    client_to_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_to_proxy.bind(proxy_socket_address)
    client_to_proxy.listen(3)

    print("##### Esperando clientes #####\n")

    while True:
        client_socket, client_socket_address = client_to_proxy.accept()
        recvd_msg = client_socket.recv(1024)

        print(recvd_msg)
        client_query_dict = proxy_aux.parse_HTTP_message(recvd_msg.decode())

        version_http_consulta = client_query_dict["startline"].split(" ")[2] #posible eliminacion

        

        server_host = client_query_dict["headers_dict"]["Host"]
        #proxy to server socket
        proxy_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        puerto = 80     #reservado para http
        server_address = (server_host, puerto)
        proxy_to_server.connect(server_address)
        proxy_to_server.send(recvd_msg)
        recvd_server = proxy_to_server.recv(buffer_size)       #mensaje recibido de servidor

        response = recvd_server
        print(response)

        client_socket.send(response)
        client_socket.close()

        print(f"Conexión con {client_socket_address} ha sido cerrada\n")



    
    


