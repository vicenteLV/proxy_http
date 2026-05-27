import socket
import proxy_aux
from datetime import datetime


#cttes para metodos del servidor
CODIGOS = {
    "200": "OK"
}
VERSION_HTTP = "HTTP/1.1"
CHARSET = "utf-8"
NOMBRE = "Vicente López Vergara"

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

    print("##### Creando socket de servidor #####\n")

    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(proxy_socket_address)
    proxy_socket.listen(3)

    print("##### Esperando clientes #####\n")

    while True:
        client_socket, client_socket_address = proxy_socket.accept()
        recvd_msg = client_socket.recv(1024)

        print(recvd_msg)
        diccionario = proxy_aux.parse_HTTP_message(recvd_msg.decode())
        version_http_consulta = diccionario["startline"].split(" ")[2]

        response = create_response("200", "../html/index.html", version=version_http_consulta)
        print(response)

        client_socket.send(response.encode())
        client_socket.close()

        print(f"Conexión con {client_socket_address} ha sido cerrada\n")



    
    


