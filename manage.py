from flask.cli import FlaskGroup

from project import create_app, db
from project.api.artists.models import Artist

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('seed_db')
def seed_db():
    db.session.add(Artist(
        name='Jonny Cash',
        city='New York',
        state='NY',
        phone='674-674-674',
        genres='Folk',
        image_link=None,
        facebook_link=None))
    
    db.session.add(Artist(
        name='Bobby Blue Bland',
        city='San Francisco',
        state='CA',
        phone='216-216-216',
        genres='Blues',
        image_link=None,
        facebook_link=None))
    
    db.session.commit()

    

if __name__ == '__main__':
    cli()