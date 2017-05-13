import json

import datetime

import bot_logger
from config import bot_config, DATA_PATH


# read file
def get_users():
    with open(DATA_PATH+bot_config['user_file'], 'r') as f:
        try:
            data = json.load(f)
        except ValueError:
            bot_logger.logger.warning("Error on read user file")
            data = {}
        return data


# save to file:
def add_user(user, address):
    bot_logger.logger.info("Add user " + user + ' ' + address)
    data = get_users()
    with open(DATA_PATH+bot_config['user_file'], 'w') as f:
        data[user] = address
        json.dump(data, f)


def get_user_info(msg):
    dict = get_users()
    address = dict[msg.author.name]
    msg.reply(msg.author.name + ' your address is ' + address)


def get_user_address(user):
    dict = get_users()
    return dict[user]


def user_exist(user):
    dict = get_users()
    if user in dict.keys():
        return True
    else:
        return False


def get_unregistered_tip():
    with open(DATA_PATH+bot_config['unregistered_tip_user'], 'r') as f:
        try:
            data = json.load(f)
        except ValueError:
            bot_logger.logger.warning("Error on read unregistered tip user file")
            data = {}
        return data


def save_unregistered_tip(sender, receiver, amount):
    bot_logger.logger.info("Save tip form %s to %s " % (sender, receiver))
    data = get_unregistered_tip()
    with open(DATA_PATH+bot_config['unregistered_tip_user'], 'w') as f:
        data[receiver] = []
        data[receiver].append({
            'amount': amount,
            'sender': sender,
            'time': datetime.datetime.now().isoformat(),
        })
        json.dump(data, f)


def get_user_pending_tip(username):
    unregistered_tip = get_unregistered_tip()
    if username in unregistered_tip.keys():
        return unregistered_tip[username]
    else:
        return False


def remove_pending_tip(username):
    unregistered_tip = get_unregistered_tip()
    del unregistered_tip[username]
    with open(DATA_PATH+bot_config['unregistered_tip_user'], 'w+') as f:
        json.dump(unregistered_tip, f)


def get_user_history(user):
    try:
        with open(DATA_PATH+bot_config['user_history_path'] + user + '.json', 'r') as f:
            try:
                data = json.load(f)
            except ValueError:
                bot_logger.logger.warning("Error on read user file history")
                data = []
    except IOError:
        bot_logger.logger.warning("Error on read user file history")
        data = []
    return data


def add_to_history(user_history, sender, receiver, amount, action, finish=True):
    bot_logger.logger.info("Save for history user=%s, sender=%s, receiver=%s, amount=%s, action=%s, finish=%s" % (
        user_history, sender, receiver, amount, action, finish))
    data = get_user_history(user_history)
    with open(DATA_PATH+bot_config['user_history_path'] + user_history + '.json', 'w+') as f:
        data.append({
            "user": user_history, "sender": sender, "receiver": receiver, "amount": amount, "action": action,
            "finish": finish,
            'time': datetime.datetime.now().isoformat(),
        })
        json.dump(data, f)
