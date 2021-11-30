
class Dummy_Sensor(base):
    __tablename__ = 'dummy_sensor'
    timestamp = Column(DateTime, primary_key=True, nullable=False)
    field = Column(Integer, ForeignKey('field.id'), primary_key=True, nullable=False)
    value = Column(Float)
    __table_args__ = (UniqueConstraint('field',
                                       'timestamp',
                                       name='UC_field_time'),)

class Dummy_Sensor(base):
    __tablename__ = 'dummy_sensor'
    timestamp = Column(DateTime, primary_key=True, nullable=False)
    field = Column(Integer, ForeignKey('field.id'), primary_key=True, nullable=False)
    value = Column(Float)
    __table_args__ = (UniqueConstraint('field',
                                       'timestamp',
                                       name='UC_field_time'),)

class input_from_dummydevice(base):
    __tablename__ = 'input_from_dummydevice'
    timestamp = Column(DateTime, primary_key=True, nullable=False)
    field = Column(Integer, ForeignKey('field.id'), primary_key=True, nullable=False)
    value = Column(Float)
    __table_args__ = (UniqueConstraint('field',
                                       'timestamp',
                                       name='UC_field_time'),)

class input_from_dummydevice(base):
    __tablename__ = 'input_from_dummydevice'
    timestamp = Column(DateTime, primary_key=True, nullable=False)
    field = Column(Integer, ForeignKey('field.id'), primary_key=True, nullable=False)
    value = Column(Float)
    __table_args__ = (UniqueConstraint('field',
                                       'timestamp',
                                       name='UC_field_time'),)
