import obsws_python as obs

client = obs.ReqClient(host="localhost", port="4455", password="obsppman")

Event = obs.EventClient(host="localhost", port="4455", password="obsppman")

data = client.get_scene_item_id("Scene", "Image")


print(data.scene_item_id)