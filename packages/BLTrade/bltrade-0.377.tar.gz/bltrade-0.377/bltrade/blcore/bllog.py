from datetime import datetime

# log
class bllog:
    # default name
    logfile="bllog.txt"

    def __init__(self,file) -> None:
        self.logfile=file


    def p(self,msg):
        current_dateTime = datetime.now()
        dt = current_dateTime.strftime('%Y-%m-%d %H:%M:%S%z')
        msg=(f'[{dt}] {msg}')  # Print date and close
        with open(self.logfile, 'a') as f:
            f.write(msg+"\n")
            print(msg)
        f.close()


"""
log=bllog("bllog123.txt")
log.p("aaaaaaa")
log.p("bbbbbbb")
"""