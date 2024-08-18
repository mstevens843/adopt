from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from models import db, Pet
from forms import AddPetForm, EditPetForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Enable the debug toolbar
toolbar = DebugToolbarExtension(app)


@app.route('/')
def list_pets():
    """Homepage: show all pets available for adoption."""
    pets = Pet.query.all()
    return render_template('index.html', pets=pets)


@app.route('/add', methods=['GET', 'POST'])
def show_add_pet_form():
    """Show form to add a new pet, handle form submission."""
    form = AddPetForm()

    # Validate form submission
    if form.validate_on_submit():
        # Create a new Pet object using form data
        new_pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data,
            age=form.age.data,
            notes=form.notes.data,
        )
        
        # Add new pet to the database
        db.session.add(new_pet)
        db.session.commit()

        # Flash success message and redirect to homepage
        flash(f"Added {new_pet.name} the {new_pet.species}!")
        return redirect('/')
    
    # If the form is not valid, re-render the form
    return render_template('add_pet.html', form=form)


@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def show_and_edit_pet(pet_id):
    """Show pet details and allow editing the pet's information."""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    # Validate form submission
    if form.validate_on_submit():
        # Update pet details
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        # Commit changes to the database
        db.session.commit()

        # Flash success message and redirect to the same page
        flash(f"{pet.name} has been updated.")
        return redirect(f'/{pet_id}')

    # If the form is not valid, re-render the form
    return render_template('pet_detail.html', pet=pet, form=form)


if __name__ == "__main__":
    app.run(debug=True)
