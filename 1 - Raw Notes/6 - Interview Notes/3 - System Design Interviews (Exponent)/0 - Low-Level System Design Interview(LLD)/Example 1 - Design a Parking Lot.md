Date: 2026-03-02
Course:
Tags: 

# Design a Parking Lot

```python
Interviewer: "Design a parking lot system"

Step 1 — Ask clarifying questions:
  - how many floors?
  - what vehicle types? (car, bike, truck)
  - how is pricing calculated?
  - any reservations or just walk-in?

Step 2 — Identify classes:
  ParkingLot
  ├── Floor
  │   └── ParkingSpot
  │       ├── CarSpot
  │       ├── BikeSpot
  │       └── TruckSpot
  ├── Vehicle
  │   ├── Car
  │   ├── Bike
  │   └── Truck
  ├── Ticket
  ├── Payment
  └── ParkingAttendant

Step 3 — Define relationships:
  ParkingLot has many Floors         (composition)
  Floor has many ParkingSpots        (composition)
  ParkingSpot is assigned a Vehicle  (association)
  Ticket links Vehicle to ParkingSpot

Step 4 — Write key code:
```

```python
from enum import Enum
from datetime import datetime

class VehicleType(Enum):
    CAR = 1
    BIKE = 2
    TRUCK = 3

class Vehicle:
    def __init__(self, plate, vehicle_type):
        self.plate = plate
        self.vehicle_type = vehicle_type

class ParkingSpot:
    def __init__(self, spot_id, spot_type):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.vehicle = None          # None means empty

    def is_available(self):
        return self.vehicle is None

    def assign(self, vehicle):
        self.vehicle = vehicle

    def free(self):
        self.vehicle = None

class Ticket:
    def __init__(self, vehicle, spot):
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.now()
        self.exit_time = None

    def calculate_fee(self, rate_per_hour=10):
        self.exit_time = datetime.now()
        hours = (self.exit_time - self.entry_time).seconds / 3600
        return max(1, hours) * rate_per_hour  # minimum 1 hour charge

class ParkingLot:
    def __init__(self):
        self.spots = {
            VehicleType.CAR:   [ParkingSpot(i, VehicleType.CAR)   for i in range(10)],
            VehicleType.BIKE:  [ParkingSpot(i, VehicleType.BIKE)  for i in range(5)],
            VehicleType.TRUCK: [ParkingSpot(i, VehicleType.TRUCK) for i in range(3)]
        }
        self.tickets = {}

    def park(self, vehicle):
        # find available spot for vehicle type
        available = [s for s in self.spots[vehicle.vehicle_type] if s.is_available()]
        if not available:
            return None  # lot is full

        spot = available[0]
        spot.assign(vehicle)
        ticket = Ticket(vehicle, spot)
        self.tickets[vehicle.plate] = ticket
        return ticket

    def leave(self, plate):
        if plate not in self.tickets:
            return None

        ticket = self.tickets.pop(plate)
        fee = ticket.calculate_fee()
        ticket.spot.free()           # free up the spot
        return fee
```

# Note


# Reference

