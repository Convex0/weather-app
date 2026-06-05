import sys,requests
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QLineEdit,QPushButton
                             ,QVBoxLayout,QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QPixmap
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("4d7d5e43a92e30553f22f658150576ba")

class Weatherapp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather app")
        self.setWindowIcon(QIcon("images.jpg"))
        self.input = QLineEdit(self)
        self.button = QPushButton(self, text="Submit")
        self.city_label=QLabel("Enter the city name:",self)
        self.temperature_label=QLabel(self)
        self.emoji_label=QLabel(self)
        self.weather_label=QLabel(self)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.city_label)
        main_layout.addWidget(self.input)
        main_layout.addWidget(self.button)
    
        weather_layout = QVBoxLayout()
        weather_layout.addWidget(self.temperature_label)
        weather_layout.addWidget(self.emoji_label)
        weather_layout.addWidget(self.weather_label)

        main_layout.addLayout(weather_layout)
        self.setLayout(main_layout)

        self.input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.weather_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)

        self.input.setObjectName("input")
        self.button.setObjectName("button")
        self.city_label.setObjectName("city_label")
        self.emoji_label.setObjectName("emoji_label")
        self.weather_label.setObjectName("weather_label")
        self.temperature_label.setObjectName("temperature_label")

        self.setStyleSheet("""
            QWidget {
                background-color: #E0F7FA;
                color: #004D40;
            }
            QLabel, QPushButton {
                font-family: Verdana;
            }

            QLineEdit#input {
                font-size: 30px;
                border: 2px solid #00BCD4;
                padding: 4px;
                border-radius: 5px;
            }
            QLineEdit#input:hover {
                border: 2px solid #007C91;
            }
            QPushButton#button {
                font-size: 22px;
                background-color: #00ACC1;
                border: none;
                padding: 6px 12px;
                color: white;
                border-radius: 5px;
            }
            QPushButton#button:hover {
                background-color: #00838F;
            }
            QLabel#city_label {
                font-size: 30px;
            }
            QLabel#temperature_label {
                font-size: 70px;
            }
            QLabel#weather_label {
                font-size: 20px;
            }
            QLabel#emoji_label {
                font-size: 80px;
                font-family: Segoe UI Emoji;
            }
        """)

        self.button.clicked.connect(self.get_weather_info)

    def get_weather_info(self):
        api_key = os.getenv("API_KEY")
        city_name=self.input.text().strip().lower()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
        response = requests.get(url)
        try:
            response.raise_for_status()
            weather_data = response.json()
            if weather_data["cod"]==200:
                weather_data = response.json()
                self.display_weather(weather_data)
        except requests.exceptions.HTTPError as httperror:
            match response.status_code:
                case 400:
                    self.display_error("Bad Requests\nPlease check your input❌")
                case 401:
                    self.display_error("Unauthorized\nInvalid API key❌")
                case 403:
                    self.display_error("Forbidden\nAccess ia denied❌")
                case 404:
                    self.display_error("Not Found\nCity not found❌")
                case 500:
                    self.display_error("Internal Server Error\nPlease try again later❌")
                case 502:
                    self.display_error("Bad Getway\nInvalid response from the server❌")
                case 503:
                    self.display_error("Server Unavailable\nServer is down❌")
                case 504:
                    self.display_error("Getaway Timeout\nNo response from the server❌")
                case _:
                    self.display_error(f"HTTPErorr has occurred \n{httperror}❌")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nCheck your internet connection❌")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects\nCheck your URL❌")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\nThe request timed out❌")

        except requests.exceptions.RequestException as re_error:
            self.display_error(f"Request Error\n{re_error}❌")

    def display_error(self,message):
        self.temperature_label.setText(message)
        self.temperature_label.setStyleSheet("font-size:30px;")

    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size:70px;")        

        temp_k=data['main']['temp']
        temp_c=temp_k- 273.15
        self.temperature_label.setText(f"{int(temp_c)}°C")

        self.emoji_label.setStyleSheet("font-size:80px;"\
        "font-family:Segoe UI Emoji;")        
        icon = data["weather"][0]["icon"]
        emoji = self.icon_to_emoji(icon)
        self.emoji_label.setText(emoji)

        self.weather_label.setStyleSheet("font-size:20px;")
        weather=data["weather"][0]["description"]
        self.weather_label.setText(weather)     

    @staticmethod
    def icon_to_emoji(icon_code):
        icon_map = {
            "01d": "☀️", "01n": "🌕",
            "02d": "🌤️", "02n": "🌤️",
            "03d": "☁️", "03n": "☁️",
            "04d": "🌥️", "04n": "🌥️",
            "09d": "🌧️", "09n": "🌧️",
            "10d": "🌦️", "10n": "🌧️",
            "11d": "⛈️", "11n": "⛈️",
            "13d": "🌨️", "13n": "🌨️",
            "50d": "🌫️", "50n": "🌫️",
        }
        return icon_map.get(icon_code,"❓")  


if __name__=="__main__":
    app = QApplication(sys.argv)
    weatherapp = Weatherapp()
    weatherapp.show()
    sys.exit(app.exec_())
