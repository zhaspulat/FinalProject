from app import create_app
from models import Mission

app = create_app('config')
test_app = create_app('test_config')

missions = [
    Mission(name='writer'),
    Mission(name='star'),
    Mission(name='director')
]

missions_test = [
    Mission(name='writer'),
    Mission(name='star'),
    Mission(name='director')
]

with app.app_context():
    for mission in missions:
        mission.insert()

with test_app.app_context():
    for mission in missions_test:
        mission.insert()
