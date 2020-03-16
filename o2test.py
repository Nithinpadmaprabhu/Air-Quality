# version, 1.0 or 1.1, which depends on the board in use
Version = 11

if (Version == 11):
    AMP = 121
else:
    AMP = 201

AMP = 121 # Needs to change to this
K_O2 = 7.43

sensor_voltage = (727 / 1024) * 3.3
sensor_voltage = sensor_voltage/float(AMP)*10000.0
Value_O2 = sensor_voltage/K_O2

print("Concentration of O2 is ")
print(Value_O2)
print("%")
