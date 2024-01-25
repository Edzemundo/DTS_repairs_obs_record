# OBS Recording

## by Edzemundo (edmundsagyekum@gmail.com)

### Made specifically for Department of Technology Services (DTS), Wentworth Institute of Technology for laptop repair recording.

>Application is used to record a scene and rename the recorded file as the incident number provided before the recording begins.

Instructions

- Install OBS Studio - this was not designed for any other streaming/recording client such as Streamlabs OBS.

- Set up OBS websocket:

  1. Enable OBS websocket in settings (Google if unsure)
  2. Set the Port as 4455 (should be the default port)
  3. Set the password as "obsppman" (password was made on short notice - not my fault), do not add quotation marks. Let me know if it REALLY needs to be changed.
  4.  Set the video input source being used for recording as the name "Camera" - case specific.
  5.  Set the active sign as the name "Recording Active" - case and space specific. This can be text or an image to show that recording is active. It is turned on whenever the record button is selected.

- Enter the incident number with or without "INC" - not case specific.

- Start recording to start

- Stop Recording to stop. It then takes a second to rename the file as the incident number. 

- Rename tab can be used to rename a video file.

- Cut tab is currently not functional but meant to be able to cut a video between specified timestamps and return the cut file.

***Anytime application is being used after installation just launch OBS first then launch the application. Audio is automatically muted but feel free to double check before saying something 'spicy'.***

=======
# DTS_repairs_obs_record

Connects to OBS via OBS Web Server. Allows the user to name a recording, then start and stop said recording (OBS has to be open). File is renamed after the recording is stopped in the location where it was saved by OBS.

Written in Python.