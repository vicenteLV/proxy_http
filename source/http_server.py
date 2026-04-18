from email.utils import formatdate
import socket
import json


"""
Funciones auxiliares
"""

def endsWith(word, c):
    if not len(word): return False

    return word[-1]==c 

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
        dict_headers[clave_valor[0]] = clave_valor[1].strip()

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

"""
html_to_string :: str -> str
recibe ruta de archivo html y devuelve su contenido en texto plano
"""
def html_to_str(ruta):
    with open(ruta, "r", encoding="utf-8") as file:
        html_content = file.read()

    return html_content


indexHTML_str = html_to_str("../html/index.html")
errorHTML_str = html_to_str("../html/error.html")
length_indexHTML = len(indexHTML_str.encode()) #largo de cuerpo para mensaje http
length_errorHTML = len(errorHTML_str.encode())
type_encoding_indexHTML = "text/html; charset=utf-8" #para linea de http 'Content-Type:...'

"""
read_json :: str -> dict
recibe ruta del archivo json en formato texto y devuelve el diccionario 
equivalente en python
"""
def read_json(ruta):
    with open(ruta, "r", encoding="utf-8") as file:    
        dict_json = json.load(file)

    return dict_json

    

buff_size = 1024
address = ('localhost', 8000)

print('(Servidor) Creando socket')


client_proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_proxy_socket.bind(address)
client_proxy_socket.listen()

print("Esperando Clientes ...")

while True:
    proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket cliente para el server original

    client_socket, client_socket_ad = client_proxy_socket.accept()

    #recibe peticion
    msg = client_socket.recv(buff_size)
    msg_str = msg.decode()
    parsed_msg = parse_HTTP_message(msg_str)

    #sitios bloqueados
    dict_blocked = read_json("../json/restricciones.json")
    forbbiden_rts = [fb.rstrip("/") for fb in dict_blocked["blocked"]]

    start_line_list = parsed_msg["start-line"].split(" ") #metodo, ruta, version
    method = start_line_list[0]
    ruta = start_line_list[1]
    dominio = parsed_msg["headers"]["Host"].strip()

    ruta_limpia=""
    if ruta.startswith("http"):
        ruta_limpia = ruta.replace("http://","").replace(dominio, "").strip("/")
    else:
        ruta_limpia = ruta.strip("/")

    rt = "http://"+ dominio + "/" + ruta_limpia.lstrip("/")

    if rt in forbbiden_rts:
        response = ""
        response_code = "403"
        response += start_line_list[2]+ " " + response_code + " error\r\n"
        response += "Server: http_server.py\r\n"

        response_date = formatdate(timeval=None, localtime=False, usegmt=True)
        response += f"Date: {response_date}\r\n"                       #fecha
        response += f"Content-Type: {type_encoding_indexHTML}\r\n"     #content type
        response += f"Content-Length: {length_errorHTML}\r\n"          #content length
        response += "Connection: close\r\n"                       #connection
        response += "Acces-Control-Allow-Origin: *\r\n\r\n"            #allowed origins

        response += errorHTML_str

        client_socket.send(response.encode())

        proxy_server_socket.close()
        client_socket.close()


    else:
        #lectura de json
        dict_json = read_json("../json/datos.json")
        consultores_lista = dict_json["Proxy"]
        nombre_q_pregunta = consultores_lista[0]["nombre"]

        dict_headers = parsed_msg["headers"]
        dict_headers["X-ElQuePregunta"] = nombre_q_pregunta

        parsed_msg["headers"] = dict_headers #actualizar headers

        msg_proxy_to_server = create_HTTP_message(parsed_msg)

        original_server_ad = (dominio, 80)

        proxy_server_socket.connect(original_server_ad)
        proxy_server_socket.send(msg_proxy_to_server.encode())

        server_response = proxy_server_socket.recv(buff_size)

        client_socket.send(server_response)
        client_socket.close()
    



