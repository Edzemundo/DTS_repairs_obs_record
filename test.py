import PySimpleGUI as sg
import repairsrecord as rr

layout = [[sg.Text("Enter incident number (Numbers ONLY): ")],
            [sg.Push(), sg.Input(size=(40), key="incident", justification="c"), sg.Button("OK", key="set"), sg.Push()],
            [sg.Push(), sg.Text("", key="status_text"), sg.Push()],
            [sg.Push(), sg.Button("Record", key="record", disabled=True, disabled_button_color="black"), sg.Button("Stop Recording", key="stop_recording", disabled=True, disabled_button_color="black"), sg.Push()]]


window = sg.Window("DTS Repairs Record", layout=layout, size=(325,130))


while True:
    event, values = window.read()
    
    if event == "set":
        rr.get_new_name(values["incident"])
        if record_ready is True:
            window["record"].update(disabled=False)
        
    if event == "record":
        rr.start_recording()
        window["status_text"].update("Recording...")
        window["stop_recording"].update(disabled=False)
        
    
    if event == "stop_recording":
        rr.stop_recording()
        window["stop_recording"].update(disabled=True)
        window["record"].update(disabled=True)
        window["status_text"].update("")
        window["incident"].update("")

        
    if event == sg.WIN_CLOSED:
        break