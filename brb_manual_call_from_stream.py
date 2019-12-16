#!/usr/bin/python
import praw, time

user_agent = "brb_call 1.0 by /u/BrokenRecordBot"
checktime = time.time() - 50 # Uses checktime to determine which stream items are actionable. -50 seconds to account for script reboot time
signature = "\n\n^(BOT IN TRAINING. PM WITH SUGGESTIONS AND CONTRIBUTIONS. SEE MY) [^(WIKI)](https://www.reddit.com/r/BrokenRecordBot/wiki) ^(FOR USE.)"
reddit = praw.Reddit(user_agent=user_agent)
wikipage = reddit.subreddit('BrokenRecordBot').wiki['index']
wikicontent = wikipage.content_md

headers = []
for ln in wikicontent.split('\n'): # this is probably not the best way, but this populates the commands from the wiki into an array
    if ln.startswith("### "):
        headers.append(ln[4:])

for item in reddit.inbox.stream(): # iterates through new stream items
    if item.created_utc > checktime: # checks if newer than script runtime
        item_body = reddit.comment(item).body.lower() # makes lowercase
        brbpos = item_body.find("u/brokenrecordbot") # returns position of mention in comment body
        if brbpos > -1:
            commandpos = item_body.find(" ", brbpos + 18) # finds end of mention command
            if commandpos == -1: # if there's no space after command text
            	commandpos = len(item_body) # mark end of command
            command = item_body[brbpos + 18:commandpos].lower() # extracts command text from comment body
            print("mention recognized with command")
            print(command + "<<< is command. checking for match in:") # make sure the extracted command has no spaces
            print(headers) # shows currently registered commands (rerun script to refresh with new wiki entries)
            if command in headers:
                print(command + " command matched")
                sectionstart = wikicontent.find("\n", wikicontent.find("### " + command)) # parses wiki for command. must be a subheader
                sectionend = wikicontent.find("###", sectionstart) # finds end of subheader section. requires a subheader below all commands
                section = wikicontent[sectionstart +1:sectionend -2] # accounts for spacing
                print("replying:\n" + section + signature + "\n to: ")
                print(item_body)
                item.reply(section + signature)
