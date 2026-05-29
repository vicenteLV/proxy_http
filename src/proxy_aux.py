import json

ctte = "ctte"

"""
str -> str
recibe ruta y agrega / si no está ya"""
def route_norm(ruta):
    ruta_normalizada = ruta
    if not ruta.endswith("/"):
        ruta_normalizada += "/"

    return ruta_normalizada

"""
str str dict-> dict
recibe nombre y descripcion de nuevo header y lo agrega al diccionario de un mensaje http, tambien entregado"""
def add_header(header_name, header_desc, http_dict):
    http_dict["headers_dict"][header_name] = header_desc
    return http_dict


"""
str -> str
recibe ruta a html y lo transforma a texto plano"""
def html_to_str(ruta):
    with open(ruta, "r", encoding="utf-8") as file:
        contenido = file.read()

    return contenido

"""
str -> dict
recibe ruta de json y lo convierte a diccionario"""
def json_load(ruta):
    with open(ruta) as file:
        data = json.load(file)

    return data

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