'''
This is a prototype script I wrote, which I would like to use as a jot-it-down notekeeper. The idea for it is to use hotkeys to either write in a new note, or view previous things.

To run this, you may have to install pynput --> (pip install pynput), and the text file I am using to keep notes for this script is local to my computer.
'''

# Keeping track of all things inside of a class.
class daytracker(object):

    # For reading previous items.
    def on_activate_r(self):
        print('READING')
        self.journalRead()

    # To add a new item.
    def on_activate_w(self):
        print('WRITING')
        self.journalWrite()

    # To quit the script.
    def on_activate_p(self):
        exit()

    def journalCheck(self):

        # Initial checks.
        import os
        os.chdir(r"C:\Users\czhu0\OneDrive\Documents\pythonstuff")
        myFile = open('journal.txt','r')
        if myFile.closed == 0:
            print("File exists and can be opened.")
            myFile.close()
            return True
        else:
            return False

    def journalWrite(self):

        if self.journalCheck() == True:
            # Getting the new data.
            from datetime import datetime
            currently = str(datetime.now())
            todaysFeelings = str(input("How are you feeling today: "))
            fullString = 'At ' + currently + ', you noted that: ' + todaysFeelings + '.' + '\n\n'

            # Inputting all the data.
            import os
            os.chdir(r"C:\Users\czhu0\OneDrive\Documents\pythonstuff")
            myFile = open('journal.txt','a')
            myFile.write(fullString)
            myFile.close()
        else:
            print("cannot open the file")

    def journalRead(self):
        if self.journalCheck() == True:
            # Open a file
            import os
            os.chdir(r"C:\Users\czhu0\OneDrive\Documents\pythonstuff")
            myFile = open('journal.txt','r')
            theStr = myFile.read()
            print(theStr)
            # Close opened file
            myFile.close()
        else:
            print("cannot open the file")

if __name__ == "__main__":

    # Start an instance.
    recording = daytracker()

    # Check if pynput was installed.
    try:
        from pynput import keyboard
    except:
        print(" 'Pynput' was not installed. Ending program now.")
        exit()

    # Getting the hotkeys to act.
    with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+r': recording.on_activate_r,
        '<ctrl>+<alt>+w': recording.on_activate_w,
        '<ctrl>+<alt>+p': recording.on_activate_p}) as h:
        h.join()
