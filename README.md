# 🌦️ Village Weather Assistant

A simple Streamlit application that fetches current weather for an Indian village or town using OpenWeather and reads the report aloud using gTTS.

## Features
- Search current weather by village/town name
- Temperature in Celsius, humidity, weather description, and wind speed
- English text-to-speech announcement
- API key kept in Streamlit Secrets, outside the source code

## Run locally
1. Install Python.
2. Open a terminal in this project folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create `.streamlit/secrets.toml` and add:
   ```toml
   OPENWEATHER_API_KEY = "YOUR_ACTUAL_OPENWEATHER_API_KEY"
   ```
5. Start the app:
   ```bash
   streamlit run app.py
   ```

Do not commit `.streamlit/secrets.toml`. It is excluded by `.gitignore`.

## Deploy on Streamlit Community Cloud
1. Push this repository to GitHub.
2. Sign in at https://share.streamlit.io/ and create an app.
3. Choose this repository, branch `main`, and main file `app.py`.
4. In the app's Advanced settings / Secrets, add:
   ```toml
   OPENWEATHER_API_KEY = "YOUR_ACTUAL_OPENWEATHER_API_KEY"
   ```
5. Deploy.

## Security
Never place your real API key in `app.py`, `README.md`, or any committed file. If a key was exposed publicly, rotate it in your OpenWeather account.
