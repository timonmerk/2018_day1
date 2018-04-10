import auth
import pathlib
import pickle
import tempfile

# global pathname thingies
PWDB_FLNAME = pathlib.Path('pwdb.pkl')
pwdb_path = tempfile.gettempdir() / PWDB_FLNAME

# user data that is correct
db_right = list()
db_right.append(('daniel', 'vargas', '=2od%]1*9Q', 9966))
db_right.append(('nadine', 'heere', 'j=U]V.n`l\\', 10976))
db_right.append(('mayar', 'ali', 'PJM0~RD*|&', 6986))
db_right.append(('marc', 'vischer', 'nL*E~T&az1', 13112))
db_right.append(('pooja', 'subramaniam', '%9<:%fSN$}', 18453))


# user data that is incorrect
db_wrong = list()
db_wrong.append(('joel', 'afreth', 'c:d{<Am),Z', 11060)) # should be 11069


# databases in the format that is used by auth
db_dict_right = dict()
for user in db_right:
    db_dict_right[user[0]] = (user[3], user[2])

db_dict_wrong = dict()
for user in db_wrong:
    db_dict_wrong[user[0]] = (user[3], user[2])

## start test functions

def test_get_salt():
    salts = [auth.get_salt() for i in range(100)]
    assert all([len(salt) == 10 for salt in salts]), 'Some are not 10 characters long'
    assert len(set(salts)) == len(salts), 'Tested 100 salts are not unique'


def test_pwhash():
    for user in db_right:
        assert auth.pwhash(user[1], user[2]) == user[3]

    for user in db_wrong:
        assert auth.pwhash(user[1], user[2]) != user[3]


def test_authenticate():
    for user in db_right:
        assert auth.authenticate(user[0], user[1], db_dict_right)

    for user in db_wrong:
        assert not auth.authenticate(user[0], user[1], db_dict_wrong)


def test_io():
    with open(pwdb_path, 'wb+') as right_file:
        auth.write_pwdb(db_dict_right, right_file)

    with open(pwdb_path, 'rb+') as right_file:
        assert auth.read_pwdb(right_file) == db_dict_right


def test_add_user():
    user = ('evert', 'de man', '6v"&?5UXx-', 10173)

    with open(pwdb_path, 'wb+') as right_file:
        auth.add_user(user[0], user[1], user[2], db_dict_right, right_file)

    assert db_dict_right[user[0]] == (user[3], user[2]), 'Dict is not right in memory'

    with open(pwdb_path, 'rb+') as right_file:
        assert auth.read_pwdb(right_file) == db_dict_right


def test_add_existing_user():
    # get an existing user from our database
    user = db_right[-1]

    flag = False
    with open(pwdb_path, 'wb+') as right_file:
        try:
            auth.add_user(user[0], user[1], user[2], db_dict_right, right_file)
        except:
            flag = True

    assert flag
