from datetime import datetime
import obsws_python as obs
import PySimpleGUI as sg
import time
import sys
import os

def connect():
    """connects to obs web socket server
    """
    try:
        global obs_ws
        # create obs server object
        obs_ws = obs.ReqClient(host="localhost", port="4455", password="obsppman")
        global cl
        # event object for callback functions
        cl = obs.EventClient(host="localhost", port="4455", password="obsppman")
        
        obs_ws.set_input_mute("Desktop Audio", True) # mutes the Desktop Audio
        obs_ws.set_input_mute("Mic/Aux", True) # mutes the microphone
        
    except ConnectionRefusedError:
        # checks for connection error
        sg.popup("Connection to OBS unsuccessful - OBS may not be opened or set up correctly", no_titlebar=True)
        sys.exit()
    

def get_new_name(incident):
    """gets the incident number from user input, formats, and sets the name of the recording to the incident number as well as date and time of video creation
    
    Args:
        incident (string): incident number

    Returns:
        new path including new filename
    """
    # receive incident number as user input
    # incident = sg.popup_get_text(title="Repairs Record", message="Please enter the incident number (numbers only):")
    
    # checks to see if there is any letters in the input
    allowed_chars = ["i","n","c"]
    invalid_char = False
    for char in incident:
        if char.isalpha():
            if char.lower() not in allowed_chars:
                invalid_char = True
                
    if invalid_char is True:
        window["status_text"].update("Invalid incident number")      
        global record_ready
        record_ready = False
        # sys.exit()
        
    # checks to see if there was any input
    elif len(incident) == 0:
        window["status_text"].update("Please input an incident number")
        record_ready = False
        # sys.exit()
    

    else:
        for char in incident:
            if char.isalpha() or char == " ":
                incident = incident.replace(char,"")
        
        # formats name and path of new video file under variable "new_path"
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%m-%d-%Y_%H-%M")
        filename = f"INC{incident}" + ".mp4"
        record_directory_call = obs_ws.send("GetRecordDirectory")
        global new_path
        new_path = record_directory_call.record_directory + f"\{filename}"
        new_path = new_path.replace("\\","//")
        
        record_ready = True
    
    
    
def on_record_state_changed(data):
    """obs web socket api callback function to receive a record state change event

    Args:
        data (data object): contains the returned attributes from callback function

    Returns:
        data when record changes
    """
    # get the path of the original recording
    global old_path
    old_path = data.output_path
    # determine if obs is producing an output i.e. recording
    global state
    state = data.output_active



def rename(old, new):
    """rename a file using the rename method from the os module

    Args:
        old (string): path to the original video recording
        new (string): path to the new recording name
    """
    
    
    
    try:
        if state is False:
            time.sleep(5)
            os.rename(old, new)

        elif state is True:
            time.sleep(1)
            rename(old, new)
            
    except FileExistsError:
        # catches the error flag that appears when there is a file with the same name (incident number) in the directory
        paths = new.split("//")
        last_path = paths[-1].split(".")
        filename = last_path[0]
        
        if "_" in filename:
            filenum = filename[filename.index("_")+1:]
            new_filename = filename.replace(filenum, str(int(filenum)+1)) #adds an _'number'+1 if there is a video that has been named the same more than once
            new = new.replace(filename, new_filename)
        else:
            new_filename = filename + "_1" 
            new = new.replace(filename, new_filename)
            
        if state is False:
            #renames the file only when there is no longer a recording output from OBS
            rename(old, new)
        elif state is True:
            time.sleep(1)
            rename(old, new)
    
        
    
    
def start_recording():
    """starts recording and begins callback function
    """
    obs_ws.start_record() # start recording
    cl.callback.register(on_record_state_changed) # begin callback function
    # following 2 lines might be redundant code. Will be determined at a later time (probably)
    global status
    status = obs_ws.send("GetRecordStatus")


def stop_recording():
    """stops recording
    """
    obs_ws.stop_record() #hopefully self explanatory
    time.sleep(2)
    rename(old_path, new_path)

        
connect()
cl.callback.register(on_record_state_changed)


# ------------------------------------------------------------------------------------

tab1 = [[sg.Text("Enter incident number: ")],
            [sg.Push(), sg.Input(size=(35), key="incident", justification="c"), sg.Button("OK", key="set"), sg.Push()],
            [sg.Push(), sg.Text("Please press OK before recording", key="status_text"), sg.Push()],
            [sg.Push(), sg.Button("Start Recording", key="record", disabled=True, disabled_button_color="black"), sg.Button("Stop Recording", key="stop_recording", disabled=True, disabled_button_color="black"), sg.Push()]]

tab2 = [[sg.Text("Enter new file name:", key="rename_instr")],
                [sg.Input(key="rename_input"), sg.Button("OK", key="rename_ok")],
                [sg.Text("Enter old file name")],
                [sg.Input(key="rename_input2", disabled=True), sg.Button("OK", key="rename_ok2", disabled=True)],
                [sg.Text("Enter new file name and hit OK", key="rename_status")],
                [sg.Push(), sg.Button("Rename", disabled=True), sg.Push()]]

layout = [[sg.Titlebar("Repairs Record", background_color="black")],
          [sg.TabGroup([[sg.Tab("Record", tab1), sg.Tab("Rename", tab2)]])]]


window = sg.Window("DTS Repairs Record", layout=layout, size=(380,230), keep_on_top=True)


while True:
    event, values = window.read()
    
    if event == "set":
        get_new_name(values["incident"])
        if record_ready is True:
            window["record"].update(disabled=False)
            window["status_text"].update("Ready to record")
        
    if event == "record":
        start_recording()
        window["status_text"].update("Recording...")
        window["stop_recording"].update(disabled=False)
        
    
    if event == "stop_recording":
        window["status_text"].update("Renaming...")
        stop_recording()
        window["stop_recording"].update(disabled=True)
        window["record"].update(disabled=True)
        window["status_text"].update("Please press OK before recording")
        window["incident"].update("")
        
    if event == "rename_ok":
        record_directory_call = obs_ws.send("GetRecordDirectory")
        path_changed_to = record_directory_call.record_directory + "//" + values["rename_input"] + ".mp4"
        window["rename_input2"].update(disabled=False)
        window["rename_ok2"].update(disabled=False)
        window["rename_status"].update("Enter old file name and hit OK")

    if event == "rename_ok2":
        record_directory_call = obs_ws.send("GetRecordDirectory")
        path_to_change = record_directory_call.record_directory + "//" + values["rename_input2"] + ".mp4"
        window["Rename"].update(disabled=False)
        window["rename_status"].update("Ready to rename")
        
    if event == "Rename":
        try:
            os.rename(path_to_change, path_changed_to)
            window["rename_input"].update("")
            window["rename_input2"].update("")
            window["rename_input2"].update(disabled=True)
            window["rename_ok2"].update(disabled=True)
            window["Rename"].update(disabled=True)
            window["rename_status"].update("File renamed")
            
        except FileNotFoundError:
            window["rename_status"].update("The old file stated does not exist")
            window["rename_input"].update("")
            window["rename_input2"].update("")
            window["rename_input2"].update(disabled=True)
            window["rename_ok2"].update(disabled=True)
            window["Rename"].update(disabled=True)
            
        except FileExistsError:
            window["rename_status"].update("The new file name already exists")
            window["rename_input"].update("")
            window["rename_input2"].update("")
            window["rename_input2"].update(disabled=True)
            window["rename_ok2"].update(disabled=True)
            window["Rename"].update(disabled=True)
            

        
    if event == sg.WIN_CLOSED:
        break