import requests
import streamlit as st
from gtts import gTTS
from io import BytesIO

st.set_page_config(
    page_title="Village Weather Assistant",
    page_icon="🌦️",
    layout="centered"
)

st.title("🌦️ Village Weather Assistant")
st.write("Get current weather information for your village and listen to a voice announcement.")

def get_weather(village):
    api_key = st.secrets.get("OPENWEATHER_API_KEY", "")

    if not api_key:
        return None, "API key is missing. Please configure Streamlit Secrets."

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": f"{village},IN",
                "appid": api_key,
                "units": "metric"
            },
            timeout=15
        )

        if response.status_code == 404:
            return None, "Village not found. Please check the spelling."

        if response.status_code == 401:
            return None, "Invalid API key or the key is not active yet."

        response.raise_for_status()
        data = response.json()

        weather_report = (
            f"Weather report for {data['name']}. "
            f"Description: {data['weather'][0]['description']}. "
            f"Temperature: {data['main']['temp']} degrees Celsius. "
            f"Humidity: {data['main']['humidity']} percent. "
            f"Wind speed: {data.get('wind', {}).get('speed', 0)} meters per second."
        )

        return data, weather_report

    except requests.exceptions.Timeout:
        return None, "Request timed out. Please try again."

    except requests.exceptions.RequestException:
        return None, "Unable to fetch weather. Please check your internet connection."

def text_to_speech(weather_report):
    audio = BytesIO()
    speech = gTTS(text=weather_report, lang="en")
    speech.write_to_fp(audio)
    audio.seek(0)
    return audio

village = st.text_input(
    "🏡 Enter village or town name",
    placeholder="Example: Tadepalligudem"
)

if st.button("🌤️ Get Weather", type="primary", use_container_width=True):

    if not village.strip():
        st.warning("Please enter a village name.")

    else:
        with st.spinner("Fetching current weather..."):
            data, result = get_weather(village.strip())

        if data is None:
            st.error(result)

        else:
            st.success(f"Weather information for {data['name']}")

            col1, col2 = st.columns(2)

            col1.metric(
                "🌡️ Temperature",
                f"{data['main']['temp']} °C"
            )

            col2.metric(
                "💧 Humidity",
                f"{data['main']['humidity']}%"
            )

            st.write(
                "☁️ **Description:**",
                data["weather"][0]["description"].title()
            )

            st.write(
                "💨 **Wind Speed:**",
                f"{data.get('wind', {}).get('speed', 0)} meters/sec"
            )

            st.subheader("🔊 Voice Announcement")

            try:
                audio = text_to_speech(result)
                st.audio(audio, format="audio/mp3")

            except Exception:
                st.warning(
                    "Weather retrieved successfully, but audio generation failed."
                )

            with st.expander("View complete weather report"):
                st.write(result)

