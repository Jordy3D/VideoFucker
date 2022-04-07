#  ▄   ▄
# ▄██▄▄██▄          ╔╗ ┌─┐┌┐┌┌─┐█
# ███▀██▀██         ╠╩╗├─┤│││├┤ █
# ▀███████▀         ╚═╝┴ ┴┘└┘└─┘█
#   ▀███████▄▄      ▀▀▀▀▀▀▀▀▀▀▀▀█▀
#    ██████████▄
#  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█▀

import os.path
from os.path import exists
import subprocess
import sys
from signal import signal, SIGTERM
import shlex


# Thank you, https://stackoverflow.com/a/57081121
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def run_ffmpeg(command):
    # Prepare Path to FFMPEG
    ffmpeg_path = "ffmpeg//ffmpeg.exe"

    new_command = shlex.split(command)
    new_command[0] = resource_path(ffmpeg_path)

    subprocess.call(new_command)


def cleanup_temp():
    if exists("TEMP_FILE.mp4"):
        os.remove("TEMP_FILE.mp4")


def quit_handler():
    signal(SIGTERM, cleanup_temp)
    signal(SIGTERM, fuck_file)


def fuck_video(file_to_fuck):
    command_1 = f"ffmpeg -y -v quiet -stats -i \"{file_to_fuck}\" -c:v libvpx-vp9 -strict -2 -c:a libopus TEMP_FILE.mp4"
    if override:
        command_2 = f"ffmpeg -y -v quiet -stats -stream_loop {loop_count} -i TEMP_FILE.mp4 -c copy {file_name}.webm"
    else:
        command_2 = f"ffmpeg -y -v quiet -stats -stream_loop {loop_count} -i TEMP_FILE.mp4 -fs 100M -c copy {file_name}.webm"

    print("\nPreparing video file...")
    run_ffmpeg(command_1)
    if exists("TEMP_FILE.mp4"):
        print("Video file prepared.")
    else:
        print("Something went wrong and TEMP_FILE could not be made Please report this on the GitHub.")
        sys.exit(1)

    print("\nLooping video file...")
    run_ffmpeg(command_2)
    print("Video file looped.")

    print("\nRemoving temp file...")
    os.remove("TEMP_FILE.mp4")
    print("Temp file removed.")

    print("\nFucking the file...")
    fuck_file(f"{file_name}.webm")
    print("File fucked.\n")


def fuck_file(file_to_fuck):
    # Open file for reading
    with open(f'{file_to_fuck}', 'rb') as f:
        content = f.read().hex()

    # Find a key feature to start with then find the start of the part we need to edit
    find = content.index("2ad7b1")
    found = content.index("4489", find)

    # Replace the existing time data with this modified data
    infinite = "4489884000"
    content = content[:found] + infinite + content[found + 4:]

    f.close()

    # Open file for writing
    with open(f'{file_to_fuck}', 'wb') as f:
        f.write(bytearray.fromhex(content))
    f.close()


if len(sys.argv) <= 1:
    print("Please drag a file onto me.")
    input("Press Enter to exit.")
    sys.exit(0)
else:
    in_file = sys.argv[1]
    file_name = os.path.basename(in_file).rsplit('.', 1)[0]
    file_type = os.path.basename(in_file).rsplit('.', 1)[1].lower()

mode = 0

override = False

if file_type == "webm":
    print("I see you have entered a WEBM. Would you like to LOOP this video or FUCK it?")
    mode = int(input("Enter 0 for LOOP and 1 for FUCK: "))

if mode == 1:
    print("\nFucking the file...")
    fuck_file(f"{file_name}.{file_type}")
    print("File fucked.\n")
    sys.exit(0)

print("Enter a number of times to loop the input video. -1 will loop the file until you kill the process.")
loop_count = int(input("Please enter a value: "))

if loop_count == -1:
    print("\nYou've selected to loop infinitely. This will fill your hard drive quickly.")
    print("There is a hardcoded limit of 100MB on the infinite loop function. To override this, type override below.")
    print("or just press Enter to continue. You have been warned.")
    override = True if input() == "override" else False

fuck_video(f"{in_file}")
