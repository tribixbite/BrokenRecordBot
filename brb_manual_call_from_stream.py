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

def inboxstream():
    keep_going = True
    wait_time = 90
    try:
        for item in reddit.inbox.stream(skip_existing=True): # iterates through new stream items
            # for item in praw.models.util.stream_generator(reddit.inbox.mentions, skip_existing=True):
            print("checktime:")
            print(checktime)
            print("created:")
            print(item.created_utc)
            if reddit.comment(item).body: #just added this
                print("commment discovered")
                if item.created_utc > checktime:
                    print(item.body)
                    item_body = reddit.comment(item).body.lower() # this breaks if no comment
                    brbpos = item_body.find("u/brokenrecordbot")
                    print(brbpos)
                    if brbpos > -1:
                        item.mark_read()
                        print(item_body)
                        print("user:")
                        print(reddit.comment(item).author)
                        commandpos = item_body.find(" ", brbpos + 18)
                        if commandpos == -1:
                        	commandpos = item_body.find("\n", brbpos + 18)
                        	if commandpos == -1:
                        	    commandpos = len(item_body)
                        altcommandpos = item_body.find("\n", brbpos + 18)
                        if altcommandpos > 0:
                            if altcommandpos < commandpos:
                                commandpos = altcommandpos
                        print(commandpos)
                        command = item_body[brbpos + 18:commandpos].lower()
                        print("mention recognized with command ")
                        print(command + "<<< is command")
                        print("checking commands list: ")
                        wikipage = reddit.subreddit('BrokenRecordBot').wiki['index']
                        wikicontent = wikipage.content_md

                        headers = []
                        for ln in wikicontent.split('\n'):
                            if ln.startswith("### "):
                                headers.append(ln[4:])
                        print(headers)
                        if command in headers:
                            print(command + " command matched")
                            sectionstart = wikicontent.find("\n", wikicontent.find("### " + command))
                            sectionend = wikicontent.find("###", sectionstart)
                            section = wikicontent[sectionstart +1:sectionend -2]
                            print("replying " + section + signature + "\n to: ")
                            print(item_body)
                            item.reply(section + signature)
                            print(command[0:2])
                            print(len(command))
                            print(command[2:len(command)])
                        elif command == "nimhpreach":
                            nimhpreach = reddit.subreddit('flashlight').wiki['preach-nimh'].content_md
                            item.reply(nimhpreach + signature)
    except Exception as e:
        print("got to exception")
        print(str(e))
        if '503' in str(e):
            time.sleep(wait_time)
            inboxstream()
        elif 'comment' in str(e):
            print("congrats, you got a comment that broke the script")
            #time.sleep(wait_time)
            inboxstream()
        else:
            print(str(e))
            print("else exception")
            inboxstream()
        return False
    return True

keep_going = True
while keep_going:
    keep_going = inboxstream()
