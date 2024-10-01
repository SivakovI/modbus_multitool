from connection.client import Client, ClientType
import asyncio


async def main():
    client = Client(ClientType.TCP, "127.0.0.1", 502)
    await client.client.connect()

    rr = await client.client.read_holding_registers(0, 10, slave=1)
    print(rr.registers)


if __name__ == "__main__":
    asyncio.run(main())
