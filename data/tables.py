from data.models.Base import *

activity_tag = Table('ActivityTag', Base.metadata,
                     Column("activity_id", Integer, ForeignKey("Activity.id")),
                     Column("tag_id", Integer, ForeignKey("Tag.id"))
                     )


class Activity(Base):
    __tablename__ = 'Activity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    subtitle = Column(String)
    description = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    cover_image = Column(String)

    host_id = Column(Integer, ForeignKey("Host.id"))
    host = relationship("Host")

    tags = relationship("Tag",
                        secondary=activity_tag,
                        back_populates="activities")


class Host(Base):
    __tablename__ = 'Host'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    profile_photo = Column(String)
    location = Column(String)

    activities = relationship("Activity", back_populates="host")


class Event(Base):
    __tablename__ = 'Event'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)

    address_1 = Column(String)
    address_2 = Column(String)
    city = Column(String)
    state = Column(String)
    postcode = Column(String)
    country = Column(String)

    gps = Column(String)

    owner_id = Column(Integer, ForeignKey("User.id"))
    owner = relationship("User")

    def find_gps(self):
        # Send the address to a library that then sets the GPS from it.
        pass


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    pword = Column(String, nullable=False)

    events = relationship("Event", back_populates="owner")


class Location(Base):
    __tablename__ = 'Location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    gps = Column(String)

    floors = relationship("Floor", back_populates="location")


class Floor(Base):
    __tablename__ = 'Floor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    map_src = Column(String)

    location_id = Column(Integer, ForeignKey("Location.id"))
    location = relationship("Location")


class Room(Base):
    __tablename__ = 'Room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    pin_x = Column(Integer)
    pin_y = Column(Integer)

    floor_id = Column(Integer, ForeignKey("Floor.id"))
    floor = relationship("Floor")

    def get_coords(self):
        return [self.pin_x, self.pin_y]


class Tag(Base):
    __tablename__ = 'Tag'
    id = Column(Integer, primary_key=True, autoincrement=True)

    activities = relationship("Activity",
                              secondary=activity_tag,
                              back_populates="tags")


session = sessionmaker()
session.configure(bind=engine)
Base.metadata.bind = engine
Base.metadata.create_all(engine)


def add_to_db(item):
    db_session = session()
    db_session.add(item)
    db_session.commit()
    db_session.flush()
    db_session.refresh(item)
    json_data = item.json()
    db_session.close()
    return json_data


if __name__ == '__main__':
    db_session = session()
    db_session.add(User(
        email="friff14@gmail.com",
        pword="$5$rounds=535000$BJwX2AvGJUsqAIl2$D1AUrNjwvYBIJxoYQZ8qZuQcN4nhVPEEprtF2OU7oQ."
    ))
    db_session.commit()
    db_session.close()
