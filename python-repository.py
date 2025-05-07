import os
import time
import shutil

# ---------- Display Welcome Message ----------
def show_welcome_message():
    terminal_size = shutil.get_terminal_size((80, 20))
    welcome_msg = "                                                     **********WELCOME TO RIDE HAILING SYSTEM**********                          "
    print("\n" * 5)
    print(welcome_msg.center(terminal_size.columns))
    time.sleep(2)


# ---------- Core Classes ----------
class User:
    def __init__(self, user_id, name, email, phone, user_type):
        self.userID = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.userType = user_type

    def register_user(self):
        print(f"User registered: {self.name}")

    def login(self):
        print(f"User logged in: {self.name}")

    def update_profile(self, new_email, new_phone):
        self.email = new_email
        self.phone = new_phone
        print(f"Profile updated for: {self.name}")


class Driver(User):
    def __init__(self, user_id, name, email, phone, driver_id, license_number, vehicle):
        super().__init__(user_id, name, email, phone, "Driver")
        self.driverID = driver_id
        self.licenseNumber = license_number
        self.vehicle = vehicle

    def accept_ride_request(self):
        print(f"Driver {self.name} accepted the ride request.")

    def show_details(self):
        print(f"Driver Name: {self.name}")
        print(f"License Number: {self.licenseNumber}")
        print(f"Vehicle: {self.vehicle}")
        print(f"Phone: {self.phone}")


class Rider(User):
    def __init__(self, user_id, name, email, phone, rider_id, payment_method=None):
        super().__init__(user_id, name, email, phone, "Rider")
        self.riderID = rider_id
        self.paymentMethod = payment_method

    def request_ride(self):
        print(f"{self.name} requested a ride.")

    def choose_payment_method(self):
        print("\nChoose your payment method: Cash, Credit, Debit, Easypaisa")
        method = input("Enter method: ").strip().lower()
        self.paymentMethod = method.capitalize()
        print(f"Payment method selected: {self.paymentMethod}")


class Ride:
    def __init__(self, ride_id, rider_id, driver_id, start_location, end_location, fare):
        self.rideID = ride_id
        self.riderID = rider_id
        self.driverID = driver_id
        self.startLocation = start_location
        self.endLocation = end_location
        self.status = "Requested"
        self.fare = fare

    def start_ride(self):
        self.status = "In Progress"
        print("\nRide has started...")

    def end_ride(self):
        self.status = "Completed"
        print("Ride completed. Thank you for riding with us!")


class Payment:
    def __init__(self, ride_id, amount, payment_method):
        self.rideID = ride_id
        self.amount = amount
        self.paymentMethod = payment_method
        self.paymentStatus = "Pending"

    def process_payment(self):
        self.paymentStatus = "Processed"
        print(f"\nPayment of Rs.{self.amount} processed using {self.paymentMethod}.")


# ---------- Ride Scheduling ----------
class RideRequest:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0


def round_robin_scheduling(requests, time_quantum):
    time = 0
    queue = []
    gantt_chart = []
    completed = 0
    n = len(requests)
    visited = [False] * n

    while completed < n:
        for i in range(n):
            if requests[i].arrival_time <= time and not visited[i]:
                queue.append(i)
                visited[i] = True

        if not queue:
            time += 1
            continue

        idx = queue.pop(0)
        req = requests[idx]
        exec_time = min(time_quantum, req.remaining_time)
        time += exec_time
        req.remaining_time -= exec_time
        gantt_chart.append((req.pid, time))

        for i in range(n):
            if requests[i].arrival_time <= time and not visited[i]:
                queue.append(i)
                visited[i] = True

        if req.remaining_time > 0:
            queue.append(idx)
        else:
            req.completion_time = time
            req.turnaround_time = req.completion_time - req.arrival_time
            req.waiting_time = req.turnaround_time - req.burst_time
            completed += 1

    return gantt_chart


# ---------- Main Program ----------
if __name__ == "__main__":
    show_welcome_message()

    # Manual Rider Input
    name = input("Enter your name to register: ").strip()
    email = input("Enter your email: ").strip()
    phone = input("Enter your phone number: ").strip()
    rider = Rider(1, name, email, phone, rider_id=1001)
    rider.register_user()
    rider.login()

    # Driver Setup
    driver = Driver(2, "Adeel", "adeel@example.com", "03001234567", 2001, "DLB2345", "Toyota Corolla")
    driver.accept_ride_request()
    driver.show_details()

    # Ride Process
    rider.request_ride()
    ride = Ride(101, rider.userID, driver.userID, "Model Town", "Gulberg", 350)
    ride.start_ride()
    ride.end_ride()

    # Payment
    rider.choose_payment_method()
    payment = Payment(ride.rideID, ride.fare, rider.paymentMethod)
    payment.process_payment()

    # Round Robin Scheduling Simulation
    print("\n---- Simulating Round Robin Scheduling for Ride Requests ----")
    requests = [
        RideRequest("R1", 0, 5),
        RideRequest("R2", 1, 3),
        RideRequest("R3", 2, 8),
        RideRequest("R4", 3, 6)
    ]
    time_quantum = 4
    gantt_chart = round_robin_scheduling(requests, time_quantum)

    print("\n{:<10} {:<10} {:<10} {:<15} {:<15} {:<10}".format("Ride ID", "Arrival", "Burst", "Completion", "Turnaround", "Waiting"))
    for r in requests:
        print("{:<10} {:<10} {:<10} {:<15} {:<15} {:<10}".format(
            r.pid, r.arrival_time, r.burst_time,
            r.completion_time, r.turnaround_time, r.waiting_time
        ))

    print("\nGantt Chart:")
    timeline = "0"
    for pid, t in gantt_chart:
        print(f"| {pid} ", end="")
        timeline += f"   {t}"
    print("|")
    print(timeline)
