from faker import Faker
from models import db, Hero, Power, HeroPower
from flask import Flask
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create an application context
with app.app_context():
    fake = Faker()

    # Ensure we have some powers available
    if Power.query.count() == 0:
        default_powers = [
            Power(name="Super Strength", description="Gives incredible physical strength."),
            Power(name="Teleportation", description="Can instantly move from one place to another."),
            Power(name="Invisibility", description="Can become invisible at will.")
        ]
        db.session.add_all(default_powers)
        db.session.commit()

    for _ in range(10):  # Generate 10 heroes
        hero = Hero(name=fake.unique.first_name(), super_name=fake.unique.first_name())
        db.session.add(hero)
        for _ in range(fake.random_int(1, 3)):
            power = Power.query.order_by(func.random()).first()  # Get a random power
            strength = fake.random_element(["Strong", "Weak", "Average"])
            hero_power = HeroPower(hero=hero, power=power, strength=strength)
            db.session.add(hero_power)

    db.session.commit()
    print(" seeding complete!")