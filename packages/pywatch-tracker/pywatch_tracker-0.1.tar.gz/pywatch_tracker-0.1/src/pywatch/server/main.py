import json
import typing
from types import ModuleType

from quart import Quart, render_template, websocket

from .detector_logic_calculation import *
from ..readout import DetectorPool, EventData


setup_mod: typing.Optional[ModuleType] = None
app = Quart(__name__, template_folder="../dist/", static_folder="../dist/assets")

detectors = []


@app.route("/")
async def main():
    if setup_mod is None:
        raise RuntimeError("Setup Script was not set")
    return await render_template("index.html")


@app.websocket("/measurement")
async def ws():
    while True:
        data = (await websocket.receive_json())["data"]
        if data["type"] == "start":
            print("start measurement")
            event_count = data["eventCount"]

            async def callback(event: EventData):
                msg: dict = {
                    "type": "event",
                    "data": event.to_dict(),
                }

                await websocket.send_json(msg)

            if len(detectors) is None:
                print("No Detector geometry was given. Try Again")
                continue

            # pool = DetectorPool(*ports, threshold=10)
            # pool = SimulationPool(detector_count, 1, 0.01)
            if setup_mod.SIMULATION:
                # pool = SimulationPool(detectors, expected_wait_time, std_dev)
                # await pool.async_run(event_count, callback, (-2, 2), (-3, 20))
                raise NotImplementedError
            else:
                pool = DetectorPool(*setup_mod.PORTS, threshold=setup_mod.THRESHOLD)
                await pool.async_run(event_count, callback)
        else:
            continue


@app.websocket("/logic")
async def ws_logic():
    global detectors
    while True:
        data = await websocket.receive_json()
        # TODO load rotation
        for d in data:
            position = Vector(*d["position"].values())
            rot_values = [0, 0, 0, "XYZ"]
            if (v := d.get("rotation")) is not None:
                rot_values = list(v.values())[1:]

            detectors.append(Detector(setup_mod.SEGMENTATION, position, (rot_values[-1], Vector(*rot_values[:-1]))))

        detector_count = len(detectors)
        coin = calculate_coincidences(detectors)
        with open("test.json", "w") as f:
            json.dump(coin.to_dict(), f, indent=4)
        await websocket.send_json(coin.to_dict("mean"))
        print("logic send")

        # pprint(detectors)


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True)
