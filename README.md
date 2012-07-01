# Humans.py

Add humans to your SQLAlchemy based web apps.

![Build status](https://secure.travis-ci.org/jeanphix/Humans.png)

## auth

The auth module provides factories for building basic auth models such as users, permissions and groups.

### `user_factory`

Creates the user model:

    User = user_factory(table_name='users')
    jeanphix = User('jeanphix', 'serafinjp@gmail.com', 'mypassword')
    assert jeanphix.check_password('mypassword')

### `group_factory`

Creates the group model:

    Group = group_factory(User, table_name='groups')
    admin = Group('admin')
    session.add(admin)
    jeanphix.groups.append(admin)


### `permission_factory`

Creates permission model.

Permissions can be linked to both user and / or group.

    Permission = permission_factory(table_name='permissions', user_class=User)
    create_user = Permission('create_user')
    session.add(create_user)
    jeanphix.permissions.append(create_user)
    assert 'create_user' in jeanphix.permissions_list
