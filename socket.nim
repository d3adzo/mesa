import net, os

proc cSock() = 
    var socket = newSocket()
    socket.bindAddr(Port(1234))
    socket.listen()
    var client: Socket
    var address = ""

    socket.acceptAddr(client, address)
    echo("Client connected from: ", address)



cSock()

