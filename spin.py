import discord
from discord.ext import commands
from discord import app_commands
import os
import aiofiles
import io
import random
import asyncio


intents = discord.Intents.default()
intents.messages = True  
intents.message_content = True  


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents=intents)
        self.synced = False

    async def on_ready(self):
        if not self.synced:
            await bot.tree.sync()  
            self.synced = True
        print(f"Bot {self.user.name} olarak giriş yaptı!")

bot = MyBot()


TXT_FOLDER_PATH = "./txt_files"


def log_debug(message):
    print(f"[DEBUG] {message}")


async def search_in_file(file_path, url):
    results = []
    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
            async for line in file:
           
                if url.lower() in line.lower():
                    results.append(line.strip())
    except Exception as e:
        log_debug(f"xx {file_path}: {str(e)}")
    return results


@bot.tree.command(name="search", description="xx")
async def search(interaction: discord.Interaction, url: str):

    await interaction.response.defer()  

    
    results = []

    try:
       
        log_debug(f"Scanned: {TXT_FOLDER_PATH}")
        

        tasks = []
        for file_name in os.listdir(TXT_FOLDER_PATH):
            if file_name.endswith(".txt"):
                file_path = os.path.join(TXT_FOLDER_PATH, file_name)
                tasks.append(search_in_file(file_path, url))  
        
      
        results = await asyncio.gather(*tasks)

       
        results = [line for result in results for line in result]


        if results:
            selected_results = random.sample(results, min(20, len(results))) 

         
            if len("\n".join(selected_results)) > 2000:  
                response = "\n".join(selected_results)
                with io.StringIO(response) as file_stream:
                    await interaction.followup.send(content="Big files xd:", file=discord.File(file_stream, filename="results.txt"))
            else:
                await interaction.followup.send(f"Scanned:\n" + "\n".join(selected_results))
        else:
            await interaction.followup.send(f"'{url}' wich not found.")
    except Exception as e:
        log_debug(f"Hata oluştu: {str(e)}")
        await interaction.followup.send(f"Bir hata oluştu: {str(e)}")

TOKEN = "your_bot_token"  

bot.run(TOKEN)
