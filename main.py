import discord, os
from discord import Message, Client, Intents

class TaskManager:
  def __init__(self):
    pass

class TaskBot(Client):
  async def on_ready(self):
    print(f'Logged on as {self.user}')

  async def on_message(self, message:Message):
    if message.author == self.user:
      return

    if not message.content.startswith('$'):
      return
    
    print(f'Command from {message.author}: {message.content}')
    
    if message.content.startswith('$del'):
      try:
        amount = int(message.content.split(' ')[-1]) + 1

        if amount < 0:
          message.channel.send('Need a positive number')
          return
        
        messages = [message async for message in message.channel.history(limit=amount)]
        
        await message.channel.delete_messages(messages)
      except Exception as e:
        print('Error:', e)

intents = Intents.default()
intents.message_content = True

client = TaskBot(intents=intents)
TOKEN = os.environ.get('token')
client.run(TOKEN)
