from config import SUPABASE_KEY, SUPABASE_URL
from supabase import create_client, Client
from faker import Faker
from utils.util import generate_random_phone_number
import random

fake = Faker()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def insert_flight_prices():
    flights = supabase.table('flights').select().execute().data
    flight_price_records = []
    for flight in flights:
        flight_id = flight['id']
        aircraft_id = flight['aircraft_id']
        if aircraft_id == 1:
            economy_price = 50
            business_price = 250
        else:
            economy_price = 100
            business_price = 300
        
        flight_price_records.append({
            "flight_id": flight_id,
            "class_name": "ECONOMY",
            "base_price": economy_price,
            "tax_percentage": 10
        })

        flight_price_records.append({
            "flight_id": flight_id,
            "class_name": "BUSINESS",
            "base_price": business_price,
            "tax_percentage": 10
        })
    res = supabase.table('flight_class_pricing').insert(flight_price_records).execute()
    print(res.count)


def insert_avail_flight_seats():
    flights = supabase.table('flights').select().execute().data
    flight_seats_records = []
    aircraft_1_seats = supabase.table("seats").select("id").eq('aircraft_id', 1).execute().data
    aircraft_2_seats = supabase.table("seats").select("id").eq('aircraft_id', 2).execute().data
    for flight in flights:
        flight_id = flight['id']
        aircraft_id = flight['aircraft_id']
        if aircraft_id == 1:
            for seat in aircraft_1_seats:
                flight_seats_records.append({
                    "flight_id": flight_id,
                    "seat_id": seat['id'],
                    "is_available": True
                })
        else:
            for seat in aircraft_2_seats:
                flight_seats_records.append({
                    "flight_id": flight_id,
                    "seat_id": seat['id'],
                    "is_available": True
                })

    res = supabase.table('flight_seat_availability').insert(flight_seats_records).execute()
    print(res.count)


def insert_users():
    number_of_users = 10
    for i in range(number_of_users):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        username = fake.user_name()
        password = "abcdef123"
        if i == 0 or i == 5:
            role = "admin"
        else:
            role = "user"
        res = supabase.auth.sign_up({"email": email, "password": password})
        supabase.table("users").insert({
            "id": res.user.id,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "role": role
        }).execute()
    
    print("Users inserted")


def temp_query():
    meals = supabase.table("services").select("name").eq("type", "MEAL").execute().data
    luggages = supabase.table("services").select("name").eq("type", "LUGGAGE").execute().data

    print(meals)
    print(luggages)

def insert_bookings():
    users = supabase.table("users").select("id").execute().data
    flights = supabase.table("flights").select("id").execute().data
    meals = supabase.table("services").select("id", "price").eq("type", "MEAL").execute().data
    print(len(users))
    luggages = supabase.table("services").select("id", "price").eq("type", "LUGGAGE").eq("id", 11).execute().data
    try:
        for i in range(100):

            print(f"Inserting booking number {i}")
            user = random.choice(users)
            # create booking record
            user_id = user['id']
            flight_id = random.choice(flights)['id']
            class_name = random.choice(["ECONOMY", "BUSINESS"])
            trip_type = "ONE_WAY"

            ticket_price = supabase.table("flight_class_pricing").select("base_price").eq("flight_id", flight_id).eq("class_name", class_name).execute().data[0]['base_price']
            number_of_passengers = random.randint(1, 3)

            total_amount = ticket_price * number_of_passengers
            res = supabase.table("bookings").insert({
                "user_id": user_id,
                "booking_status": "CONFIRMED",
                "total_amount": total_amount,
                "number_of_passengers": number_of_passengers,
                "class_name": class_name,
                "trip_type": trip_type
            }).execute()
            # create passenger records for that booking

            print("Finished booking")

            booking_id = res.data[0]['id']
            # associate booking with flight
            res = supabase.table("booking_flight").insert({
                "booking_id": booking_id,
                "flight_id": flight_id,
                "leg_number": 1 # ONE_WAY TRIP
            }).execute()

            booking_flight_id = res.data[0]['id']
            
            seats_with_chosen_class = supabase.table("flight_seat_availability").select("seat_id, seats!flight_seat_availability_seat_id_fkey(class_name)").eq("flight_id", flight_id).eq("is_available", True).execute().data
            random_seats = random.sample(seats_with_chosen_class, number_of_passengers)
            passengers_id = []

            # create passenger records
            for i in range(number_of_passengers):
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = fake.email()
                birthday = fake.date_of_birth()
                phone_number = generate_random_phone_number("VN")
                res = supabase.table("passengers").insert({
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "gender": random.choice(["MALE", "FEMALE"]),
                    "birthday": birthday.strftime("%Y-%m-%d %H:%M:%S"),
                    "phone": phone_number,
                }).execute()
                passengers_id.append(res.data[0]['id'])

            # associate seats with passengers

            for i in range(number_of_passengers):
                passenger_id = passengers_id[i]
                seat_id = random_seats[i]['seat_id']
                res = supabase.table("booking_passenger_seat").insert({
                    "booking_flight_id": booking_flight_id,
                    "passenger_id": passenger_id,
                    "seat_id": seat_id
                }).execute()

                # update seat availability
                res = supabase.table("flight_seat_availability").update({"is_available": False}).eq("flight_id", flight_id).eq("seat_id", seat_id).execute()

            print("Finished associating passengers with seats")

            services_count = []
            
            meal = random.choice(meals)
            luggage = random.choice(luggages)
            services_count.append({
                "booking_flight_id": booking_flight_id,
                "service_id": meal['id'],
                "quantity": random.randint(1, 5),
                "total_price": meal['price'] * 3
            })

            services_count.append({
                "booking_flight_id": booking_flight_id,
                "service_id": luggage['id'],
                "quantity": 1,
                "total_price": luggage['price'] * random.randint(1, 20)
            })

            service_res = supabase.table("booking_flight_service").insert(services_count).execute()
            print("Finished associating services with booking")

    except Exception as e:
        print(str(e))
if __name__ == "__main__":
    # insert_flight_prices()
    # insert_avail_flight_seats()
    # insert_users()
    insert_bookings()
    # temp_query()
