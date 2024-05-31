import streamlit as st
import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import requests

# '''
# # TaxiFareModel front
# '''

st.markdown('''
# New York Taxi Fare
## By Annabel C and forked from LeWagon
''')

# '''
# ## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

# 1. Let's ask for:
# - date and time
# - pickup longitude
# - pickup latitude
# - dropoff longitude
# - dropoff latitude
# - passenger count
# '''
# col1, col2, col3, col4= st.columns(4)

# with col1:
#     date = st.date_input("What day is it?", datetime.date(year, month, day))
#     st.write('The date is:', date)
#     time = st.time_input('What time do you want to travel?:', datetime.time(hour, minute))
#     st.write('Your travel time is set for:', time)
# with col2:
#     pickup = st.text_input('Number', 'Street', 'Postcode', 'Area')
# with col3:
#     dropoff = st.text_input('Number', 'Street', 'Postcode', 'Area')
# with col4:
#     passengers = st.number_input('How many passengers?')

# Function to geocode an address
def geocode_address(address):
    geolocator = Nominatim(user_agent="taxi-fare")
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None
    # except (GeocoderTimedOut, GeocoderServiceError) as e:
    #     st.error(f"Geocoding error: {e}")
    #     return None

def get_prediction(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count):
    url = 'https://taxifare.lewagon.ai/predict'
    params = {
        'pickup_datetime': pickup_datetime,
        'pickup_longitude': pickup_longitude,
        'pickup_latitude': pickup_latitude,
        'dropoff_longitude': dropoff_longitude,
        'dropoff_latitude': dropoff_latitude,
        'passenger_count': passenger_count
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

# Streamlit application
def main():
    st.title("Ride Parameters Input")

    st.write("Please enter the details of your ride:")

    # Create columns for input fields
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Date and time input
        date = st.date_input("What day is it?", datetime.date.today())
        st.write('The date is:', date)
        time = st.time_input('What time do you want to travel?:')
        st.write('Your travel time is set for:', time)

    with col2:
        # Pickup address input
        pickup = st.text_input('Pickup Address', 'Number, Street, City/Area, State, Postcode, Country')
    
    with col3:
        # Dropoff address input
        dropoff = st.text_input('Dropoff Address', 'Number, Street, City/Area, State, Postcode, Country')
    
    with col4:
        # Passenger count input
        passengers = st.number_input('How many passengers?', min_value=1, step=1)

    if st.button("Get Coordinates and Predict Fare"):
        if pickup and dropoff:
            pickup_coords = geocode_address(pickup)
            dropoff_coords = geocode_address(dropoff)

            if pickup_coords and dropoff_coords:
                st.write(f"Pickup Coordinates: {pickup_coords}")
                st.write(f"Dropoff Coordinates: {dropoff_coords}")

                pickup_longitude, pickup_latitude = pickup_coords
                dropoff_longitude, dropoff_latitude = dropoff_coords
            
            # Combine date and time into a single datetime string
            pickup_datetime = f"{date} {time}"

                # Call the API to get the prediction
            prediction = get_prediction(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passengers)

            if prediction:
                fare = prediction.get('fare', 'N/A')
                st.success(f"Estimated Fare: ${fare:.2f}")
            else:
                st.error("Failed to get a prediction from the API.")
        else:
            st.error("Could not find coordinates for the provided addresses.")
    else:
        st.error("Please enter both pickup and dropoff addresses.")

        #     if prediction:
        #         fare = prediction.get('fare', 'N/A')
        #         st.success(f"Estimated Fare: ${fare:.2f}")
        #     else:
        #         st.error("Failed to get a prediction from the API.")
            
        #     if pickup_coords:
        #         st.write(f"Pickup Coordinates: {pickup_coords}")
        #     else:
        #         st.error("Could not find coordinates for the pickup address.")

        #     if dropoff_coords:
        #         st.write(f"Dropoff Coordinates: {dropoff_coords}")
        #     else:
        #         st.error("Could not find coordinates for the dropoff address.")
        # else:
        #     st.error("Please enter both pickup and dropoff addresses.")

if __name__ == "__main__":
    main()




# '''
# ## Once we have these, let's call our API in order to retrieve a prediction

# See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

# 🤔 How could we call our API ? Off course... The `requests` package 💡
# '''

# url = 'https://taxifare.lewagon.ai/predict'

# if url == 'https://taxifare.lewagon.ai/predict':

#     st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''

# 2. Let's build a dictionary containing the parameters for our API...

# 3. Let's call our API using the `requests` package...

# 4. Let's retrieve the prediction from the **JSON** returned by the API...

# ## Finally, we can display the prediction to the user
# '''