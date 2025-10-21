import asyncio  # biblioteca assíncrona do Python usada para servidores concorrentes sem threads pesadas
import signal  # para capturar sinais do sistema (ex.: SIGINT) e encerrar graciosamente.
import sys  # usado apenas para sair no final em caso de exceção.

# listas que definem portas e banners/respostas. Facilita adicionar/remover serviços.

# Configuração: portas e banners
TCP_SERVICES = [
    (22, "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu1\r\n"),  # simula SSH
    (
        80,
        "HTTP/1.1 200 OK\r\nServer: SimplePyHTTP/0.1\r\n\r\nHello from HTTP!\n",
    ),  # HTTP-like banner
    (8080, "MyApp/1.2.3\r\nWelcome to the app!\n"),  # app custom banner
    (2222, "FakeSSH-1.0-Faker\r\n"),
    (9000, "CustomService v0.9\nType 'help' for commands\n"),
]

UDP_SERVICES = [
    (53, b"\x12\x34" + b"FAKE-DNS-REPLY"),  # resposta binária simulada (porta 53)
    (161, b"\x30\x82" + b"FAKE-SNMP"),  # resposta binária para SNMP-like
    (9999, b"OK"),  # UDP simples
]

clients = (
    []
)  # lista global que registra pares (addr, writer) para permitir fechamento limpo das conexões abertas quando o servidor termina.


async def handle_tcp(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter, banner: bytes
):
    addr = writer.get_extra_info("peername")
    clients.append((addr, writer))
    try:
        # envia banner (se houver)
        if banner:
            writer.write(banner)
            await writer.drain()

        # pequeno loop eco para interação opcional
        while True:
            data = await reader.read(1024)
            if not data:
                break
            # encerra conexão se receber "quit"
            if data.strip().lower() in (b"quit", b"exit"):
                break
            # responde echo simples
            writer.write(b"Echo: " + data)
            await writer.drain()
    except (asyncio.CancelledError, ConnectionResetError):
        pass
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass
        if (addr, writer) in clients:
            clients.remove((addr, writer))


async def start_tcp_servers(loop):
    servers = []
    for port, banner_text in TCP_SERVICES:
        banner = banner_text.encode() if isinstance(banner_text, str) else banner_text
        server = await asyncio.start_server(
            lambda r, w, b=banner: handle_tcp(r, w, b),
            "127.0.0.1",
            port,
        )
        servers.append(server)
        addr = server.sockets[0].getsockname()
        print(
            f"[TCP] Servidor simulado escutando em {addr}  (banner: {banner.decode(errors='ignore').splitlines()[0]})"
        )
    return servers


class UDPProtocol(asyncio.DatagramProtocol):
    def __init__(self, reply_bytes: bytes, port: int):
        self.reply = reply_bytes
        self.port = port

    def connection_made(self, transport):
        self.transport = transport
        print(
            f"[UDP] Servidor simulado escutando em {transport.get_extra_info('sockname')}"
        )

    def datagram_received(self, data, addr):
        print(f"[UDP:{self.port}] recebido {len(data)} bytes de {addr} -> respondendo")
        # envia a resposta predefinida
        self.transport.sendto(self.reply, addr)


async def start_udp_servers(loop):
    transports = []
    for port, reply in UDP_SERVICES:
        transport, proto = await loop.create_datagram_endpoint(
            lambda r=reply, p=port: UDPProtocol(r, p), local_addr=("127.0.0.1", port)
        )
        transports.append((transport, proto))
    return transports


async def main():
    loop = asyncio.get_running_loop()

    tcp_servers = await start_tcp_servers(loop)
    udp_servers = await start_udp_servers(loop)

    # mantém o loop rodando até receber sinal de término
    stop = asyncio.Event()

    def _on_signal():
        print("\nSinal de término recebido. Encerrando servidores...")
        stop.set()

    loop.add_signal_handler(signal.SIGINT, _on_signal)
    loop.add_signal_handler(signal.SIGTERM, _on_signal)

    await stop.wait()

    # fechar servidores TCP
    for s in tcp_servers:
        s.close()
        await s.wait_closed()
    # fechar transports UDP
    for t, p in udp_servers:
        t.close()

    # fechar clientes abertos
    for addr, writer in list(clients):
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Encerrado pelo usuário.")
        sys.exit(0)
