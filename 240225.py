import csv
import random
from datetime import datetime, timedelta

# Define time slots and their respective frequency intervals
time_slots = {
    "Pre AM Peak": ("06:00", "07:30", (15, 20)),  # Frequency between 15-20 minutes
    "AM Peak": ("07:30", "09:30", (3, 5)),  # Frequency between 3-5 minutes
    "Off-Peak": ("09:30", "14:00", (12, 15)),  # Frequency between 12-15 minutes
    "PM Peak": ("14:00", "20:30", (5, 9)),  # Frequency between 5-9 minutes
    "Evening": ("20:30", "23:30", (10, 15))  # Frequency between 10-15 minutes
}

# Stops in order
stops = ["114th Avenue", "C (Business Area)", "B (Suburb)"]
stops_reverse = stops[::-1]  # Reverse order for return trips

# Function to determine if a service is express
def is_express(time_slot, direction):
    if direction == "Outbound":  # From 114th Avenue
        if time_slot == "AM Peak":
            return random.choice([(True, "114th -> C"), (False, "Full Route")])
        elif time_slot == "PM Peak":
            return random.choice([(True, "114th -> B"), (False, "Full Route")])
    else:  # Inbound (to 114th Avenue)
        if time_slot == "AM Peak":
            return random.choice([(True, "B -> 114th"), (False, "Full Route")])
        elif time_slot == "PM Peak":
            return random.choice([(True, "C -> 114th"), (False, "Full Route")])
    return (False, "Full Route")

# Function to generate schedules
def generate_schedule(output_file, direction, first_service, last_service):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'Direction', 'Departure Time', 'Arrival Time', 'Stop 1', 'Stop 2', 'Stop 3', 'Is Express'
        ])
        writer.writeheader()

        # Ensure the first service is fixed
        current_time = datetime.strptime(first_service, "%H:%M")
        last_time = datetime.strptime(last_service, "%H:%M")
        
        while current_time <= last_time:
            # Determine the current time slot
            time_slot = next(slot for slot, (start, end, _) in time_slots.items()
                             if datetime.strptime(start, "%H:%M") <= current_time <= datetime.strptime(end, "%H:%M"))
            
            # Determine if service is express or full route
            express_status, express_type = is_express(time_slot, direction)
            if express_status:
                if express_type == "114th -> B":
                    stops_service = [stops[0], stops[2]]
                elif express_type == "114th -> C":
                    stops_service = [stops[0], stops[1]]
                elif express_type == "B -> 114th":
                    stops_service = [stops[2], stops[0]]
                else:  # "C -> 114th"
                    stops_service = [stops[1], stops[0]]
                express_str = "Yes"
            else:
                stops_service = stops if direction == "Outbound" else stops_reverse  # Normal service
                express_str = "No"
            
            # Calculate travel time
            base_travel_time = random.randint(35, 55)  # Random travel time between 35-55 minutes
            arrival_time = current_time + timedelta(minutes=base_travel_time)
            
            # Write to CSV
            writer.writerow({
                'Direction': " -> ".join(stops_service),
                'Departure Time': current_time.strftime("%H:%M"),
                'Arrival Time': arrival_time.strftime("%H:%M"),
                'Stop 1': stops_service[0],
                'Stop 2': stops_service[1] if len(stops_service) > 1 else "",
                'Stop 3': stops_service[2] if len(stops_service) > 2 else "",
                'Is Express': express_str
            })
            
            # Increment departure time by a random frequency in the given range
            min_freq, max_freq = time_slots[time_slot][2]
            current_time += timedelta(minutes=random.randint(min_freq, max_freq))

# Generate schedules for both directions with fixed first and last services
generate_schedule("schedule_114th_to_B.csv", "Outbound", "06:30", "23:30")
generate_schedule("schedule_B_to_114th.csv", "Inbound", "06:00", "23:00")

print("CSV files successfully generated.")
