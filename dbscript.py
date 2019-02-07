from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Sets up database ad creates a session to the database
Base = declarative_base()
engine = create_engine('sqlite:///example.sqlite', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Sets up the tables
class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)

    def __repr__(self):
        return '{} {}'.format(self.firstname, self.lastname)


# Creates all the tables
Base.metadata.create_all(engine)


# Example functions showing how to
def add_user_if_not_exists(username, firstname, lastname):
    result = session.query(Users).filter(Users.username == username).first()
    if result:
        return False
    else:
        session.add(Users(username=username, firstname=firstname, lastname=lastname))
        session.commit()
        return True

def update_existing_user(username, firstname, lastname):
    result = session.query(Users).filter(Users.username == username).first()
    if not result:
        return False
    else:
        result.firstname = firstname
        result.lastname = lastname
        session.commit()
        return True

if __name__ == '__main__':

    username = input('Enter Username: ')
    firstname = input('Enter First Name: ')
    lastname = input('Enter Last Name: ')

    print('adding a user')
    if add_user_if_not_exists(username, firstname, lastname) is True:
        print('User added successfully!')
    else:
        print('User already exists, updating information')
        if update_existing_user(username, firstname, lastname) is True:
            print('User updated successfully!')
        else:
            print('Unable to update user!')
