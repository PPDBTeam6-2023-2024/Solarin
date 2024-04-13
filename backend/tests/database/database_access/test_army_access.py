import pytest
from sqlalchemy.orm import Session

from src.app.database.database_access.army_access import ArmyAccess
from src.app.models import Army

@pytest.fixture
def army_access(session: Session):
    return ArmyAccess(session)

def test_create_army(army_access: ArmyAccess, session: Session):
    # Create a new army
    army = Army(name="Test Army", size=1000)
    army_access.create_army(army)

    # Retrieve the army from the database
    db_army = session.query(Army).filter_by(name="Test Army").first()

    # Assert that the army was successfully created
    assert db_army is not None
    assert db_army.name == "Test Army"
    assert db_army.size == 1000

def test_get_army(army_access: ArmyAccess, session: Session):
    # Create a new army
    army = Army(name="Test Army", size=1000)
    session.add(army)
    session.commit()

    # Retrieve the army using the ArmyAccess class
    db_army = army_access.get_army("Test Army")

    # Assert that the retrieved army matches the expected values
    assert db_army is not None
    assert db_army.name == "Test Army"
    assert db_army.size == 1000

def test_update_army(army_access: ArmyAccess, session: Session):
    # Create a new army
    army = Army(name="Test Army", size=1000)
    session.add(army)
    session.commit()

    # Update the army's size
    army_access.update_army("Test Army", size=2000)

    # Retrieve the updated army from the database
    db_army = session.query(Army).filter_by(name="Test Army").first()

    # Assert that the army's size was successfully updated
    assert db_army is not None
    assert db_army.name == "Test Army"
    assert db_army.size == 2000

def test_delete_army(army_access: ArmyAccess, session: Session):
    # Create a new army
    army = Army(name="Test Army", size=1000)
    session.add(army)
    session.commit()

    # Delete the army
    army_access.delete_army("Test Army")

    # Retrieve the army from the database
    db_army = session.query(Army).filter_by(name="Test Army").first()

    # Assert that the army was successfully deleted
    assert db_army is Noneimport pytest
from sqlalchemy import select

from src.app.database.database_access.army_access import ArmyAccess

@pytest.fixture
def army_access(sessionmanager):
    return ArmyAccess(sessionmanager)

def test_get_army_by_id(army_access):
    # Create a test army
    army_id = 1
    army_name = "Test Army"
    army = {"id": army_id, "name": army_name}
    army_access.create_army(army)

    # Retrieve the army by ID
    retrieved_army = army_access.get_army_by_id(army_id)

    # Check if the retrieved army matches the created army
    assert retrieved_army["id"] == army_id
    assert retrieved_army["name"] == army_name

def test_create_army(army_access):
    # Create a test army
    army_id = 1
    army_name = "Test Army"
    army = {"id": army_id, "name": army_name}

    # Create the army in the database
    army_access.create_army(army)

    # Retrieve the army by ID
    retrieved_army = army_access.get_army_by_id(army_id)

    # Check if the retrieved army matches the created army
    assert retrieved_army["id"] == army_id
    assert retrieved_army["name"] == army_name

def test_update_army(army_access):
    # Create a test army
    army_id = 1
    army_name = "Test Army"
    army = {"id": army_id, "name": army_name}
    army_access.create_army(army)

    # Update the army's name
    new_army_name = "Updated Army"
    army_access.update_army(army_id, {"name": new_army_name})

    # Retrieve the updated army by ID
    updated_army = army_access.get_army_by_id(army_id)

    # Check if the army's name has been updated
    assert updated_army["name"] == new_army_name

def test_delete_army(army_access):
    # Create a test army
    army_id = 1
    army_name = "Test Army"
    army = {"id": army_id, "name": army_name}
    army_access.create_army(army)

    # Delete the army
    army_access.delete_army(army_id)

    # Try to retrieve the deleted army by ID
    deleted_army = army_access.get_army_by_id(army_id)

    # Check if the deleted army is None
    assert deleted_army is None