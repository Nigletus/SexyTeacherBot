import json
import random
import threading
import time

from Bot import Bot

art = """
   _____              _______              _               ____        _
  / ____|            |__   __|            | |             |  _ \      | |
 | (___   _____  ___   _| | ___  __ _  ___| |__   ___ _ __| |_) | ___ | |_
  \___ \ / _ \ \/ / | | | |/ _ \/ _` |/ __| '_ \ / _ \ '__|  _ < / _ \| __|
  ____) |  __/>  <| |_| | |  __/ (_| | (__| | | |  __/ |  | |_) | (_) | |_
 |_____/ \___/_/\_\\__, |_|\___|\__,_|\___|_| |_|\___|_|  |____/ \___/ \__|
                    __/ |
                   |___/
                                  Special thanks to ClaudiaD & l33t
"""

CONF_FILENAME = "conf.json"

with open(CONF_FILENAME, "r") as _data:
    data = json.load(_data)

conf = data["conf"]
bot = Bot(data)


def chat():
    while True:
        msg = input()
        bot.message(msg, conf["chans"][0])


def jew():
    while True:
        s = random.randint(3600 * 24, 3600 * 36)
        time.sleep(s)
        bot.message(data["commands"]["donate"], conf["chans"][0])


def welcome(nick):
    greet = ("Welcome to #learninghub %s ! Here you'll find lots of resources and people to learn hacking/pentesting "
             "as well as other IT subjects. Type ?goldmine to get started and get rid of the welcome message. Type "
             "?desc <course_number> to know the description of a course. You have to use the course number in the "
             "ghostbin. Type ?help for more." % nick)
    bot.notice(nick, greet)


def check_nick(msg, nick=None):
    return "%s: %s" % (nick, msg) if nick else msg


def halp(nick=None):
    if nick in data["helps"]:
        return data["helps"][nick]

    commands = [x for x in data["commands"]]
    commands += [x for x in data["defs"] if len(x) > 3]
    commands.sort()

    cmds = ", ".join("?%s" % x for x in commands)
    msg = "Available commands: \u0002%s\u000F." % cmds
    return check_nick(msg, nick)


def random_course(nick=None):
    i = random.choice(data["courses"])
    msg = "%s. %s." % (i["id"], i["title"])
    return check_nick(msg, nick)


def desc(course):
    try:
        info = data["courses"][int(course)]
        d = info["desc"]
        return d
    except:
        return "?desc <0-108>"


def link(course):
    try:
        info = data["courses"][int(course)]
        url = info["link"]
        return url
    except:
        return "?link <0-108>"


def whatof(arg=None):
    if arg in data["whatof"]:
        return data["whatof"][arg]
    else:
        return "There is no data for this user."


def write_data(data, filename):
    w = open(filename, "w")
    json.dump(data, w)


def get_argument(msg):
    m = msg.split()
    a = m[1] if len(m) > 1 else None
    return a


def exec_command(cmd, arg):
    try:
        c = str(data["defs"][cmd])
        response = globals()[c](arg) if arg else globals()[c]()
    except:
        response = "That is not a valid command format."

    return response


def listen_irc():
    while True:
        found = re.match(r'^:([^!\s]+)!([^@\s]+@[^\s]+)\s(PRIVMSG|JOIN)\s:?(#[^:\s]+)(?:\s:(.+))?', bot.listen())
        '''
        re groups:
        if JOIN:    0 all, 1 nick, 2 host, 3 JOIN, 4 channel, 5 none
        if PRIVMSG: 0 all, 1 nick, 2 host, 3 PIVMSG, 4 channel, 5 msg
        
        '''
        # Finds JOIN and send msg/add user to list if not already in list.
        if found and found.group(3) in 'JOIN':
            if not bot.sha2(found.group(1)) in data['users'] and found.group(4) in '#learninghub':
                welcome(found.group(1))
                data['users'].append(bot.sha2(found.group(1)))

        elif found:
            cmd = re.match(r'^\?(\w+)(?:\s)(.+)?', found.group(5))
            '''
            re groups:
            0 all, 1 cmd, 2 arg
            
            '''
            arg = cmd.group(2)
            if cmd.group(1) in data["commands"]:
                response = data["commands"][cmd]
                if arg:
                    response = "%s: %s" % (arg, response)

            elif cmd.group(1) in data["defs"]:
                response = exec_command(cmd, arg)
            else:
                response = "The command you are trying to execute does not exist."
            bot.message(response, chan) if response else None


def main():
    print(art)
    bot.auth()
    bot.ping()
    bot.join()
    threading.Thread(target=chat).start()
    threading.Thread(target=jew).start()
    print("[+] Bot is up and working.\n")
    print(conf["chans"][0])
    print()
    listen_irc()


if __name__ == "__main__":
    main()
