from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.core.window import Window
from calendar import monthrange

Window.clearcolor = (0.96, 0.96, 0.96, 1)  # Off-white background color
Window.size = (800, 600)  # Set the window size

class CalendarApp(App):
    def build(self):
        self.title = "Tracking"

        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=[10, 10, 10, 10])

        # Title
        title_label = Label(
            text='Tracking',
            font_size=30,
            size_hint=(1, None),
            height=60,
            color=(0, 0, 0, 1),  # Black color
            halign='center',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))
        main_layout.add_widget(title_label)

        # Options layout for year and month
        option_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, spacing=10)
        
        self.year_spinner = Spinner(
            text='2024',
            values=[str(year) for year in range(2024, 2030)],
            size_hint=(None, None),
            size=(100, 40),
            background_color=(0, 0, 0, 1),  # Black background color for Spinner
            color=(1, 1, 1, 1)  # White text color for Spinner
        )
        
        self.month_spinner = Spinner(
            text='July',
            values=['July', 'August', 'September', 'October', 'November', 'December'],
            size_hint=(None, None),
            size=(100, 40),
            background_color=(0, 0, 0, 1),  # Black background color for Spinner
            color=(1, 1, 1, 1)  # White text color for Spinner
        )
        
        self.year_spinner.bind(text=self.update_calendar)
        self.month_spinner.bind(text=self.update_calendar)

        option_layout.add_widget(self.year_spinner)
        option_layout.add_widget(self.month_spinner)

        main_layout.add_widget(option_layout)

        # Grid layout for days
        self.day_grid = GridLayout(cols=7, spacing=5, size_hint_y=None)
        main_layout.add_widget(self.day_grid)

        self.update_calendar()

        return main_layout

    def update_calendar(self, *args):
        self.day_grid.clear_widgets()
        
        year = int(self.year_spinner.text)
        month = list(self.month_spinner.values).index(self.month_spinner.text) + 7  # Adjust for July being the 7th month
        
        days_in_month = monthrange(year, month)[1]

        for day in range(1, days_in_month + 1):
            day_label = Label(text=str(day), size_hint=(None, None), size=(40, 40), halign='left', valign='top', color=(0, 0, 0, 1))
            day_label.bind(size=day_label.setter('text_size'))
            day_button = Button(size_hint=(None, None), size=(100, 100))
            day_button.add_widget(day_label)
            self.day_grid.add_widget(day_button)
        
        # Add empty buttons for alignment
        total_cells = 42  # 6 weeks x 7 days
        for _ in range(total_cells - days_in_month):
            self.day_grid.add_widget(Button(text='', size_hint=(None, None), size=(100, 100)))

if __name__ == '__main__':
    CalendarApp().run()
