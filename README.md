# Humans.py

Add humans to yor SQLAlchemy based web apps.

## auth

The auth module provides factories for building basic auth models such as users, permissions and groups.

### `user_factory`

Creates the user model:

    User = user_factory(table_name='users')
    jeanphix = User('jeanphix', 'serafinjp@gmail.com', 'mypassword')
    assert jeanphix.check_password('mypassword')

### `permission_factory`

Creates permission model.
Permissions can be linked to both user and / or group.
