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

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await send_time_off_reminder()
    print(datetime.datetime.now().strftime("%H:%M UTC %a"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #FIXME: Contact Fourth regarding External Customer Canonical ID's in HTTP requests. See about getting one or finding out what ours is.
    if message.content.startswith('$hs'):
        await message.channel.send('HotSchedules RESTful API HTTP Request')
        #r = requests.get('https://httpbin.org/get')
        #data = r.json()
        #await message.channel.send(data)

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

#FIXME: Send time off cutoff reminder on Sundays and Mondays at a specific time each week
async def send_time_off_reminder():
    #FIXME Needs to set a flag message_sent to false until the minute for the message being sent has passed to avoid duplicate messages
    #FIXME Needs to allow for setting a specific start time/date rather than beginning timer sequence on the time/date the bot script is ran.
    message_sent = false
    
    while not message_sent:
        now = datetime.datetime.now()

        then = now + datetime.timedelta(days=7)
        then = now.replace(hour=8, minute=25)

        print((then - now).total_seconds)
        wait_time = (then - now).total_seconds()
        await asyncio.sleep(wait_time)
        
        channel = client.get_channel(channel_ids['Schedule'])

        await channel.send('Remember to put in any scheduling requests you have for the upcoming week as the cutoff is at 3pm today!')

# Run script via a discord bot, passing in the bot's token as the argument
client.run('MTIyMzM2OTIyNjUxODAwNzg2OA.Gfby-v.sKqPTJUVHc72y10ggSSbkdryiFCcucMebyF12w')