from django.shortcuts import render
import asyncio, os

def index(request):
    context = {}
    
    return render(request, 'remind_app/index.html', context)

def submit(request):
    context = {}
    user_id = request.POST['user_id']
    data = request.POST['data']
    text = request.POST['text']
    response = f'{user_id}&&&{data}&&&{text}'
    
    async def tcp_echo_client(message):
        reader, writer = await asyncio.open_connection(
            os.environ.get('SOCKET_SERVER_IP'), os.environ.get('SOCKET_SERVER_PORT'))
            
        writer.write(message.encode())
        await writer.drain()
        
        writer.close()
        await writer.wait_closed()

    asyncio.run(tcp_echo_client(response))

    return render(request, 'remind_app/done.html', context)