"""Simple synthetic feedback for price-demand."""
import random, math

class MarketSimulator:
    def __init__(self):
        self.properties = self._bootstrap()

    def _bootstrap(self):
        data = []
        for i in range(10):
            data.append(
                {
                    "id": f"PROP{i}",
                    "base_price": random.randint(5000, 8000),
                    "price": None,
                    "size": random.choice([1, 2, 3]),
                    "location": random.choice(["Downtown", "Marina", "Creek"]),
                }
            )
        return data

    def sample_state(self):
        p = random.choice(self.properties)
        if p["price"] is None:
            p["price"] = p["base_price"]
        return p

    def apply_action(self, prop_id: str, action: str):
        p = next(x for x in self.properties if x["id"] == prop_id)
        if action == "decrease_price":
            p["price"] *= 0.95
        elif action == "increase_price":
            p["price"] *= 1.05
        demand = math.exp(-(p["price"] - p["base_price"]) / 1000)
        occupancy = max(0.0, min(1.0, demand))
        revenue = occupancy * p["price"]
        return {"new_price": round(p["price"], 2), "occupancy": occupancy, "revenue": revenue}