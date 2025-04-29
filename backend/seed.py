# This script seeds the database with standard exercises and routines.
from app import app, db
from models import Exercises, Routines
import logging

def seed_exercises():
    standard_exercises = [
        Exercises(name="Squat", muscle_group="Legs"),
        Exercises(name="Bench Press", muscle_group="Chest"),
        Exercises(name="Deadlift", muscle_group="Back"),
        Exercises(name="Overhead Press", muscle_group="Shoulders"),
        Exercises(name="Barbell Row", muscle_group="Back"),
        Exercises(name="Pull-Up", muscle_group="Back"),
        Exercises(name="Lunge", muscle_group="Legs"),
        Exercises(name="Dumbbell Curl", muscle_group="Arms"),
    ]
    db.session.bulk_save_objects(standard_exercises)
    print(f"✅ Seeded {len(standard_exercises)} standard exercises.")

def seed_routines():
    standard_routines = [
        Routines(name="Starting Strength"),
        Routines(name="Push Pull Legs"),
        Routines(name="Upper Lower Split"),
        Routines(name="Full Body Routine"),
    ]
    db.session.bulk_save_objects(standard_routines)
    print(f"✅ Seeded {len(standard_routines)} standard routines.")

with app.app_context():
    try:
        if not Exercises.query.first():
            seed_exercises()
        else:
            logging.info("⚡ Exercises already seeded.")

        if not Routines.query.first():
            seed_routines()
        else:
            logging.info("⚡ Routines already seeded.")

        db.session.commit()
        logging.info("🌱 Seeding complete!")
    except Exception as e:
        logging.error(f"❌ Error during seeding: {e}")
        db.session.rollback()
