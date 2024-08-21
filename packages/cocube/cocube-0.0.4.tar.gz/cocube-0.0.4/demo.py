from cocube import CoCube

client = CoCube()
found_devices = client.discover(timeout=5)
print("found devices:", found_devices)
# connect all discovered devices
devices = [CoCube(i) for i in found_devices]

for index, device in enumerate(devices):
    device.display_character(index)