from discord.ext import commands
from datetime import datetime
from typing import Optional
import discord
import os

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    def is_guild_owner():
        def predicate(ctx):
            return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
        return commands.check(predicate)

    @commands.command(name="userinfo", aliases=["memberinfo", "ui", "mi"])
    @commands.guild_only()
    @commands.check_any(commands.is_owner(), is_guild_owner())
    async def user_info(self, ctx, target: Optional[discord.Member]):
        # If no target is given, use the user who wrote the command
        target = target or ctx.author

        embed = discord.Embed(
            title="Server Information",
            colour = target.colour,
            timestamp = datetime.utcnow()
        )

        embed.set_thumbnail(url=target.avatar_url)

        fields = [
            ("Name", str(target), True),
            ("ID", target.id, True),
            ("Bot?", target.bot, True),
            ("Top role", target.top_role.mention, True),
            ("Status", str(target.status).title(), True),
            ("Activity", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", True),
            ("Created at", target.created_at.strftime("%Y-%m-%d %H:%M:%S"), True),
            ("Joined at", target.joined_at.strftime("%Y-%m-%d %H:%M:%S"), True),
            ("Boosted", bool(target.premium_since), True)
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_footer(text=f"Generated by {ctx.author.display_name}")

        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", aliases=["guildinfo", "si", "gi"])
    @commands.guild_only()
    @commands.check_any(commands.is_owner(), is_guild_owner())
    async def server_info(self, ctx):
        embed = discord.Embed(
            title="Server Information",
            colour = ctx.guild.owner.colour,
            timestamp = datetime.utcnow()
        )

        statuses = {
            "online": len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
            "idle": len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
            "dnd": len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
            "offline": len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members))),
        }

        fields = [
            ("ID", ctx.guild.id, True),
            ("Name", ctx.guild.name, True),
            ("Region", ctx.guild.region, True),
            ("Owner", ctx.guild.owner, True),
            ("Created At", ctx.guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), True),
            ("Members", len(ctx.guild.members), True),
            ("Statuses", f":green_circle: {statuses['online']} :orange_circle: {statuses['idle']} :red_circle: {statuses['dnd']} :black_circle: {statuses['offline']} ", True),
            ("Categories", len(ctx.guild.categories), True),
            ("Emoji Count", len(ctx.guild.emojis), True),
            ("Text Channels", len(ctx.guild.text_channels), True),
            ("Voice Channels", len(ctx.guild.voice_channels), True),
            ("Roles", len(ctx.guild.roles), True),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_footer(text=f"Generated by {ctx.author.display_name}")

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Info(client))
