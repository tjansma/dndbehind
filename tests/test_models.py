import pytest
from dndbehind.models import User, Role, Character, Background


def test_user_creation(db_session):
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.check_password('password123') is True
    assert user.check_password('wrongpass') is False


def test_user_unique_constraints(db_session):
    user1 = User(username='testuser', email='test@example.com')
    user1.set_password('password123')
    db_session.add(user1)
    db_session.commit()

    # Test duplicate username
    with pytest.raises(Exception):
        user2 = User(username='testuser', email='different@example.com')
        user2.set_password('password123')
        db_session.add(user2)
        db_session.commit()

    # Test duplicate email
    with pytest.raises(Exception):
        user3 = User(username='different', email='test@example.com')
        user3.set_password('password123')
        db_session.add(user3)
        db_session.commit()


def test_user_role_relationship(db_session, test_user, admin_role):
    test_user.roles.append(admin_role)
    db_session.commit()

    assert admin_role in test_user.roles
    assert test_user in admin_role.users


def test_role_creation(db_session):
    role = Role(name='testrole', description='Test role description')
    db_session.add(role)
    db_session.commit()

    assert role.id is not None
    assert role.name == 'testrole'
    assert role.description == 'Test role description'


def test_role_unique_name(db_session):
    role1 = Role(name='testrole', description='First role')
    db_session.add(role1)
    db_session.commit()

    with pytest.raises(Exception):
        role2 = Role(name='testrole', description='Second role')
        db_session.add(role2)
        db_session.commit()


def test_role_as_dict(db_session):
    role = Role(name='testrole', description='Test role description')
    db_session.add(role)
    db_session.commit()

    role_dict = role.as_dict()
    assert role_dict['name'] == 'testrole'
    assert role_dict['description'] == 'Test role description'


def test_background_creation(db_session):
    background = Background(
        name='Test Background',
        description='A background for testing'
    )
    db_session.add(background)
    db_session.commit()

    assert background.id is not None
    assert background.name == 'Test Background'
    assert background.description == 'A background for testing'


def test_background_unique_name(db_session):
    background1 = Background(
        name='Test Background',
        description='First background'
    )
    db_session.add(background1)
    db_session.commit()

    with pytest.raises(Exception):
        background2 = Background(
            name='Test Background',
            description='Second background'
        )
        db_session.add(background2)
        db_session.commit()


def test_background_as_dict(db_session):
    background = Background(
        name='Test Background',
        description='A background for testing'
    )
    db_session.add(background)
    db_session.commit()

    background_dict = background.as_dict()
    assert background_dict['name'] == 'Test Background'
    assert background_dict['description'] == 'A background for testing'


def test_character_creation(db_session, test_user, test_background):
    character = Character(
        name='Test Character',
        description='Test description',
        backstory='Test backstory',
        strength=10,
        dexterity=12,
        constitution=14,
        intelligence=16,
        wisdom=15,
        charisma=8,
        owner=test_user,
        background=test_background
    )
    db_session.add(character)
    db_session.commit()

    assert character.id is not None
    assert character.name == 'Test Character'
    assert character.description == 'Test description'
    assert character.backstory == 'Test backstory'
    assert character.strength == 10
    assert character.dexterity == 12
    assert character.constitution == 14
    assert character.intelligence == 16
    assert character.wisdom == 15
    assert character.charisma == 8
    assert character.owner == test_user
    assert character.background == test_background


def test_character_as_dict(db_session, test_user, test_background):
    character = Character(
        name='Test Character',
        description='Test description',
        backstory='Test backstory',
        strength=10,
        dexterity=12,
        constitution=14,
        intelligence=16,
        wisdom=15,
        charisma=8,
        owner=test_user,
        background=test_background
    )
    db_session.add(character)
    db_session.commit()

    character_dict = character.as_dict()
    assert character_dict['name'] == 'Test Character'
    assert character_dict['description'] == 'Test description'
    assert character_dict['backstory'] == 'Test backstory'
    assert character_dict['strength'] == 10
    assert character_dict['dexterity'] == 12
    assert character_dict['constitution'] == 14
    assert character_dict['intelligence'] == 16
    assert character_dict['wisdom'] == 15
    assert character_dict['charisma'] == 8
    assert character_dict['owner_id'] == test_user.id
    assert character_dict['background_id'] == test_background.id


def test_character_required_fields(db_session, test_user, test_background):
    # Test zonder verplichte velden
    with pytest.raises(Exception):
        character = Character(
            name='Test Character',
            # ontbrekende verplichte velden
            owner=test_user,
            background=test_background
        )
        db_session.add(character)
        db_session.commit()


def test_character_owner_relationship(db_session, test_user, test_background):
    character = Character(
        name='Test Character',
        description='Test description',
        backstory='Test backstory',
        strength=10,
        dexterity=12,
        constitution=14,
        intelligence=16,
        wisdom=15,
        charisma=8,
        owner=test_user,
        background=test_background
    )
    db_session.add(character)
    db_session.commit()

    assert character in test_user.characters
    assert test_user == character.owner
