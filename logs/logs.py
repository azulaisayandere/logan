import json

read_log = json.load(open("user_log.json", "r"))

masslist = read_log['guilds']
write = {"guilds": masslist}

async def log_data(message):

    g = False # guild data
    for guilds in masslist:
        if guilds['guild_name'] == message.guild.name:
            userlist = guilds['users']
            g = True
        elif (guilds['guild_name'] != message.guild.name) and (guilds['guid'] == message.guild.id):
            print("[{}] {} has changed their guild name to {}, updating entry in file.".format(message.created_at.strftime('%H:%M:%S'), guilds['guild_name'], message.guild.name))
            guilds['guild_name'] = f'{message.guild.name}'
            userlist = guilds['users']
            g = True

    if g == True:
        u = False # user data
        for users in userlist:
            if users['username'] == f'{message.author}':
                u = True
                users['cnt'] += 1
            elif (users['uid'] == message.author.id) and (users['username'] != f'{message.author}'):
                print("[{}] User {} has changed their tag to {}, updating entry in file.".format(message.created_at.strftime('%H:%M:%S'), users['username'], message.author))
                users['username'] = f'{message.author}'
                u = True
                users['cnt'] += 1

        if u == False: # log new users
            role_list = []
            for role in message.author.roles:
                if role.name != '@everyone':
                    role_list.append({"role name":role.name, "role id":role.id})
            userlist.append({
                'username': f'{message.author}',
                'uid': message.author.id,
                'cnt': 1,
                'roles':role_list})
            print(f"[{message.created_at.strftime('%H:%M:%S')}] Logged new user, {message.author}, in {message.guild}! ")

    else: # log new guilds
        masslist.append({'guild_name': f'{message.guild}', 'guid': int(f'{message.guild.id}'), 'users': [],})
        role_list = []
        for role in message.author.roles:
            if role.name != '@everyone':
                role_list.append({"role name":role.name, "role id":role.id})
        for guilds in masslist:
            if guilds['guid'] == message.guild.id:
                guilds['users'].append({
                        'username': f'{message.author}',
                        'uid': message.author.id,
                        'cnt': 1,
                        'roles':role_list})
                print(f"[{message.created_at.strftime('%H:%M:%S')}] Logged new user, {message.author}, in {message.guild}!")
            else:
                pass

    with open('user_log.json', 'w') as file: # write to files
        json.dump(write, file, indent=2)

async def role_check(message):
    for guilds in masslist:
        if message.guild.id == guilds['guid']:
            for users in guilds['users']:
                if users['username'] == str(message.author):
                    pass