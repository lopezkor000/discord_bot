import os, requests
from discord import Message, Client, Intents

class TaskManager:
  def __init__(self):
    self.BASEURL = "https://habitica.com/api/v3/"
    self.token = os.environ.get('api_token')
    self.user = os.environ.get('user_id')
    self.headers = {"x-api-user":self.user, "x-api-key":self.token, "x-client":self.user+"-DiscordBot"}

  def add_task(self, text:str, task_type:str, **kwargs):
    params = {
      "text": text,
      "type": task_type
    }
    requests.post(url=self.BASEURL + 'tasks/user', headers=self.headers, data=params)

class TaskBot(Client):
  def __init__(self, *, intents, **options):
    super().__init__(intents=intents, **options)
    self.TaskManager = TaskManager()

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

    if message.content.startswith('$add_task'):
      command = message.content.split(' ')
      task_type = command[1]
      task_name = " ".join(command[2:])
      self.TaskManager.add_task(task_name, task_type)

intents = Intents.default()
intents.message_content = True

client = TaskBot(intents=intents)
TOKEN = os.environ.get('token')
client.run(TOKEN)
