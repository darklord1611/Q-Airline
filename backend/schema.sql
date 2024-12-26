create table services (
  id serial not null primary key,
  name text not null,
  description text,
  type character not null,
  price numeric not null,
  is_active boolean,
  img_src text
);

create table airports (
  id serial not null primary key,
  iata_code character not null,
  name character not null,
  city character not null,
  country character not null,
  timezone character not null
);

create table aircrafts (
  id serial not null primary key,
  model character not null,
  manufacturer character not null,
  total_capacity character not null,
  seat_configuration jsonb
);

create table discounts (
  id serial not null primary key,
  name character not null,
  description text not null,
  discount_factor numeric not null,
  image_url text,
  start_time timestamp default now() not null,
  end_time timestamp default now() not null,
  is_active boolean,
  created_at timestamp default now(),
  updated_at timestamp default now()
);

create table routes (
  id serial not null primary key,
  departure_airport_id integer references airports (id),
  arrival_airport_id integer references airports (id),
  distance integer not null,
  created_at timestamp default now()
);

create table flights (
  id serial not null primary key,
  route_id integer references routes (id),
  arrival_time timestamp default now() not null,
  departure_time timestamp default now() not null,
  updated_at timestamp default now(),
  aircraft_id integer references aircrafts (id),
  is_active boolean not null,
  flight_status character not null,
  flight_number text
);

create table passengers (
  id serial not null primary key,
  birthday timestamp default now() not null,
  gender character,
  email character not null,
  phone character not null,
  first_name character not null,
  last_name character not null
);

create table users (
  id uuid default uuid_generate_v4() primary key,
  first_name character not null,
  last_name character not null,
  username text,
  phone character,
  created_at timestamp default now(),
  updated_at timestamp default now(),
  role character not null
);

create table news (
  id serial not null primary key,
  title character not null,
  body text not null,
  category character,
  visibility character,
  author_id uuid references users (id),
  created_at timestamp default now(),
  updated_at timestamp default now(),
  image_url text,
  external_article_link text
);

create table flight_audit (
  id serial not null primary key,
  flight_id integer references flights (id),
  route_id integer not null,
  arrival_time timestamp default now() not null,
  departure_time timestamp default now() not null,
  is_active boolean,
  updated_at timestamp default now(),
  aircraft_id integer not null,
  flight_status character not null,
  flight_number text
);

create table bookings (
  id serial not null primary key,
  user_id uuid references users (id),
  booking_status character not null,
  number_of_passengers integer not null,
  total_amount numeric not null,
  created_at timestamp default now(),
  trip_type character not null,
  class_name text not null
);

create table seats (
  id serial not null primary key,
  aircraft_id integer references aircrafts (id),
  seat_number character not null,
  class_name character not null
);

create table notifications (
  id serial not null primary key,
  title character not null,
  description text not null,
  type text not null,
  created_at timestamp default now()
);

create table payments (
  id serial not null primary key,
  booking_id integer references bookings (id),
  payment_method character not null,
  transaction_id character not null,
  payment_status character not null,
  amount_paid numeric not null,
  payment_date timestamp default now()
);

create table notification_user (
  id serial not null primary key,
  user_id uuid references users (id),
  notification_id integer references notifications (id),
  is_read boolean
);

create table booking_flight (
  id serial not null primary key,
  booking_id integer references bookings (id),
  flight_id integer references flights (id),
  leg_number integer not null
);

create table booking_flight_service (
  id serial not null primary key,
  booking_flight_id integer references booking_flight (id),
  service_id integer references services (id),
  quantity integer,
  total_price numeric
);

create table booking_passenger_seat (
  id serial not null primary key,
  booking_flight_id integer references booking_flight (id),
  passenger_id integer references passengers (id),
  seat_id integer references seats (id)
);

create table flight_seat_availability (
  id serial not null primary key,
  flight_id integer references flights (id),
  seat_id integer references seats (id),
  is_available boolean not null
);

create table flight_class_pricing (
  id serial not null primary key,
  flight_id integer references flights (id),
  base_price numeric not null,
  tax_percentage numeric,
  discount_percentage numeric,
  class_name character not null
);
