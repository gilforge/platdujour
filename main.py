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

def generate_pdf(meal_plan, filename):
    pdf = SimpleDocTemplate("meal_plan.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    data = [["Jour", "Moment", "Plat"]]
    for day_moment, meal in meal_plan.items():
        day, moment = day_moment.split()
        data.append([day, moment, meal])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    pdf.build(elements)

# Main function for the PyQt5 app
def main(df, meal_plan):
    app = QApplication(sys.argv)

    style_sheet = """
        QWidget {
            font: 12px;
        }
        QPushButton {
            background-color: #555555;
            color: white;
            border: none;
            padding: 10px;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #666666;
        }
        QPushButton:pressed {
            background-color: #777777;
        }
        QPushButton#quitButton {
            background-color: #FF5555;
        }
        QPushButton#quitButton:hover {
            background-color: #FF6666;
        }
        QPushButton#quitButton:pressed {
            background-color: #FF7777;
        }
    """

    app.setStyleSheet(style_sheet)

    window = QWidget()
    window.setWindowTitle('Planificateur de repas')
    layout = QVBoxLayout()

    for day_moment, meal in meal_plan.items():
        label = QLabel(f"{day_moment}: {meal}")
        btn = QPushButton("Refuser")
        
        def on_click(day_moment=day_moment, label=label):
            new_meal = replace_meal(day_moment, meal_plan, df)
            label.setText(f"{day_moment}: {new_meal}")
        
        btn.clicked.connect(lambda checked, day_moment=day_moment, label=label: on_click(day_moment, label))
        
        layout.addWidget(label)
        layout.addWidget(btn)
    
    final_btn = QPushButton("Exporter en PDF")

    def on_final_click():
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(None, "Enregistrer le PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if fileName:
            if not fileName.endswith('.pdf'):
                fileName += '.pdf'
            generate_pdf(meal_plan, fileName)

    final_btn.clicked.connect(on_final_click)
    layout.addWidget(final_btn)
    layout.addWidget(final_btn)

    quit_btn = QPushButton("Quitter")
    quit_btn.setObjectName("quitButton")

    def quit_app():
        app.quit()

    quit_btn.clicked.connect(quit_app)
    layout.addWidget(quit_btn)

    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())

# Load CSV into DataFrame
df = pd.read_csv('bdd.csv', encoding='utf8')

# Generate the initial meal plan
initial_meal_plan = generate_initial_meal_plan(df)

# Start the PyQt5 app
main(df, initial_meal_plan)
