from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
import datetime

Base = declarative_base()

class Guest(Base):
    __tablename__ = 'guests'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String)
    
    bookings = relationship("Booking", back_populates="guest")

    def __repr__(self):
        return f"<Guest(id={self.id}, name='{self.name}', phone='{self.phone}')>"

class Room(Base):
    __tablename__ = 'rooms'
    
    id = Column(Integer, primary_key=True)
    room_number = Column(String, unique=True, nullable=False)
    room_type = Column(String)
    price_per_night = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
    
    bookings = relationship("Booking", back_populates="room")

    def __repr__(self):
        return (f"<Room(id={self.id}, room_number='{self.room_number}', "
                f"type='{self.room_type}', price={self.price_per_night})>")

class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True)
    guest_id = Column(Integer, ForeignKey('guests.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=False)
    
    guest = relationship("Guest", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
    
    def __repr__(self):
        return (f"<Booking(id={self.id}, guest_id={self.guest_id}, "
                f"room_id={self.room_id}, check_in='{self.check_in_date}', "
                f"check_out='{self.check_out_date}')>")