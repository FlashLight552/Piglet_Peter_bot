from datetime import datetime


def message_log(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print (datetime.now(), func.__name__)   
        return result
    return wrapper


def print_log(id, name, command ):
    print ('date:' + str(datetime.now()), 'userid:' + str(id), 'username:' + str(name), 'command:' + str(command))    