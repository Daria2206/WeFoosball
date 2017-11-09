import flask
from . import db


class Team(db.Model):
    __tablename__ = 'teams'
    t_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    city = db.Column(db.String(50))
    users = db.relationship('User',backref='teams')

    def __repr__(self):
        return '<Team %r>' % self.team_name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self.t_id
    
    @staticmethod
    def id_to_name(num):
        name = Team.query.filter_by(team_id=num).first()
        return name.team_name

    @staticmethod
    def name_to_id(name):
        name = Team.query.filter_by(team_name=name).first()
        return name.t_id

    @staticmethod
    def display_teams_data():
        data = db.engine.execute(
            '''SELECT team_name, COUNT(CASE WHEN NULL THEN 0 ELSE users.email END), city
            FROM teams LEFT JOIN users
            ON teams.t_id = users.team_id
            GROUP BY team_name
            ORDER BY team_name COLLATE NOCASE ASC''')
        display_data = {}
        for element in data:
            display_data[str(element[0])] = element[1], element[2]
        return display_data


class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.t_id'), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.name
    
    def join_team(self, team_id):
        self.team_id = team_id

    def leave_team(self, team_id):
        self.team_id = None

    @staticmethod
    def current_user():
        return User.query.filter_by(
        email=flask.session['user_info']['emails']).first()

   
