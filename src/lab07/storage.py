

import json
from datetime import datetime
from pathlib import Path

from model import Bus


def bus_to_dict(bus):
    d = {
        "kind": "bus",
        "route_number": bus.route_number,
        "capacity": bus.capacity,
        "passenger_count": bus.passenger_count,
        "current_speed": bus.current_speed,
        "state": bus.state,
    }
    if bus.__class__.__name__ == "CityBus":
        d["kind"] = "city"
        d["fare"] = bus.fare
        d["stop_count"] = bus.stop_count
    elif bus.__class__.__name__ == "ExpressBus":
        d["kind"] = "express"
        d["zone"] = bus.zone
        d["speed_factor"] = bus.speed_factor
    return d


def dict_to_bus(d):
    from models import CityBus, ExpressBus

    route = d["route_number"]
    cap = d["capacity"]
    if d["kind"] == "city":
        bus = CityBus(route, cap, fare=d.get("fare", 45), stop_count=d.get("stop_count", 12))
    elif d["kind"] == "express":
        bus = ExpressBus(route, cap, zone=d.get("zone", "A"), speed_factor=d.get("speed_factor", 1.2))
    else:
        bus = Bus(route, cap)
    bus._state = d["state"]
    bus._passenger_count = d["passenger_count"]
    bus._current_speed = float(d["current_speed"])
    return bus


def save(buses: list, dates: dict, filepath: str) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    items = []
    for bus in buses:
        route = bus.route_number
        items.append({
            "added_at": dates.get(route, datetime.now().isoformat()),
            "bus": bus_to_dict(bus),
        })
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"items": items}, f, ensure_ascii=False, indent=2)


def load(filepath: str) -> tuple[list, dict]:
    path = Path(filepath)
    if not path.exists():
        return [], {}
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    buses = []
    dates = {}
    for row in data.get("items", []):
        bus = dict_to_bus(row["bus"])
        buses.append(bus)
        dates[bus.route_number] = row.get("added_at", "")
    return buses, dates
