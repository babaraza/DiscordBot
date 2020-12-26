[![Python 3.8](https://img.shields.io/badge/Python-3.8-blue.svg)](https://www.python.org/downloads/release/python-38/)

# Discord Bot
Bot to get live stock updates from online stores for Nvidia RTX 3000 series graphic cards

### Information

This script works as a `Discord` bot and uses `Repl.it` for hosting and server
 - `Discord` bot to handle messages to user
 - `Repl.it` for hosting
 - `Flask` for server so `UptimeRobot` can ping to keep bot alive
 - `UptimeRobot` for pinging `Repl.it` server to keep the bot alive


### Bot Commands 

> Enter these inside the Discord chat to the Bot

| Command   | Example       | Notes                                                        |
| --------- | ------------- | ------------------------------------------------------------ |
| $run      | $run          | Will run the main loop to start scraping                     |
| $stop     | $stop         | Will stop the scraping                                       |
| $list     | $list         | Will list all the items in the array that are being checked for |
| $add      | $add 3080     | Will add 3080 to the list of items to check stock for        |
| $del      | $del 1        | Will delete item at specific index of the $list              |
| $test     | $test 3080    | Will run a test scrape for 3080 and return json in logs      |
| $timer    | $timer        | Will return the current sleep timer in seconds that determines the interval with which the bot checks for new stock |
| $settimer | $settimer 300 | Set the above timer (in seconds) to a new interval           |