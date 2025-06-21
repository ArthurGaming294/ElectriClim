from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import tinytuya

app = Flask(__name__)

# Charger les appareils depuis devices.json
with open("devices.json") as f:
    DEVICES = json.load(f)

def get_device(key):
    dev_info = DEVICES[key]
    d = tinytuya.OutletDevice(dev_info["id"], dev_info["ip"], dev_info["key"])
    d.set_version(float(dev_info.get("version", 3.3)))
    return d

# Récupérer le statut d’un device
def fetch_status(dev):
    try:
        data = dev.status().get("dps", {})

        raw_mode = data.get("4")
        raw_fan = data.get("5")

        mode = None
        if isinstance(raw_mode, str):
            mode_map = {"auto": 0, "cold": 1, "heat": 2, "dry": 3, "dehumidify": 3, "fan": 4}
            mode = mode_map.get(raw_mode.lower(), -1)
        elif raw_mode is not None:
            mode = int(raw_mode)
        else:
            mode = -1

        fan = None
        if isinstance(raw_fan, str):
            fan_map = {"auto": 0, "low": 1, "medium": 2, "mid": 2, "high": 3}
            fan = fan_map.get(raw_fan.lower(), -1)
        elif raw_fan is not None:
            fan = int(raw_fan)
        else:
            fan = -1

        print(f"[DEBUG] raw_mode={raw_mode} mapped_mode={mode}, raw_fan={raw_fan} mapped_fan={fan}")

        return {
            "on": data.get("1", False),
            "temp_set": float(data["2"]) / 10 if "2" in data else None,
            "temp_room": float(data["3"]) / 10 if "3" in data else None,
            "mode": mode,
            "fan_speed": fan,
            "error": None,
            "raw_mode_type": type(raw_mode).__name__,
            "raw_fan_type": type(raw_fan).__name__,
        }
    except Exception as e:
        return {
            "on": None,
            "temp_set": None,
            "temp_room": None,
            "mode": None,
            "fan_speed": None,
            "error": str(e),
            "raw_mode_type": "unknown",
            "raw_fan_type": "unknown"
        }

@app.route("/")
def dashboard():
    status = {key: fetch_status(get_device(key)) for key in DEVICES}
    return render_template("index.html", devices=DEVICES, status=status)

@app.route("/api/<device_key>/<path:actions>", methods=["GET"])
def api_batch(device_key, actions):
    if device_key not in DEVICES:
        return jsonify(success=False, error=f"Device '{device_key}' not found"), 404

    dev = get_device(device_key)
    results = []

    # Exemple: "on+set_mode=2+set_temp=21.5"
    for action in actions.split("+"):
        try:
            if action == "on":
                dev.set_status(True)
                results.append({"action": "on", "success": True})
            elif action == "off":
                dev.set_status(False)
                results.append({"action": "off", "success": True})
            elif action == "toggle":
                current = dev.status().get("dps", {}).get("1", False)
                dev.set_status(not current)
                results.append({"action": "toggle", "success": True})
            elif action.startswith("set_mode="):
                value = int(action.split("=")[1])
                status = fetch_status(dev)
                mode_map = {0: "auto", 1: "cold", 2: "heat", 3: "dry", 4: "fan"}

                if status["raw_mode_type"] == "str":
                    val = mode_map.get(value, "auto")
                    dev.set_value("4", val)
                else:
                    current_status = dev.status()
                    if "dps" in current_status:
                        dps = current_status["dps"]
                        dps["4"] = value
                        dev.set_status(dps)
                    else:
                        dev.set_value("4", value)
                results.append({"action": f"set_mode={value}", "success": True})

            elif action.startswith("set_temp="):
                value = float(action.split("=")[1])
                dev.set_value("2", int(value * 10))
                results.append({"action": f"set_temp={value}", "success": True})

            elif action.startswith("set_fan="):
                value = int(action.split("=")[1])
                status = fetch_status(dev)
                if status["raw_fan_type"] == "str":
                    fan_map = {0: "auto", 1: "low", 2: "medium", 3: "high"}
                    val = fan_map.get(value, "auto")
                    dev.set_value("5", val)
                else:
                    dev.set_value("5", value)
                results.append({"action": f"set_fan={value}", "success": True})
            else:
                results.append({"action": action, "success": False, "error": "Unknown action"})

        except Exception as e:
            results.append({"action": action, "success": False, "error": str(e)})

    return jsonify(success=True, results=results)

# --- NOUVELLES ROUTES POST POUR LES FORMULAIRES ---

@app.route("/set_temp/<device_key>", methods=["POST"])
def set_temp(device_key):
    if device_key not in DEVICES:
        return "Device not found", 404
    temp = request.form.get("temp", type=float)
    if temp is None:
        return "Température invalide", 400
    # appel API avec action set_temp
    return redirect(url_for("api_batch", device_key=device_key, actions=f"set_temp={temp}"))

@app.route("/set_fan/<device_key>", methods=["POST"])
def set_fan(device_key):
    if device_key not in DEVICES:
        return "Device not found", 404
    fan_speed = request.form.get("fan_speed", type=int)
    if fan_speed is None:
        return "Vitesse ventilateur invalide", 400
    return redirect(url_for("api_batch", device_key=device_key, actions=f"set_fan={fan_speed}"))

@app.route("/set_mode/<device_key>", methods=["POST"])
def set_mode(device_key):
    if device_key not in DEVICES:
        return "Device not found", 404
    mode = request.form.get("mode", type=int)
    if mode is None:
        return "Mode invalide", 400
    return redirect(url_for("api_batch", device_key=device_key, actions=f"set_mode={mode}"))

@app.route("/api/<device_key>/toggle", methods=["POST"])
def toggle(device_key):
    if device_key not in DEVICES:
        return "Device not found", 404
    return redirect(url_for("api_batch", device_key=device_key, actions="toggle"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
