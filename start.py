import sys
import subprocess
import threading


start_files = ["./GuildOfGuilds/main.py"]


def runfile(name):
    working_dir = "/".join(name.split("/")[:-1])
    subprocess.call([sys.executable, '-u', name])


threads = []
for f in start_files:
    thread = threading.Thread(target=runfile, args=(f,))
    thread.start()
    threads += [thread]

for thread in threads:
    thread.join()
