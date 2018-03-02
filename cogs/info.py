import datetime
import platform
import time
import discord
from discord.ext import commands
from cogs.utils.tools import *

about_description = """
**H-hello!~~**
My name is Godavaru, but you can call me Godava, as many people do. I was named after a community guild, which I am not directly linked to anymore, but you may check out if you wish using the link [here](https://discord.gg/bxDV2yu)! I-I mean, It's not like I want you to join or anything... baka!
Below, you can find a link to the actual support guild for me, where you may tell my mom if I misbehave and throw errors around again. :< Below, you can also find a link to invite me, if you so wish! I promise that I will do you good!
I have quite a few features; I can list them for you now!

**__I come with:__**
-> Action Commands (hug, kiss, even some lewd ones :eyes:)
-> Moderation Commands (ban, kick, prune, and more!)
-> Utility Commands (urbandictionary search, normal dictionary, complex maths, and much more!)
-> Fun Commands (slots, trivia, and other miscellanious features to keep you occupied!)
-> Information Commands (userid lookup, discriminator lookup, role information, and more!)

Check all my commands with `g_help` or `godavaru help`!
"""


class Info:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roleinfo(self, ctx, *, role: discord.Role):
        """Get information on a role.
        Note that the role name is case sensitive. If the role name is `Member`, then you must pass the role argument as `Member` and not `member`."""
        em = discord.Embed(title="Role Info", description="Information for role **{}**".format(role.name),
                           color=role.color)
        em.add_field(name="Permissions", value=role.permissions.value, inline=True)
        em.add_field(name="Colour", value=role.colour, inline=True)
        em.add_field(name="Managed", value=role.managed, inline=True)
        em.add_field(name="Hoisted", value=role.hoist, inline=True)
        em.add_field(name="Role ID", value=role.id, inline=True)
        em.add_field(name="Position", value=role.position, inline=True)
        em.add_field(name="Mentionable", value=role.mentionable, inline=True)
        em.add_field(name="Creation Date", value=role.created_at.strftime('%a %d %b %Y at %H:%M:%S'), inline=True)
        em.set_thumbnail(url="https://i.imgur.com/La0f2NY.png")
        await ctx.send(embed=em)

    @commands.group()
    async def about(self, ctx):
        """Show the stuff about me! I promise I'm interesting uwu"""
        member_count = 0
        server_count = len(self.bot.guilds)
        for server in self.bot.guilds:
            for _ in server.members:
                member_count += 1
        em = discord.Embed(title='About Godavaru!', description=about_description, color=0x9B59B6)
        em.add_field(name='Version', value=self.bot.version + '\n' + self.bot.version_info, inline=False)
        em.add_field(name='Servers', value=str(server_count))
        em.add_field(name='Users', value=f'{member_count} total/{len(self.bot.users)} unique')
        em.add_field(
            name='Invite Me!',
            value='[Click Here](https://goo.gl/chLxM9)\n[Support guild](https://discord.gg/ewvvKHM)\n[Patreon page](https://www.patreon.com/desii)',
            inline=False)
        em.set_footer(text="Made with love <3")
        em.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/311810096336470017/fa4daf0662e13f25bdbd09fd18bdc36d.png")
        await ctx.send(embed=em)

    @about.command()
    async def credits(self, ctx):
        """List the users that have been credited for this bot."""
        creds = [
            '267207628965281792|Main developer',
            '99965250052300800|Secondary developer',
            '132584525296435200|Web Developer',
            '188663897279037440|Provided python basic knowledge at the beginning',
            '170991374445969408|Helped with early on commands & initial hosting'
        ]
        mods = discord.utils.get(self.bot.get_guild(315251940999299072).roles, id=315252093239820289).members
        full_credits = ""
        for i in range(len(creds)):
            splitted = creds[i].split('|')
            user_id = int(splitted[0])
            desc = splitted[1]
            full_credits += f'**{self.bot.get_user(user_id)}** - {desc}\n'
        em = discord.Embed(description=full_credits, color=ctx.author.color)
        em.set_author(name='Credited users', icon_url=ctx.me.avatar_url)
        await ctx.send(embed=em)

    @commands.command(aliases=["links"])
    async def invite(self, ctx):
        """Get some important links about me."""
        em = discord.Embed(
            description='Here are some useful links for the Godavaru bot. If you have any questions at all, '
                        + f'feel free to join the support guild and tag {self.bot.get_user(267207628965281792)} with your questions!\n'
                        + 'Below you can also find the links to the support guild itself and the Patreon URL. '
                        + 'Thanks for using the bot!',
            color=0x9B59B6)
        em.set_author(
            name='Useful Links for Godavaru!',
            icon_url='https://cdn.discordapp.com/avatars/311810096336470017/fa4daf0662e13f25bdbd09fd18bdc36d.png')
        em.add_field(name='Invite URL', value='http://is.gd/godavaru')
        em.add_field(name='Support Guild', value='https://discord.gg/ewvvKHM')
        em.add_field(name="Patreon URL", value='https://patreon.com/desii')
        em.add_field(name="Github", value="https://github.com/Desiiii/Godavaru")
        await ctx.send(embed=em)

    @commands.command()
    async def ping(self, ctx):
        """Check my response time and my websocket ping"""
        before = datetime.utcnow()
        ping_msg = await ctx.send(":mega: If you see this message you are cool... jk. It's just a ping message.")
        ping = (datetime.utcnow() - before) * 1000
        before2 = time.monotonic()
        await (await self.bot.ws.ping())
        after = time.monotonic()
        ping2 = (after - before2) * 1000
        await ping_msg.edit(
            content=":mega: Pong! My ping is {:.2f}ms! `Websocket: {:.0f}ms`".format(ping.total_seconds(), ping2))

    def get_bot_uptime(self, *, brief=False):
        now = datetime.utcnow()
        delta = now - self.bot.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if not brief:
            if days:
                fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
            else:
                fmt = '{h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{h}h {m}m {s}s'
            if days:
                fmt = '{d}d ' + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    @commands.command(pass_context=True)
    async def info(self, ctx):
        """Show some of the more statistical information about me.
        This information includes the current version(s), number of commands, amount of servers, channels, users, uptime, and average websocket ping."""
        commands = len(self.bot.commands)
        cogs = len(self.bot.cogs)
        version = discord.__version__
        before = time.monotonic()
        await (await self.bot.ws.ping())
        after = time.monotonic()
        ping = (after - before) * 1000
        pversion = platform.python_version()
        server_count = 0
        member_count = 0
        channel_count = 0
        for server in self.bot.guilds:
            server_count += 1
            for _ in server.channels:
                channel_count += 1
            for _ in server.members:
                member_count += 1
        await ctx.send("""```prolog
=========[ Bot Information ]=========

Commands           :  {0}
Cogs               :  {1}
Version            :  {2}
DiscordPY Version  :  {3}
Python Version     :  {4}
Websocket Ping     :  {5:.0f}ms
Uptime             :  {6}

=========[ Guild Information ]=========

Guilds             :  {7}
Users              :  {8}
Channels           :  {9}
Hostname           :  {10}
OS                 :  {11}```""".format(commands, cogs, self.bot.version, version, pversion, ping,
                                          self.get_bot_uptime(), server_count, member_count, channel_count,
                                                      platform.node(), platform.system()))

    @commands.command()
    async def avatar(self, ctx, *, user: discord.Member):
        """Get a user-friendly image of the specified user's avatar.
        If no user is specified, the user is the author.
        You can also search for a user's name. The name can have an optional discriminator argument, e.g. “Jake#0001” or “Jake” will both do the lookup. However the former will give a more precise result. Note that the discriminator must have all 4 digits for this to work.
        If a nickname is passed, then it is looked up via the nickname. Note however, that a nickname + discriminator combo will not lookup the nickname but rather the username + discriminator combo due to nickname + discriminator not being unique."""
        avi = user.avatar_url
        avi = avi.replace("gif?size=1024", "gif?size=1024&.gif")
        avi = avi.replace("webp?size=1024", "png?size=1024")
        embed = discord.Embed(title=user.display_name + "'s avatar!", description="Click [here](" + avi + ")!",
                              color=ctx.author.color).set_image(url=avi).set_footer(icon_url=avi,
                                                                                    text="Requested by " + ctx.author.display_name)
        await ctx.send(embed=embed)

    @commands.command(aliases=["guild", "ginfo", "server", "serverinfo", "sinfo"])
    async def guildinfo(self, ctx):
        """Get information on the guild you are currently in!"""
        g = ctx.guild
        num = 0
        if ctx.channel.permissions_for(ctx.me).external_emojis:
            num = 1
        online = len([m.name for m in g.members if m.status == discord.Status("online")])
        idle = len([m.name for m in g.members if m.status == discord.Status("idle")])
        dnd = len([m.name for m in g.members if m.status == discord.Status("dnd")])
        guild_embed = discord.Embed(
            title=g.name,
            description=f"Guild ID: {g.id}",
            color=ctx.author.color
        ).set_thumbnail(
            url=g.icon_url
        ).add_field(
            name="Created At",
            value=g.created_at.strftime("%A %d %B %Y at %H:%M:%S"),
            inline=False
        ).add_field(
            name="Users - "+str(len(g.members)),
            value=f"{get_status_emoji('online', num)} Online: {online}\n"
                  + f"{get_status_emoji('idle', num)} Idle: {idle}\n"
                  + f"{get_status_emoji('dnd', num)} DnD: {dnd}",
            inline=False
        ).add_field(
            name="Days Since Creation",
            value=(datetime.now() - g.created_at).days
        ).add_field(
            name="Guild Region:",
            value=g.region
        ).add_field(
            name="AFK Timeout",
            value=f"{int(g.afk_timeout/60)} minutes"
        ).add_field(
            name="Owner",
            value=str(g.owner)
        ).add_field(
            name="Total Channels",
            value=len(g.channels)
        ).add_field(
            name="Category Channels",
            value=len([c.name for c in g.channels if isinstance(c, discord.CategoryChannel)])
        ).add_field(
            name="Text Channels",
            value=len([c.name for c in g.channels if isinstance(c, discord.TextChannel)])
        ).add_field(
            name="Voice Channels",
            value=len([c.name for c in g.channels if isinstance(c, discord.VoiceChannel)])
        ).add_field(
            name="Verification Level",
            value=g.verification_level
        ).add_field(
            name="Explicit Content Filter",
            value=g.explicit_content_filter
        ).add_field(
            name=f"Roles - {len(g.roles)-1}",
            value=", ".join([r.name for r in sorted(g.roles, key=lambda x: -x.position) if not r.is_default()])
        )
        await ctx.send(embed=guild_embed)

    @commands.command(aliases=["user", "uinfo"])
    async def userinfo(self, ctx, *, user: discord.Member = None):
        """Display information about a user."""
        if not user:
            user = ctx.author
        em = discord.Embed(color=user.color)
        em.add_field(name="Joined At:", value=user.joined_at.strftime("%A %d %B %Y at %H:%M:%S"), inline=False)
        em.add_field(name="Created At:", value=user.created_at.strftime("%A %d %B %Y at %H:%M:%S"), inline=False)
        em.add_field(name="Days Since Join:", value=(datetime.now() - user.joined_at).days)
        em.add_field(name="Days Since Creation:", value=(datetime.now() - user.created_at).days)
        em.add_field(name="Status:", value=user.status)
        em.add_field(name="Nickname:", value=user.nick)
        em.add_field(name="Voice Channel:", value=user.voice.channel if user.voice is not None else None)
        em.add_field(name="Is Bot:", value=user.bot)
        em.add_field(name="Game:", value=user.game, inline=False)
        em.add_field(name="Top Role:", value=user.top_role.name)
        em.add_field(name="Highest Position:", value=user.top_role.position)
        em.add_field(name=f"Roles [{len(user.roles) - 1}]:", value=", ".join(
            [r.name for r in sorted(user.roles, key=lambda x: -x.position) if not r.is_default()]))
        em.set_thumbnail(url=user.avatar_url.replace("?size=1024", ""))
        em.set_author(name=f"{user} ({user.id})", icon_url=user.avatar_url.replace("?size=1024", ""),
                      url=user.avatar_url.replace("?size=1024", ""))
        em.set_footer(text=f"Requested by {ctx.author.display_name}",
                      icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
        await ctx.send(embed=em)

    @commands.command()
    async def status(self, ctx, *, user: discord.Member):
        """Display the current status of the specified member.
        If the member is not specified or an invalid member argument is passed, the member is the author."""
        if len(ctx.message.mentions) == 0:
            user = ctx.message.author
            a = ", you are "
        else:
            user = ctx.message.mentions[0]
            a = " is "
        if user.game is None:
            game = "Nothing."
            footer = "Maybe you should get out into the world. Meet some people. Could be good for you."
        else:
            game = str(user.game)
            footer = "Hope it's a fun one!"
        em = discord.Embed(title=user.display_name + a + "playing:", description="`{}`".format(game), color=user.color)
        em.set_footer(text=footer)
        await ctx.send(embed=em)

    @commands.command()
    async def changelog(self, ctx):
        """Check the most recent changelog for all of the newer features!"""
        changelog_channel = discord.utils.get(discord.utils.get(self.bot.guilds, id=315251940999299072).channels,
                                             id=315602734235516928)
        async for m in changelog_channel.history(limit=1):
            changelog = m.clean_content
            desii = m.author
            last_update = m.created_at
        em = discord.Embed(description=changelog, color=ctx.message.author.color)
        em.set_author(icon_url=desii.avatar_url.replace("?size=1024", ""),
                      name="Found the latest changelog from my support guild!")
        em.timestamp = last_update
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Info(bot))
