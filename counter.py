class VehicleCounter:

    def __init__(self):

        self.counted_ids = set()

        self.counts = {
            "Car":0,
            "Motorcycle":0,
            "Bus":0,
            "Truck":0
        }

    def update(self, vehicle_id, vehicle_class):

        if vehicle_id in self.counted_ids:
            return

        self.counted_ids.add(vehicle_id)

        if vehicle_class in self.counts:
            self.counts[vehicle_class] += 1

    def get_counts(self):
        return self.counts