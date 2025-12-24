import numpy as np
import cv2
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# -------- INIT --------
client = RemoteAPIClient()
sim = client.require('sim')

vision = sim.getObject('/visionSensor')

print("🔧 Disabling stepping mode...")
sim.setStepping(False)

print("▶️ Starting simulation...")
sim.startSimulation()

# WAIT until simulation is running
while sim.getSimulationState() != sim.simulation_advancing_running:
    time.sleep(0.05)

print("✅ Simulation fully running")

# Give sensors time to initialize
time.sleep(0.5)

# -------- VIDEO LOOP --------
start_time = time.time()
RUN_TIME = 15  # seconds

while time.time() - start_time < RUN_TIME:

    img_raw, res = sim.getVisionSensorImg(vision)

    img = np.frombuffer(img_raw, dtype=np.uint8)
    img = img.reshape(res[1], res[0], 3)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.flip(img, 0)

    cv2.imshow("Vision Sensor", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -------- CLEAN SHUTDOWN --------
print("⏹ Stopping simulation...")
sim.stopSimulation()

while sim.getSimulationState() != sim.simulation_stopped:
    time.sleep(0.05)

cv2.destroyAllWindows()
print("🛑 Simulation stopped cleanly")
