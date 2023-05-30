from datetime import datetime
import obsws_python as obs
import PySimpleGUI as sg
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
        
        obs_ws.set_input_mute("Mic/Aux", True) # mutes the microphone
        
    except ConnectionRefusedError:
        # checks for connection error
        sg.popup("Connection to OBS unsuccessful - OBS may not be opened or set up correctly", no_titlebar=True)
        sys.exit()
    

def get_new_name(incident):
    """gets the incident number from user input, formats, and sets the name of the recording to the incident number as well as date and time of video creation
    """
    # receive incident number as user input
    # incident = sg.popup_get_text(title="Repairs Record", message="Please enter the incident number (numbers only):")
    
    # checks to see if there is any letters in the input
    if any(char.isalpha() for char in incident):
        sg.popup("Only numbers please")
        global record_ready
        record_ready = False
        # sys.exit()
        
    # checks to see if there was any input
    elif len(incident) == 0:
        sg.popup("Please input an incident number")
        record_ready = False
        # sys.exit()
    
    else:
        # check current date and time and formats name and path of new video file under variable "new_path"
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%m-%d-%Y_%H-%M")
        filename = f"INC{incident}_{formatted_datetime}" + ".mkv"
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
    os.rename(old, new)
    
    
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
    rename(old_path, new_path)

        
connect()
cl.callback.register(on_record_state_changed)


# ------------------------------------------------------------------------------------

layout = [[sg.Text("Enter incident number (Numbers ONLY): ")],
            [sg.Push(), sg.Input(size=(40), key="incident", justification="c"), sg.Button("OK", key="set"), sg.Push()],
            [sg.Push(), sg.Text("", key="status_text"), sg.Push()],
            [sg.Push(), sg.Button("Record", key="record", disabled=True, disabled_button_color="black"), sg.Button("Stop Recording", key="stop_recording", disabled=True, disabled_button_color="black"), sg.Push()]]


window = sg.Window("DTS Repairs Record", layout=layout, size=(325,130))


while True:
    event, values = window.read()
    
    if event == "set":
        get_new_name(values["incident"])
        if record_ready is True:
            window["record"].update(disabled=False)
        
    if event == "record":
        start_recording()
        window["status_text"].update("Recording...")
        window["stop_recording"].update(disabled=False)
        
    
    if event == "stop_recording":
        stop_recording()
        window["stop_recording"].update(disabled=True)
        window["record"].update(disabled=True)
        window["status_text"].update("")
        window["incident"].update("")

        
    if event == sg.WIN_CLOSED:
        break