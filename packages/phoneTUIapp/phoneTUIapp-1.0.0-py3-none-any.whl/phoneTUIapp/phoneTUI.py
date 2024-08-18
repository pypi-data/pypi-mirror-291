import subprocess
import re
import npyscreen

# Your existing functions for parsing call and SMS data (parse_call_data and parse_sms_data) remain unchanged.

def parse_call_data(output_string):
    """Parses call data from the output string.

    Args:
        output_string: The output string containing call data.

    Returns:
        A tuple containing the number and direction if found, otherwise None.
    """

    # Regular expressions to match "number" and "direction"
    number_match = re.search(r'number:\s+(.+)', output_string)
    direction_match = re.search(r'direction:\s+(.+)', output_string)

    if number_match and direction_match:
        number = number_match.group(1).strip()
        direction = direction_match.group(1).strip()
        return number, direction
    else:
        return None
def parse_sms_data(data):
    """
    Parses SMS data from the given string using line-by-line parsing.
    """

    result = {}
    lines = data.splitlines()  # Split data into lines

    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        #print(f"Processing line: {repr(line)}")  # Print the line being processed

        if ":" in line:
            major = line.split("|")
            parts = major[1].split(":")  # Split at the first colon
            
            key = parts[0].strip()
            value = ":".join(parts[1:]).strip()  # Join the rest in case there were multiple colons

            # Check if the key is one we're interested in
            if key in ['number', 'text', 'state', 'timestamp']:
                result[key] = value  # Store directly using key

    if all(key in result for key in ['number', 'text', 'state', 'timestamp']):
        return result
    else:
        return None

class MyTUI(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="My TUI")

class MainForm(npyscreen.Form):
    def create(self):
        self.menu = self.add(npyscreen.SelectOne, 
                             values = ["Phone Calls", "SMS", "Exit"], 
                             max_height=4, 
                             scroll_exit=True)

        self.display_box = self.add(npyscreen.MultiLineAction, 
                                    max_height=-3,  # Fill remaining space
                                    editable=False,
                                    scroll_exit=True)

    def afterEditing(self):
        choice = self.menu.values[self.menu.value[0]]
        
        if choice == "Phone Calls":
            self.display_calls()
        elif choice == "SMS":
            self.display_sms()
        elif choice == "Exit":
            self.parentApp.setNextForm(None)  # Exit the TUI

    def display_calls(self):
        call_result = subprocess.run(["timeout", "5", "mmcli", "-m", "0", "--voice-list-calls"], capture_output=True, text=True, timeout=6)
        calls = [line.split("/")[5][0] for line in call_result.stdout.splitlines()]
        call_data = []
        for id in calls:
            call_data.append(parse_call_data(subprocess.run(["timeout", "5", "mmcli", "-m", "0", "-o", id], capture_output=True, text=True, timeout=6).stdout))

        # Format and display call data in the display_box
        formatted_calls = "\n".join([f"Number: {call[0]}, Direction: {call[1]}" for call in call_data if call])
        self.display_box.values = formatted_calls.splitlines() 
        self.display_box.display()

    def display_sms(self):
        sms_result = subprocess.run(["timeout", "5", "mmcli", "-m", "0", "--messaging-list-sms"], capture_output=True, text=True, timeout=6)
        sms = [line.split("/")[5][0] for line in sms_result.stdout.splitlines()]
        sms_data = []
        for id in sms:
            sms_data.append(parse_sms_data(subprocess.run(["timeout", "5", "mmcli", "-m", "0", "--sms", id], capture_output=True, text=True, timeout=6).stdout))
        
        # Format and display SMS data in the display_box
        formatted_sms = "\n".join([f"Number: {sms['number']}, Text: {sms['text']}" for sms in sms_data if sms])
        self.display_box.values = formatted_sms.splitlines() 
        self.display_box.display()

if __name__ == "__main__":
    myTUI = MyTUI()
    myTUI.run()
