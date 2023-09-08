from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from random import choice
import pandas as pd
import sys

# Function to generate an initial meal plan
def generate_initial_meal_plan(df):
    days = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
    moments = ['midi', 'soir']
    
    meal_plan = {}
    
    for day in days:
        for moment in moments:
            if moment == 'midi':
                available_meals = df[df['moment'].str.contains('m')]['plat'].tolist()
            else:  # soir
                available_meals = df[df['moment'].str.contains('s')]['plat'].tolist()
            
            selected_meal = choice(available_meals)
            meal_plan[f"{day} {moment}"] = selected_meal
            
    return meal_plan

# Replace a meal in the meal plan
def replace_meal(day_moment, meal_plan, df):
    moment = day_moment.split()[1]
    if moment == 'midi':
        available_meals = df[df['moment'].str.contains('m')]['plat'].tolist()
    else:  # soir
        available_meals = df[df['moment'].str.contains('s')]['plat'].tolist()
        
    new_meal = choice(available_meals)
    meal_plan[day_moment] = new_meal
    return new_meal

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

def on_export_png_click(window):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(None, "Enregistrer le PNG", "", "PNG Files (*.png);;All Files (*)", options=options)
        if fileName:
            if not fileName.endswith('.png'):
                fileName += '.png'
            window.grab().save(fileName, 'PNG')

# Main function for the PyQt5 app
from PyQt5.QtWidgets import QVBoxLayout

from PyQt5.QtWidgets import QHBoxLayout

from PyQt5.QtWidgets import QHBoxLayout

from PyQt5.QtWidgets import QGridLayout

def main(df, meal_plan):
    app = QApplication(sys.argv)

    style_sheet = """
        QWidget {
            font: 12px;
        }
        QLabel#dayLabel {
            font-weight: bold;
        }
        QPushButton {
            background-color: #555555;
            color: white;
            border: none;
            padding: 5px;
            min-width: 60px;
            max-width: 60px;
        }
        QPushButton#quitButton {
            background-color: #FF5555;
        }
    """

    app.setStyleSheet(style_sheet)

    window = QWidget()
    window.setWindowTitle('Planificateur de repas')
    layout = QGridLayout()

    row = 0
    for day_moment, meal in meal_plan.items():
        day, moment = day_moment.split()
        day_label = QLabel(f"{day.upper()}")
        day_label.setObjectName("dayLabel")
        moment_label = QLabel(f"{moment}")
        meal_label = QLabel(f"{meal}")
        meal_label.setWordWrap(True)
        
        btn = QPushButton("Suivante")
        
        def on_click(day_moment=day_moment, meal_label=meal_label):
            new_meal = replace_meal(day_moment, meal_plan, df)
            meal_label.setText(f"{new_meal}")
        
        btn.clicked.connect(lambda checked, day_moment=day_moment, meal_label=meal_label: on_click(day_moment, meal_label))

        layout.addWidget(day_label, row, 0)
        layout.addWidget(moment_label, row, 1)
        layout.addWidget(meal_label, row, 2)
        layout.addWidget(btn, row, 3)

        row += 1

    png_btn = QPushButton("PNG")
    png_btn.clicked.connect(on_export_png_click)
    layout.addWidget(png_btn, row, 0, 1, 2)  # Spanning 2 columns

    quit_btn = QPushButton("Quitter")
    quit_btn.setObjectName("quitButton")
    quit_btn.clicked.connect(lambda: app.quit())
    layout.addWidget(quit_btn, row, 2, 1, 2)  # Spanning 2 columns

    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())

# Load CSV into DataFrame
df = pd.read_csv('bdd.csv', sep=';', encoding='utf8')

# Generate the initial meal plan
initial_meal_plan = generate_initial_meal_plan(df)

# Start the PyQt5 app
main(df, initial_meal_plan)