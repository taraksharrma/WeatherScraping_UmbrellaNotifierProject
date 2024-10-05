import schedule
import smtplib
import requests
from bs4 import BeautifulSoup
import time

def umbrellaReminder():
    city = "Chandigarh"
    
    # Step 1: Fetch weather data
    print(f"Fetching weather data for {city}...")
    
    try:
        url = "https://www.google.com/search?q=" + "weather " + city
        html = requests.get(url).content
        
        # Parse the HTML
        soup = BeautifulSoup(html, 'html.parser')
        temperature = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        time_sky = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
        
        # Format the data
        sky = time_sky.split('\n')[1]
        print(f"Weather in {city}: {sky}, Temperature: {temperature}")
        
    except Exception as e:
        print(f"Failed to fetch weather data: {e}")
        return  # Exit the function if fetching weather fails
    
    # Step 2: Send an email if the weather indicates rain or clouds
    if sky in ["Rainy", "Rain And Snow", "Showers", "Haze", "Cloudy"]:
        try:
            smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_object.starttls()
            
            # Login using the correct app password (not your regular Gmail password)
            smtp_object.login("chikashikame@gmail.com", "mnaz ixcv qnuu kfjo")
            print("SMTP login successful.")
            
            # Prepare email
            subject = "Umbrella Reminder"
            body = f"Take an umbrella before leaving the house. " \
                   f"Weather condition for today is {sky} and temperature is " \
                   f"{temperature} in {city}."
                   
            msg = f"Subject: {subject}\n\n{body}\n\nRegards,\nGeeksforGeeks".encode('utf-8')
            
            # Send email
            smtp_object.sendmail("chikashikame@gmail.com", "jaitaraknand@gmail.com", msg)
            print("Email Sent!")
            
        except Exception as e:
            print(f"Failed to send email: {e}")
        
        finally:
            smtp_object.quit()
            print("SMTP session closed.")
    else:
        print(f"No umbrella needed today. Weather: {sky}")

# For testing purposes, run the reminder every minute (change to daily after testing)
schedule.every(1).minutes.do(umbrellaReminder)  # For testing

# Uncomment the line below and comment the one above for production:
# schedule.every().day.at("10:10").do(umbrellaReminder)

# Run the scheduler
print("Starting the scheduler...")
while True:
    schedule.run_pending()
    time.sleep(1)  # Sleep to avoid busy-waiting
