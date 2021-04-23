#!/usr/bin/env python3

import os, time, discord, logzero, requests, json
from logzero import logger
from discord.ext import tasks

# Globals
_client = discord.Client()
_id = 42 # Channel id
_token = os.environ['DISCORD_TOKEN']
_log_maxBytes = 5000 # Log size in bytes
_log_backupCount = 5 # History length
_task_looptime_sec = 10.0 # Checking for updates interval

class QuoteManager():
	def get_quote(self):
		try:
			response = requests.get(self._url)
			json_data = json.loads(response.text)
			quote = json_data[0]['q'] + ' -' + json_data[0]['a']
			return quote

		except Exception as error:
			logger.error(error.with_traceback)

	def __init__(self, url: str = "https://zenquotes.io/api/random", *args, **kwargs) -> None:
		self._url = url


@_client.event
async def on_ready():
    # Prints login time and username to file
    logger.info('We have logged in as {0.user}'.format(_client))
    # Starts Check_For_Updates task
    Check_For_Updates.start()

@_client.event
async def on_message(message):
    # Check if the sender is the bot
	if message.author == _client.user:
		return

	if message.content.startswith('/getquote'):
		# Get quote data
		await message.channel.send(QuoteManager().get_quote())

# Task check according to _task_looptime_sec
@tasks.loop(seconds=_task_looptime_sec)
async def Check_For_Updates():
    try:
		# Add logic here
        # Set channel id before sending
        channel = _client.get_channel(_id)
        await channel.send(f"Datafrom task")
        
    except Exception as error:
        logger.error(error.with_traceback)


def main():

    # Disable jason formated output by putting false
    logzero.json(False)

    # rotating logfile
    logzero.logfile("log.txt",
        maxBytes=_log_maxBytes,
        backupCount=_log_backupCount)

    # Start of program
    logger.info("Starting Discord BOT")

    # Setting up discord client
    _client.run(_token)

if __name__ == "__main__":
    main()
