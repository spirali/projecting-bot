# Discord Projecting Bot

This is a discord bot designed to create a realtime exhibition from images
posted on a discord.

The bot downloads all images posted to a discord channels 
and show them on the local machine (e.g. on the projector).

Images are chosen randomly, but the bot remembers how many of each image was shown
and probability of more shown images exponentially decays.

## Typical usage

For the following configuration we assume that we have connected a second monitor (or a projector).

```commanline
python3 main.py <DISCORD_BOT_KEY> --display=1
```

## Note

Use in a trusted environment; the code was written for a specific use case
and it is not tested for usage on a public servers.