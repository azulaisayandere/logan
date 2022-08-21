import json

read_log = json.load(open("user_log.json", "r"))

masslist = read_log['guilds']
write = {"guilds": masslist}

async def log_data(message):

    g = False # guild data
    for guilds in masslist:
        if guilds['name'] == message.guild.name:
            userlist = guilds['users']
            g = True
        elif (guilds['name'] != message.guild.name) and (guilds['guid'] == message.guild.id):
            print("[{}] {} has changed their guild name to {}, updating entry in file.".format(message.created_at.strftime('%H:%M:%S'), guilds['name'], message.guild.name))
            guilds['name'] = f'{message.guild.name}'
            userlist = guilds['users']
            g = True

    if g == True:
        u = False # user data
        for users in userlist:
            if users['name'] == f'{message.author}':
                u = True
                users['cnt'] += 1
            elif (users['uid'] == message.author.id) and (users['name'] != f'{message.author}'):
                print("[{}] User {} has changed their tag to {}, updating entry in file.".format(message.created_at.strftime('%H:%M:%S'), users['name'], message.author))
                users['name'] = f'{message.author}'
                u = True
                users['cnt'] += 1

        if u == False: # log new users
            userlist.append({
                'name': f'{message.author}',
                'uid': message.author.id,
                'dnm': 40,
                'cnt': 1})
            print(f"[{message.created_at.strftime('%H:%M:%S')}] Logged new user, {message.author}, in {message.guild}! ")

    else: # log new guilds
        masslist.append({'name': f'{message.guild}', 'guid': int(f'{message.guild.id}'), 'users': [],})
        for guilds in masslist:
            if guilds['guid'] == message.guild.id:
                guilds['users'].append({
                        'name': f'{message.author}',
                        'uid': message.author.id,
                        'dnm': 40,
                        'cnt': 1})
                print(f"[{message.created_at.strftime('%H:%M:%S')}] Logged new user, {message.author}, in {message.guild}!")
            else:
                pass
    with open('user_log.json', 'w') as file: # write to files
        json.dump(write, file, indent=2)