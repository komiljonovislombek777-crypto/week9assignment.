class BlendError(Exception):
    pass
class BlendNotFoundError(BlendError):
    def __init__(self, blend_name ):
        self.blend_name=blend_name
        super().__init__(f"blend not found: {blend_name}" )
class DuplicateBlendError(BlendError):
    def __init__(self, blend_name ):
        self.blend_name=blend_name
        super().__init__(f"blend already exists: {blend_name}" )
class InvalidPlotsError(BlendError):
    def __init__(self, plots):
        self.plots=plots
        super().__init__(f"invalid plots: {plots}. must be positive")
class MissingMineralsError(BlendError):
    def __init__(self, blend_name,missing):
        self.missing=missing
        self.blend_name=blend_name
        super().__init__(f"cannot prepare {blend_name}: missing {missing}" )
class BlendPlanner:
    def __init__(self):
        self.blends={}
    def add_blend(self, name, plots, minerals):
        if name in self.blends:
            raise DuplicateBlendError(name)
        if plots<=0:
            raise InvalidPlotsError(plots)
        self.blends[name] = {"plots": plots,"minerals": minerals}
    def scale_blend(self, name, desired_plots):
        if desired_plots <= 0:
            raise InvalidPlotsError(desired_plots)

        try:
            blend = self.blends[name]
        except KeyError:
            raise BlendNotFoundError(name)

        result = {}

        for mineral, amount in blend["minerals"].items():
                result[mineral] = round(amount * (desired_plots / blend["plots"]), 2)

        return result
    def check_stock(self, name, stock):
        try:
            blend = self.blends[name]
        except KeyError:
            raise BlendNotFoundError(name)
        missing = {}
        for mineral, needed in blend["minerals"].items():
            available = stock.get(mineral, 0)

            if available < needed:
                missing[mineral] = round(needed - available, 2)
        if missing:
            raise MissingMineralsError(name, missing)
        return True
planner = BlendPlanner()

planner.add_blend("Growth Mix", 5, {"nitrogen": 10.0, "phosphorus": 4.0, "potassium": 6.0})
planner.add_blend("Bloom Boost", 3, {"phosphorus": 9.0, "potassium": 3.0, "iron": 1.5})

scaled = planner.scale_blend("Growth Mix", 10)
print(f"growth mix for 10: {scaled}")

scaled = planner.scale_blend("Bloom Boost", 1)
print(f"bloom boost for 1: {scaled}")

stock = {"nitrogen": 10.0, "phosphorus": 1.0, "potassium": 6.0}
try:
    planner.check_stock("Growth Mix", stock)
except BlendError as e:
    print(e)

stock2 = {"phosphorus": 15.0, "potassium": 5.0, "iron": 3.0}
result = planner.check_stock("Bloom Boost", stock2)
print(f"can prepare bloom boost: {result}")

tests = [
    lambda: planner.add_blend("Growth Mix", 5, {"nitrogen": 2.0}),
    lambda: planner.scale_blend("Root Strong", 4),
    lambda: planner.scale_blend("Growth Mix", -3),
]

for test in tests:
    try:
        test()
    except BlendError as e:
        print(e)

    