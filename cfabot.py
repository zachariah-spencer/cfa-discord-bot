import discord, requests, datetime, asyncio

# Set intents
intents = discord.Intents.default()
intents.message_content = True

# Define a discord Client object
client = discord.Client(intents=intents)

# A dictionary to simplify getting the role id's for any particular discord role
role_ids = {
  "Operator": -1,
  "Back of House Leader": -1,
  "Back of House": -1,
  "Training Leader": -1,
  "Trainer": -1,
  "Director": -1,
  "Manager": -1,
  "Senior Team Member": 1223305162240557127,
  "Team Member 2": 1223304930455064769,
  "Team Member 1": 1223304192471470180,
  "In Training": 1223421528931172482
}

# A dictionary to simplify getting the channel id's for any particular discord channel
channel_ids = {
    "Shout Outs": 1212541612681338890,
    "News And Updates": 1212541980895092767,
    'Schedule': 1212541482507051100
}

# Code will execute as the bot is initially launched
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Code will execute anytime a members status is updated, in particular if they are assigned any new roles or any roles they currently have are removed
@client.event
async def on_member_update(before, after):
    handle_shout_outs(before, after)

# Handle sending a shout out message whenever a member gains a new role
async def handle_shout_outs(before, after):

    # Is a role being added
    if len(before.roles) < len(after.roles):
        # The user has gained a new role, so lets find out which one
        new_role = next(role for role in after.roles if role not in before.roles)

        # Establish the channel to send shout out messages in
        channel = client.get_channel(channel_ids['Shout Outs'])

        # Send an appropriate shout out message dependent on which role the member is moved to
        if new_role.id == role_ids['In Training']:
            await channel.send('Welcome ' + after.display_name + ' to the team! We\'re excited to have them join the Chick-Fil-A family!')

        elif new_role.id == role_ids['Team Member 1']:
            await channel.send('Congratulations to ' + after.display_name + ' on completing their training! Everbody welcome ' + after.display_name + ' once more to the team! :fire:')
        
        elif new_role.id == role_ids['Team Member 2']:
            await channel.send('Congratulations to ' + after.display_name + ' on reaching Team Member 2! Keep up the good work!')

        elif new_role.id == role_ids['Senior Team Member']:
            await channel.send('Everyone give a huge shout out to ' + after.display_name + ' on reaching Senior Team Member! :fire: :muscle:')

# Run script via a discord bot, passing in the bot's token as the argument -- left blank for github hosting while remaining compliant with discord's security policy.
client.run('[TOKEN GOES HERE]')