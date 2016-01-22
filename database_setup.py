import os
import sys	
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper,create_session,relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Events(Base):
	__tablename__ = 'events'

	id = Column(Integer, primary_key = True)
	name = Column(String(40))
	date = Column(String(20))
	venue = Column(String(40))
	time = Column(String(10))
	speakers = Column(String(30))
	status = Column(Boolean)
	description = Column(String(200))

	@property
	def serialize(self):
	    return {
	    	'ID':self.id,
	    	'Event Name':self.name,
	    	'Date':self.date,
	    	'Venue':self.venue,
	    	'Time':self.time,
	    	'Speakers':self.speakers,
	    	'Status':self.status,
	    	'Description':self.description
	    }

class Projects(Base):
	__tablename__ = 'projects'

	id = Column(Integer, primary_key = True)
	name = Column(String(40))
	lead = Column(String(30))
	members = Column(String(100))
	language = Column(String(20))
	github = Column(String(50))
	publish_link = Column(String(50))
	description = Column(String(200))

	@property
	def serialize(self):
	    return {	 
	    	'ID':self.id,
	    	'Event Name':self.name,
	    	'Project Lead':self.lead,
	    	'Members':self.members,
	    	'Language':self.language,
	    	'GitHub Link':self.github,
	    	'Published link':self.publish_link,
	    	'Description':self.description
	    }
	

engine = create_engine('sqlite:///api.db')
Base.metadata.create_all(engine)