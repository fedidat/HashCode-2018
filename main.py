import random

num = 200

filename = "input/b_should_be_easy.in"


def output_sol(vehicles_to_rides):
    outputfl = open("output/" + filename[6] + "_output.txt", "w")
    outputfl.write("\n".join([str(len(v2r)) + " " + " ".join([str(a) for a in v2r]) for v2r in vehicles_to_rides]))
    outputfl.close()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return str((self.x, self.y))


class Vehicle:
    def __init__(self, index, next_free_time, next_free_point):
        self.index = index
        self.next_free_time = next_free_time
        self.next_free_point = next_free_point

    def __repr__(self):
        return str((self.index, self.next_free_time, self.next_free_point.x, self.next_free_point.y))

    def next_time_free(self, ride):
        return max(ride.start_time, self.get_distance_to_start(ride) + self.next_free_time) + ride.get_ride_dist()

    def get_distance_to_start(self, ride):
        return abs(self.next_free_point.x - ride.start_point.x) + abs(self.next_free_point.y - ride.start_point.y)


class Ride:
    def __init__(self, (index, start_x, start_y, finish_x, finish_y, start_time, finish_time)):
        self.start_point = Point(start_x, start_y)
        self.finish_point = Point(finish_x, finish_y)
        self.start_time = start_time
        self.fin = finish_time
        self.index = index

    def __repr__(self):
        return str((self.index, self.start_point, self.finish_point, self.start_time, self.fin))

    def get_ride_dist(self):
        return abs(self.finish_point.x - self.start_point.x) + abs(self.finish_point.y - self.start_point.y)

    def is_feasible(self, vehicle):
        return vehicle.get_distance_to_start(self) + self.get_ride_dist() <= (self.fin - vehicle.next_free_time) \
               and self.get_ride_dist() <= (self.fin - self.start_time)

    def is_earliest_start_possible(self, vehicle):
        return vehicle.get_distance_to_start(self) <= (self.start_time - vehicle.next_free_time)


def vehicle_to_ride_score(vehicle, ride, bonus):
    score = 0
    if not ride.is_feasible(vehicle):
        return score
    distance_score = ride.get_ride_dist()
    bonus_score = ride.is_earliest_start_possible(vehicle) * bonus
    score = distance_score + bonus_score
    return score


def find_next_free_veh_and_pop(status):
    mn = min(status[:num], key=lambda x: x.next_free_time)
    status.remove(mn)
    return mn


def get_next_ride(veh, remaining_rides, bonus):
    return max(remaining_rides[:num], key=lambda ride: vehicle_to_ride_score(veh, ride, bonus))


def solve_problem(vehicles, rides_num, bonus, steps, rides):
    vehicles_to_rides = [[] for _ in range(rides_num)]  # maps each vehicle to the list of rides it takes
    status = [Vehicle(v_index, 0, Point(0, 0)) for v_index in range(vehicles)]  # vehicle id, time free, next free point
    i = 0
    while len(rides) > 0:
        i += 1
        if i % 10 == 0:
            random.shuffle(rides)
            random.shuffle(status)
        veh = find_next_free_veh_and_pop(status)  # find the next free vehicle
        if veh.next_free_time >= steps:
            break
        next_ride = get_next_ride(veh, rides, bonus)  # find next ride of free vehicle
        rides.remove(next_ride)  # mark ride as removed
        vehicles_to_rides[veh.index].append(next_ride.index)  # remember next ride for vehicle
        status.append(Vehicle(veh.index, veh.next_time_free(next_ride),
                              Point(next_ride.finish_point.x, next_ride.finish_point.y)))  # adding vehicle to status
    return vehicles_to_rides


def __main__():
    f = open(filename)
    lines = f.read().split("\n")
    (rows, cols, vehicles, rides_num, bonus, steps) = [int(x) for x in lines[0].split()]

    rides = [Ride([i - 1] + [int(x) for x in lines[i].split()]) for i in range(1, len(lines) - 1)]
    f.close()

    vehicles_to_rides = solve_problem(vehicles, rides_num, bonus, steps, rides)
    output_sol(vehicles_to_rides)


if __name__ == "__main__":
    __main__()
