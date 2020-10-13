import socket
import select

HEADER_LENGTH = 10

IP = "127.0.0.1" #Colocar o ipv4 do server caso esteja usando um vpn
PORT = 1234

# Criar socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind do server
server_socket.bind((IP, PORT))

# Server escutando para receber novas conexões
server_socket.listen()

# Lista de sockets
lista_de_sockets = [server_socket]

# Lista de clientes conectados
clientes = {}

print(f'Esperando conexões no IP {IP}:{PORT}...')

# Trata as mensagens recebidas
def receber_mensagem(client_socket):

    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        # Converte o header para valor inteiro
        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False

while True:

    read_sockets, _, exception_sockets = select.select(lista_de_sockets, [], lista_de_sockets)


    for notified_socket in read_sockets:

        if notified_socket == server_socket:

            client_socket, client_address = server_socket.accept()

            # O cliente envia o username de cara
            usuario = receber_mensagem(client_socket)

            # Se falso - client se desconectou antes de enviar o username
            if usuario is False:
                continue

            lista_de_sockets.append(client_socket)

            clientes[client_socket] = usuario

            print('Aceitando nova conexão de {}:{}, username: {}'.format(*client_address, usuario['data'].decode('utf-8')))

        # Else socket existente está enviando uma mensagem
        else:

            # Receber mensagem
            message = receber_mensagem(notified_socket)

            # Se falso, cliente desconectou
            if message is False:
                print('Conexão terminada com: {}'.format(clientes[notified_socket]['data'].decode('utf-8')))

                lista_de_sockets.remove(notified_socket)

                del clientes[notified_socket]

                continue

            usuario = clientes[notified_socket]

            print(f'Mensagem recebida de {usuario["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Enviar mensagem de um usuário para os outros
            for client_socket in clientes:
                
                #Não enviar para si mesmo
                if client_socket != notified_socket:
                    client_socket.send(usuario['header'] + usuario['data'] + message['header'] + message['data'])


    for notified_socket in exception_sockets:

        lista_de_sockets.remove(notified_socket)

        del clientes[notified_socket]
