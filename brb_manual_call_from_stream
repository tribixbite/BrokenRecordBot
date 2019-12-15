#!/usr/bin/python
import praw, time

user_agent = "brb_call 1.0 by /u/BrokenRecordBot"
checktime = time.time() - 50
signature = "\n\n^(BOT IN TRAINING. PM WITH SUGGESTIONS.)"
reddit = praw.Reddit(user_agent=user_agent)
wikipage = reddit.subreddit('BrokenRecordBot').wiki['index']
wikicontent = wikipage.content_md

headers = []
for ln in wikicontent.split('\n'):
    if ln.startswith("### "):
        headers.append(ln[4:])

for item in reddit.inbox.stream():
    if item.created_utc > checktime:
        item_body = reddit.comment(item).body.lower()
        brbpos = item_body.find("u/brokenrecordbot")
        if brbpos > -1:
            commandpos = item_body.find(" ", brbpos + 18)
            if commandpos == -1:
            	commandpos = len(item_body)
            command = item_body[brbpos + 18:commandpos].lower()
            print("mention recognized with command")
            print(command + "<<< is command. checking for match in:")
            print(headers)
            if command in headers:
                print(command + " command matched")
                sectionstart = wikicontent.find("\n", wikicontent.find("### " + command))
                sectionend = wikicontent.find("###", sectionstart)
                section = wikicontent[sectionstart +1:sectionend -2]
                print("replying " + section + signature + "\n to: ")
                print(item_body)
                item.reply(section + signature)
