import click
from .database import Session
from .models import Guest, Room, Booking
from sqlalchemy.orm import selectinload
from datetime import datetime

ROOM_TYPES = ("Single", "Double", "Suite")

@click.group()
def cli():
    pass

def validate_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        raise click.BadParameter("Date must be in YYYY-MM-DD format.")

def get_session():
    return Session()

def display_info(title, data, headers):
    click.echo(f"\n--- {title} ---")
    header_str = " | ".join(headers)
    click.echo(header_str)
    click.echo("-" * len(header_str))
    
    for item in data:
        row = " | ".join(str(val) for val in item)
        click.echo(row)
    click.echo("-" * len(header_str))

@cli.command()
@click.option('--room-number', prompt='Room number')
@click.option('--room-type', prompt='Room type (Single/Double/Suite)', 
              type=click.Choice(ROOM_TYPES, case_sensitive=False))
@click.option('--price', prompt='Price per night', type=int)
def add_room(room_number, room_type, price):
    session = get_session()
    try:
        new_room = Room(
            room_number=room_number,
            room_type=room_type,
            price_per_night=price
        )
        session.add(new_room)
        session.commit()
        click.echo(f"Room {room_number} added successfully!")
    except Exception as e:
        session.rollback()
        click.echo(f"Error adding room: {e}")
    finally:
        session.close()

@cli.command()
def view_rooms():
    session = get_session()
    try:
        rooms = session.query(Room).all()
        room_data = [
            (r.id, r.room_number, r.room_type, r.price_per_night, 
             "Available" if r.is_available else "Booked") for r in rooms
        ]
        headers = ("ID", "Number", "Type", "Price", "Status")
        display_info("All Rooms", room_data, headers)
    finally:
        session.close()

@cli.command()
@click.option('--name', prompt='Guest name')
@click.option('--phone', prompt='Guest phone number')
def add_guest(name, phone):
    session = get_session()
    try:
        new_guest = Guest(name=name, phone=phone)
        session.add(new_guest)
        session.commit()
        click.echo(f"Guest '{name}' added successfully!")
    except Exception as e:
        session.rollback()
        click.echo(f"Error adding guest: {e}")
    finally:
        session.close()

@cli.command()
def view_guests():
    session = get_session()
    try:
        guests = session.query(Guest).all()
        guest_data = [(g.id, g.name, g.phone) for g in guests]
        headers = ("ID", "Name", "Phone")
        display_info("All Guests", guest_data, headers)
    finally:
        session.close()

@cli.command()
@click.option('--guest-id', prompt='Guest ID', type=int)
@click.option('--room-id', prompt='Room ID', type=int)
@click.option('--check-in', prompt='Check-in date (YYYY-MM-DD)', 
              callback=lambda ctx, param, value: validate_date(value))
@click.option('--check-out', prompt='Check-out date (YYYY-MM-DD)', 
              callback=lambda ctx, param, value: validate_date(value))
def book_room(guest_id, room_id, check_in, check_out):
    session = get_session()
    try:
        guest = session.query(Guest).get(guest_id)
        room = session.query(Room).get(room_id)

        if not guest:
            click.echo(f"Error: Guest with ID {guest_id} not found.")
            return
        
        if not room:
            click.echo(f"Error: Room with ID {room_id} not found.")
            return
            
        if not room.is_available:
            click.echo(f"Error: Room {room.room_number} is not available.")
            return

        if check_out <= check_in:
            click.echo("Error: Check-out date must be after check-in date.")
            return
            
        room.is_available = False
        new_booking = Booking(
            guest_id=guest_id, 
            room_id=room_id, 
            check_in_date=check_in, 
            check_out_date=check_out
        )
        session.add(new_booking)
        session.commit()
        click.echo(f"Room {room.room_number} booked for '{guest.name}' from {check_in} to {check_out}.")
    except Exception as e:
        session.rollback()
        click.echo(f"An unexpected error occurred: {e}")
    finally:
        session.close()

@cli.command()
def view_bookings():
    session = get_session()
    try:
        bookings = (session.query(Booking)
                        .options(selectinload(Booking.guest), selectinload(Booking.room))
                        .all())
        
        booking_details = {}
        for b in bookings:
            guest_name = b.guest.name if b.guest else "Unknown"
            room_number = b.room.room_number if b.room else "Unknown"
            
            if guest_name not in booking_details:
                booking_details[guest_name] = []
            
            booking_dict = {
                "booking_id": b.id,
                "room_number": room_number,
                "check_in": str(b.check_in_date),
                "check_out": str(b.check_out_date)
            }
            booking_details[guest_name].append(booking_dict)

        click.echo("\n--- All Bookings ---")
        for guest, bookings_list in booking_details.items():
            click.echo(f"\nGuest: {guest}")
            booking_table = []
            for booking_dict in bookings_list:
                booking_table.append([
                    booking_dict["booking_id"],
                    booking_dict["room_number"],
                    booking_dict["check_in"],
                    booking_dict["check_out"]
                ])
            headers = ("Booking ID", "Room Number", "Check-in", "Check-out")
            display_info("Booking Details", booking_table, headers)
            
    finally:
        session.close()