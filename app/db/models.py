#from sqlalchemy import Column, Integer, String, ForeignKey
#from sqlalchemy.orm import relationship
#from app.db.database import Base

#class User(Base):
    #__tablename__ = "users"
    #id = Column(Integer, primary_key=True)
    #email = Column(String, unique=True, nullable=False)
    #password = Column(String, nullable=False)
    #role = Column(String, default="user")

#class Listing(Base):
    #__tablename__ = "listings"
    #id = Column(Integer, primary_key=True)
    #title = Column(String)
    #owner_id = Column(Integer, ForeignKey("users.id"))

    #images = relationship("ListingImage", cascade="all, delete", back_populates="listing")

#class ListingImage(Base):
    #__tablename__ = "listing_images"
    #id = Column(Integer, primary_key=True)
    #listing_id = Column(Integer, ForeignKey("listings.id"))
    #url = Column(String, nullable=False)

    #listing = relationship("Listing", back_populates="images")
