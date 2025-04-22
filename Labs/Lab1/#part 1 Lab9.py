#part 1 Lab9
import logging
import logging.config
import json
import time
import threading
import os
import matplotlib.pyplot as plt
pip install matplotlib



# the log
LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

# Create logger instances for different components
loggers = {
    "sqldb": logging.getLogger("sqldb"),
    "ui": logging.getLogger("ui"),
    "frontend.js": logging.getLogger("frontend.js"), #child of frontend
    "backend.js": logging.getLogger("backend.js"), #child of backend
    "frontend.flask": logging.getLogger("frontend.flask"),#child of frontend
    "backend.flask": logging.getLogger("backend.flask"), #child of backend
}

# Function to log messages (i dont know if its supposed to be this simple or not for part 1)
def log_messages():
    loggers["sqldb"].info("sqldb info message")
    loggers["sqldb"].error("sqldb error message")
    loggers["ui"].warning("ui warning message")
    loggers["frontend.js"].critical("bruh crtitcal frontend")
    loggers["backend.flask"].error("yuh error backend")

if __name__ == "__main__":
    log_messages()

#part 2 Lab9
# lab9_part2.py
# I think this is for reading and counting logs? let's try it
import re  
import json 
import os  

# Part 2a - reading the file
def read_the_log_file(filename):
    # this function is supposed to read the log file
    # i hope this works for opening files
    log_lines = []
    try:
        file = open(filename, 'r')  # open file to read
        for line in file:
            log_lines.append(line)  # add each line to list
        file.close()  # gotta close the file right?
        print("Yay, read the file!")
        return log_lines
    except:
        print("Uh oh, something went wrong with the file! Maybe it’s not there?")
        return []  # return empty if it fails

# Part 2b 
def parse_the_log_lines(lines_of_log):
    # this is where we break down the log lines
    #formated the log the same as part 1
    # i think regex is needed? i copied this from copilot autofill
    regex_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \| ([\w\.]+) \| (INFO|WARNING|ERROR|CRITICAL) \| (.+)'
    
    parsed_stuff = []  # store all the parsed lines here
    for line in lines_of_log:
        line = line.strip()  # remove extra spaces or newlines
        match = re.match(regex_pattern, line)
        if match:
            # i think these are the parts we need
            timestamp = match.group(1)
            logger = match.group(2)
            level = match.group(3)
            message = match.group(4)
            # put it in a dictionary
            log_entry = {
                "time": timestamp,  # i called it time cause timestamp is long
                "logger": logger,
                "level": level,
                "message": message
            }
            parsed_stuff.append(log_entry)
        else:
            print("This line is weird, skipping it: " + line)
    
    return parsed_stuff

# Part 2c 
def count_all_levels(logs_that_were_parsed):
    # we need to count how many INFO, WARNING, etc and the messages
    # i’m gonna use a dictionary from the example
    counts = {
        "INFO": {},
        "WARNING": {},
        "ERROR": {},
        "CRITICAL": {}
    }
    
    # go through each log
    for log in logs_that_were_parsed:
        level = log["level"]
        message = log["message"]
        # if message isn’t in the dictionary yet, add it with 0
        if message not in counts[level]:
            counts[level][message] = 0
        # add 1 to the count
        counts[level][message] = counts[level][message] + 1
    
    # remove levels with no messages to make it look cleaner
    final_counts = {}
    for level in counts:
        if counts[level]:  # only add if it has something
            final_counts[level] = counts[level]
    
    return final_counts

# save to json file
def save_to_json_file(data_to_save, json_filename):
    # this saves the counts to a json file
    try:
        file = open(json_filename, 'w')
        json.dump(data_to_save, file, indent=4)  # indent to make it pretty
        file.close()
        print("Saved the json file, I think!")
    except:
        print("Something broke when saving the json file :(")

#main function
if __name__ == "__main__":
    # i guess we start here
    log_file_name = "app.log"  # hope this is the right file
    json_file_name = "log_summary.json"  # where to save the counts
    
    # read the file first
    lines = read_the_log_file(log_file_name)
    
    # check if we got anything
    if len(lines) == 0:
        print("No lines to read, stopping.")
    else:
        # parse the lines
        parsed_logs = parse_the_log_lines(lines)
        
        # check if we parsed anything
        if len(parsed_logs) == 0:
            print("somethings wrong.")
        else:
            # count the levels
            counted_logs = count_all_levels(parsed_logs)
            
            # save to json
            save_to_json_file(counted_logs, json_file_name)
            print("done")


#Part 3a - the log summary
# Checking the json
LOG_FILE = "log_summary.json"
# Function to load the JSON log summary (function was autofilled by copilot)
def load_logs(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        print("Problem reading the log summary:", e)
        return {}

# This will keep track of new critical messages
previous_criticals = {}

# Main monitoring function (I wasnt sure about the path so i had to use copilot to fill it in)
def watch_logs():
    last_updated = 0

    while True:
        if os.path.exists(LOG_FILE):
            current_time = os.path.getmtime(LOG_FILE)
            if current_time != last_updated:
                last_updated = current_time
                logs = load_logs(LOG_FILE)

                print("\nLog Summary")
                for level, msgs in logs.items():
                    total = sum(msgs.values())
                    print(f"{level}: {total} entries")

                    if level == "CRITICAL":
                        for msg, count in msgs.items():
                            # Only show if it's new
                            old_count = previous_criticals.get(msg, 0)
                            if count > old_count:
                                print(f"!!! NEW CRITICAL: {msg} ({count})")
                                previous_criticals[msg] = count

        time.sleep(WAIT_TIME)

# Start the thread for monitoring (i dont know if were allowed to use daemons for this part)
if __name__ == "__main__":
    t = threading.Thread(target=watch_logs)
    t.daemon = True
    t.start()

    print("Monitoring logs... Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped monitoring.")

#part 3b - graphing the log summary
LOG_FILE = "log_summary.json"
WAIT_TIME = 2

# Read the JSON file (reused )
def load_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print("Couldn't read log file:", e)
        return {}

# Main function for plotting (had to look this up how to do this)
def plot_logs():
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    last_updated = 0

    while True:
        if os.path.exists(LOG_FILE):
            current_time = os.path.getmtime(LOG_FILE)
            if current_time != last_updated:
                last_updated = current_time
                logs = load_logs()

                # Reset the chart
                ax.clear()

                levels = []
                totals = []

                for level, msgs in logs.items():
                    levels.append(level)
                    totals.append(sum(msgs.values()))

                ax.bar(levels, totals, color=['blue', 'orange', 'yellow', 'red'])
                ax.set_title("Log Level Distribution")
                ax.set_ylabel("Count")
                ax.set_xlabel("Log Level")

                plt.draw()
                plt.pause(0.1)

        time.sleep(WAIT_TIME)

# Start graphing in a daemon thread
if __name__ == "__main__":
    t = threading.Thread(target=plot_logs)
    t.daemon = True
    t.start()

    print("Graphing logs... Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped graphing.")
