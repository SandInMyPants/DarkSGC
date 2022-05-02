import time
import json
from pyfiglet import figlet_format
import pyautogui as pyg
import os

# save urls.json do a variable
f = open("urls.json")
global urls
urls = json.load(f)
f.close()

# save data.json to a variable
f = open("data.json")
global data
data = json.load(f)
f.close()

# save all data
def save():
    f = open("data.json", 'w')
    json.dump(data, f)
    f.close()
    f = open("urls.json", 'w')
    json.dump(urls, f)
    f.close()
    print("Data saved")

# wait x seconds and restart
def wait_and_reset(amount=data["waittime"]):
    time.sleep(amount)
    clear()
    start()


def params(command, *args):
    print("Invalid params for:", command)
    for value in args:
        print("[{}]".format(value))
        wait_and_reset()


def clear():
    os.system("clear")


if data["clear_on_start"] == "True":
    clear()


def error():
    print("Someting went wrong")
    wait_and_reset()

# operation select function
def operation_select():
    operation = (input("Input operation (open or run)> ")).split(" ")
    # prime opening function
    if operation[0] == "open":
        run("open", "N/A", "N/A")
    # prime spam function
    elif operation[0] == "run":
        operation = "run"
    # change loadtime
    elif operation[0] == "lt":
        try:
            data["loadtime"] = int(operation[1])
        except ValueError:
            print("Value must be an integer")
            wait_and_reset()
        except IndexError:
            params("lt(load time)", "length")
        save()
        wait_and_reset()
    # change wait time
    elif operation[0] == "wt":
        try:
            data["loadtime"] = int(operation[1])
        except ValueError:
            print("Value must be an integer")
            wait_and_reset()
        except IndexError:
            params("wt(wait time)", "length")
        save()
        wait_and_reset()
    # change 'clear on start' status
    elif operation[0] == "cos":
        try:
            if operation[1] == "t":
                data["clear_on_start"] = "True"
            if operation[1] == "f":
                data["clear_on_start"] = "False"
            else:
                params("cos(clear on start)", "t(True) or f(False")
        except IndexError:
            params("cos(clear on start)", "t(True) or f(False")
        save()
        wait_and_reset()

    # add url fucntion
    elif operation[0] == "url":
        try:
            data["loadtime"] = str(operation[1])
        except IndexError:
            params("url(add url)", "url")
        wait_and_reset()
    # save data
    elif operation[0] == "s":
        save()
        print("All data saved")
        wait_and_reset()
    # else
    else:
        print("Invalid operation")
        wait_and_reset()
    return operation

# runtime select function
def length_select():
    try:
        length = int(input("Input desired runtime (seconds)> "))
    except ValueError:
        print("Invalid length")
        time.sleep(data["waittime"])
        length_select()
    return length

# message select function
def message_select():
    message = input("Input message> ")
    return message

# countdown function
def countdown(amount):
    for i in range(0, amount):
        print(amount-i)
        time.sleep(1)

# main function (opens sites / or run spam)
def run(operation, message, runtime):
    # open urls
    if operation == 'open':
        if input("Enter 'r' when ready> ") == "r":
            print("Have browser open in:")
            countdown(data["loadtime"])
            for key, value in urls.items():
                pyg.keyDown("CTRL")
                pyg.press("E")
                pyg.keyUp("CTRL")
                pyg.typewrite(value)
                pyg.press("ENTER")
            inp = input("Would you like to run program> ")
            if inp == "yes":
                run("run", message_select(), length_select())
            elif inp == "no":
                print("Ok")
                save()
                exit()
            else:
                print("Invalid input")
                save()
                save()
                exit()
        else:
            print("Invalid input")
            time.sleep(data["waittime"])
            run(open, message, runtime)

    # start spam
    if operation == 'run':
        print("Open browser in:")
        countdown(data["loadtime"])
        t_end = time.time() + 60 * runtime
        while time.time() < t_end:
            time.sleep(1)
            pyg.typewrite(message)
            time.sleep(0.1)
            pyg.press("ENTER")
            pyg.keyDown("CTRL")
            pyg.press("TAB")
            pyg.keyUp("CTRL")
        print("Process finished")
        save()
        exit()

# define main loop
def start():
    print(figlet_format("DarkSGC", font="graffiti") + "Version 1.1\n")
    operation = operation_select()
    message = message_select()
    length = length_select()
    run(operation, message, length)

# start main loop
start()
