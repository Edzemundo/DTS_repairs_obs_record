# OBS Recording

### Made specifically for Department of Technology Services (DTS) for laptop repair recording.

>Application is used to record a scene and rename the recorded file as the incident number provided before the recording begins.

Instructions

- Install OBS Studio - this was not designed for any other streaming/recording client such as Streamlabs OBS.

- Set up OBS websocket:

  1. Enable OBS websocket in settings (Google if unsure)
  2. Set the Port as 4455 (should be the default port)
  3. Set the password as "obsppman" (password was made on short notice - not my fault), do not add quotation marks. Let me know if it REALLY needs to be changed.
  4.  Set the camera source as the name "Camera" - case specific.
  5.  Set the active sign as the name "Recording Active" - case and space specific. This can be text or an image to show that recording is active. It is turned on whenever the record button is selected.

- Enter the incident number with or without "INC" - not case specific.

- Start recording to start

- Stop Recording to stop. It then takes a second to rename the file as the incident number. 

- Rename tab can be used to rename a video file.

- Cut tab is currently not functional but meant to be able to cut a video between specified timestamps and return the cut file.  

