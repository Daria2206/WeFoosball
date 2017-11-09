"""
 We Foosball
    ~~~~~~
    A simple web application written with Flask + sqlite3 + SQLAlchemy.
    Photo credit: Thomas Serer on Unsplash (https://unsplash.com/photos/r-xKieMqL34)

"""
import os
from sqlite3 import dbapi2 as sqlite3
import flask
from . import main
from .. import db
from ..models import User, Team
from .forms import NewTeam
import json


@main.route('/', methods = ['GET', 'POST'])
def index():
    return flask.render_template('index.html')


@main.route('/register', methods = ['GET', 'POST'])
def register():
    return flask.render_template('register.html')


@main.route('/teams', methods = ['GET', 'POST'])
def teams():
    if 'credentials' not in flask.session:
      return flask.redirect('register')
    teams = Team.display_teams_data()
    user_info = User.query.group_by(User.team_id).all()
    return flask.render_template(
        'teams.html', teams=teams, user_info=user_info)


@main.route('/teams/<name>')
def team(name):
    if 'credentials' not in flask.session:
      return flask.redirect('register')
    try:
        eligibile_member = User.current_user()
        team_data = Team.query.filter_by(team_name=name).first()
        members = User.query.filter_by(team_id=team_data.t_id).all()
        if len(members) == 0:
            db.session.delete(team_data)
            db.session.commit()
            return flask.render_template('deleted.html', name=name)
        return flask.render_template(
            'team.html', name=name, team=team_data, members=members,
            number = len(members), eligibile=eligibile_member)
    except:
        return flask.redirect('teams')


@main.route('/teams/<name>/join')
def jointeam(name):
    if 'credentials' not in flask.session:
      return flask.redirect('register')
    current_user = User.current_user()
    team_id = Team.name_to_id(name)
    members = User.query.filter_by(team_id=team_id).all()
    if (current_user.team_id == None) and (len(members)) < 4:
        current_user.join_team(team_id)
    return flask.redirect('teams/' + name)


@main.route('/teams/<name>/leave')
def leaveteam(name):
    if 'credentials' not in flask.session:
      return flask.redirect('register')
    current_user = User.current_user()
    team_id = Team.name_to_id(name)
    if current_user.team_id == team_id:
        current_user.leave_team(team_id)
    return flask.redirect('teams/' + name)


@main.route('/teams/newteam', methods = ['GET', 'POST'])
def newteam():
    if 'credentials' not in flask.session:
      return flask.redirect('register')
    # Check if a user belongs to any team already.
    eligibile_member = User.current_user()
    # Allow a user to create a new team if he/she doesn't belong to any team.
    if eligibile_member.team_id == None:
        name, city = None, None
        form = NewTeam()
        if form.validate_on_submit():
            # Check whether selected team name is already taken.
            check_name_av = Team.query.filter_by(
                team_name=form.name.data).first()
            if check_name_av != None:
                flask.flash("Seems like you selected a team name already in use.")
                return flask.render_template(
                    'newteam.html', form=form, name=name, city=city)
            else:
                # Add a new team and add it's creator as a first member.
                new_team = Team(team_name=form.name.data, city=form.city.data)
                id_of_new_team = new_team.save_to_db()
                eligibile_member.join_team(id_of_new_team)
                return flask.redirect(flask.url_for('main.teams'))
        return flask.render_template(
            'newteam.html', form=form, name=name, city=city)
    else:
        teamname = Team.query.filter_by(t_id=eligibile_member.team_id).first()
        return flask.render_template('double.html', teamname=teamname.team_name)
