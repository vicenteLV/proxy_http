from source.http_msgs import parse_HTTP_message

response_test = "HTTP/1.1 200 OK\r\n" \
"Date: Thu, 26 Mar 2026 10:15:00 GMT\r\n" \
"Server: Apache/2.4.41 (Ubuntu)\r\n" \
"Last-Modified: Wed, 25 Mar 2026 12:00:00 GMT\r\n" \
"Content-Type: text/html; charset=UTF-8\r\n" \
"Content-Length: 54\r\n" \
"Connection: keep-alive\r\n\r\n" \
"<html><body><h1>Instalacion Exitosa</h1></body></html>"

assert parse_HTTP_message(response_test), {"Start-Line": "HTTP/1.1 200 OK",
                                           "Date": "Thu, 26 Mar 2026 10:15:00 GMT",
                                           "Server": "Apache/2.4.41 (Ubuntu)",
                                           "Last-Modified": "Wed, 25 Mar 2026 12:00:00 GMT",
                                           "Content-Type": "text/html; charset=UTF-8",
                                           "Content-Length": "54",
                                           "Connection": "keep-alive",
                                           "Body":"<html><body><h1>Instalacion Exitosa</h1></body></html>"
                                           }