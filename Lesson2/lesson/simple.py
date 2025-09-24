# import logging


# log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"

# #creating a formatter using our string above
# formatter = logging.Formatter(log_format)

# #create log message handler that sends outputs to a specified file
# file_handler = logging.FileHandler('my_log.log')

# #set the formattter for the messages to the formatter created
# file_handler.setFormatter(formatter)

# #get the 'root' logger
# logger = logging.getLogger()

# #add file_handler to the root loggers handlers
# logger.addHandler(file_handler)

# # logging.basicConfig(level=logging.DEBUG)
# # logging.basicConfig(level=logging.WARNING, format=log_format, filename='mylog.log')
# def my_fun(n):
#     for i in range(0, n):
#         logging.debug(i)
#         if i == 50:
#             logging.warning("Value of i is 50")
#         try:
#             100 / (50-i)
#         except ZeroDivisionError:
#             logging.error(f"Tried to divide by zero. Var was {i}")

# if __name__ == '__main__':
#     my_fun(100)

import logging


log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"

#creating a formatter using our string above
formatter = logging.Formatter(log_format)

#create log message handler that sends outputs to a specified file
file_handler = logging.FileHandler('my_log.log')
file_handler.setLevel(logging.WARNING) #allows you to set the level of the debug messages you want w/ your file handler - we should get all warning
                                        # messages here

#set the formattter for the messages to the formatter created
file_handler.setFormatter(formatter)

#these are streams to the console, allowing
# you to see all error messages as needed
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

#get the 'root' logger
logger = logging.getLogger()

#we have to set the lowest level of messages that we want to track
logger.setLevel(logging.DEBUG)

#add file_handler to the root loggers handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("Value of i is 50")
        try:
            100 / (50-i)
        except ZeroDivisionError:
            logging.error(f"Tried to divide by zero. Var was {i}")

if __name__ == '__main__':
    my_fun(100)