from flask.cli import AppGroup
from .users import seed_users, undo_users
from .players import seed_players, undo_players
from .stages import seed_stages, undo_stages
from .background_images import seed_background_images, undo_background_images
from .monsters import seed_monsters, undo_monsters
from .monster_images import seed_monster_images, undo_monster_images
from .reviews import seed_reviews, undo_reviews
from .schedules import seed_schedules, undo_schedules
from .events import seed_events, undo_events
from .spell_books import seed_spell_books, undo_spell_books
from .spells import seed_spells, undo_spells
from .spell_images import seed_spell_images, undo_spell_images
from .potion_bags import seed_potion_bags, undo_potion_bags
from .potions import seed_potions, undo_potions
from .potion_images import seed_potion_images, undo_potion_images
from .sword_galleries import seed_sword_galleries, undo_sword_galleries

from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo
        # command, which will  truncate all tables prefixed with
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below
        undo_users()
        undo_players()
        undo_stages()
        undo_background_images()
        undo_monsters()
        undo_monster_images()
        undo_reviews()
        undo_schedules()
        undo_events()
        undo_spell_books()
        undo_spells()
        undo_spell_images()
        undo_potion_bags()
        undo_potions()
        undo_potion_images()
        undo_sword_galleries()
    seed_users()
    seed_players()
    seed_stages()
    seed_background_images()
    seed_monsters()
    seed_monster_images()
    seed_reviews()
    seed_schedules()
    seed_events()
    seed_spell_books()
    seed_spells()
    seed_spell_images()
    seed_potion_bags()
    seed_potions()
    seed_potion_images()
    seed_sword_galleries()
    # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_users()
    undo_players()
    undo_stages()
    undo_background_images()
    undo_monsters()
    undo_monster_images()
    undo_reviews()
    undo_schedules()
    undo_events()
    undo_spell_books()
    undo_spells()
    undo_spell_images()
    undo_potion_bags()
    undo_potions()
    undo_potion_images()
    undo_sword_galleries()
    # Add other undo functions here
