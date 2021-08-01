import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from gtts import gTTS
import os
import os.path
import random

image_types = ["png", "jpeg", "gif", "jpg"]


class TextToSpeech(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.client.user:
            return
        for voice_client in self.client.voice_clients:
            num_members = len(voice_client.channel.members)
            if num_members <= 1:
                return await voice_client.disconnect()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def tts(self, ctx, *, arg):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if not voice:
            if not ctx.author.voice:
                await ctx.send("User must be in a voice channel")
                return
            channel = ctx.author.voice.channel
            await channel.connect()
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        sound = gTTS(arg)
        sound.save("tts.wav")

        if not voice.is_playing():
            voice.play(FFmpegPCMAudio("tts.wav"))
        else:
            await ctx.send("Something is playing right now!")
            return

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_connected():
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("bot is not connected")

    @commands.command()
    async def play(self, ctx, url : str):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        settings = {
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'song.%(ext)s',
        }

        if not voice:
            if not ctx.author.voice:
                await ctx.send("User must be in a voice channel")
                return
            channel = ctx.author.voice.channel
            await channel.connect()
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        with YoutubeDL(settings) as ydl:
            ydl.download([url])

        if not voice.is_playing():
            voice.play(FFmpegPCMAudio("song.mp3"))
            voice.is_playing()
            await ctx.send(f"Now playing {url}")
        else:
            await ctx.send("Already playing song")
            return

    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if not voice or not voice.is_playing():
            await ctx.send("Music is not playing")
            return
        voice.stop()

    @commands.command()
    async def cat(self, ctx):
        num_files = len(os.listdir('./cats/'))
        rand = random.randint(0, num_files-1)
        await ctx.send(file=discord.File('cats/' + str(rand) + '.jpg'))


def setup(client):
    client.add_cog(TextToSpeech(client))
