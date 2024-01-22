# Steven Dang
# ENAE380 | Section 0101
# Final Project - Live Flight Tracking
# ------------------------------------------------------------------------------------------------------------------
# LIBRARIES
# These libraries are for webscrapping purposes
import requests
from bs4 import BeautifulSoup
# For auto-refreshing
import time
# These libraries are for layout and text format purposes
import os
from rich import print
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
console = Console()
# ------------------------------------------------------------------------------------------------------------------
# Verify if flight information is avaliable
def verify_flight(flight_number_input, date_input):
  # Takes the flight number and break it into airline code and flight number
  flight_number_arr = [*flight_number_input]
  flight_number_str = ''
  airline_code_arr = []
  airline_code_str = ''
  for i in range(2):
      airline_code_arr.append(flight_number_arr[0])
      flight_number_arr.pop(0)
  airline_code = airline_code_str.join(airline_code_arr)
  flight_number = flight_number_str.join(flight_number_arr)

  # Takes the date and breaks up to its respective month, day, and year
  date_arr = [*date_input]
  month = str(date_arr[0] + date_arr[1])
  day = str(date_arr[3] + date_arr[4])
  year = '20' + str(date_arr[8] + date_arr[9])

  # Gets the URL of the flight
  url = 'https://www.flightstats.com/v2/flight-tracker/' + str(airline_code) + '/' + str(flight_number) + '?year=' + str(year) + '&month=' + str(month) + '&date=' + str(day)

  # Access the page and obtain the HTML code that will be used for webscraping
  page = requests.get(url)
  flight_info = BeautifulSoup(page.text, 'html.parser')

  results = flight_info.find(id='__next')

  # Flight Status
  # If the flight is ontime
  flight_status_ontime = results.find_all('div', class_='text-helper__TextHelper-sc-8bko4a-0 iicbYn')
  # If the flight is delayed
  flight_status_delayed = results.find_all('div',class_='text-helper__TextHelper-sc-8bko4a-0 hYcdHE')

  if flight_status_ontime == [] and flight_status_delayed == []:
      return "Error"
  else:
      return "Success"
# ------------------------------------------------------------------------------------------------------------------  
# Function to grab basic flight information
def basic_flight_info(flight_number_input, date_input):
    # Takes the flight number and break it into airline code and flight number
    flight_number_arr = [*flight_number_input]
    flight_number_str = ''
    airline_code_arr = []
    airline_code_str = ''
    for i in range(2):
        airline_code_arr.append(flight_number_arr[0])
        flight_number_arr.pop(0)
    airline_code = airline_code_str.join(airline_code_arr)
    flight_number = flight_number_str.join(flight_number_arr)

    # Takes the date and breaks up to its respective month, day, and year
    date_arr = [*date_input]
    month = str(date_arr[0] + date_arr[1])
    day = str(date_arr[3] + date_arr[4])
    year = '20' + str(date_arr[8] + date_arr[9])

    # Gets the URL of the flight
    url = 'https://www.flightstats.com/v2/flight-tracker/' + str(airline_code) + '/' + str(flight_number) + '?year=' + str(year) + '&month=' + str(month) + '&date=' + str(day)

    # Access the page and obtain the HTML code that will be used for webscraping
    page = requests.get(url)
    flight_info = BeautifulSoup(page.text, 'html.parser')

    results = flight_info.find(id='__next')

    # Flight Status
    # If the flight is ontime
    flight_status_ontime = results.find_all('div', class_='text-helper__TextHelper-sc-8bko4a-0 iicbYn')
    # If the flight is delayed
    flight_status_delayed = results.find_all('div',class_='text-helper__TextHelper-sc-8bko4a-0 hYcdHE')

    if flight_status_ontime == []:
        flight_status = flight_status_delayed[0].text
        color = 'yellow'
    else:
        flight_status = flight_status_ontime[0].text
        color = 'green'

    # Departure + Arrival Location & Airport
    location = results.find_all('div', class_='text-helper__TextHelper-sc-8bko4a-0 efwouT')
    airport = results.find_all('div', class_='text-helper__TextHelper-sc-8bko4a-0 cHdMkI')

    # Departure + Arrival Date & Times (Scheduled & Actual) | Terminal and Gate Information
    time = results.find_all('div', class_='text-helper__TextHelper-sc-8bko4a-0 kbHzdx')
    date = results.find_all('div', class_='text-helper__TextHelper-sc-8bko4a-0 cPBDDe')

    # Gates
    gates = results.find_all('div', class_="ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx")
    # TO confirm if there's information on baggage
    if len(gates) == 5:
      baggage = gates[4].text 
    else:
      baggage = "N/A"
    # Returns flight information to the main function as an array
    #      |flight status|                        departing info                        |                        arrival info                         |          dates            |                terminal and gates                                   |                                     
    #            0                1                2              3             4               5                 6              7             8             9            10            11            12             13           14             15       16
    return flight_status, location[0].text, airport[0].text, time[0].text, time[1].text, location[1].text, airport[1].text, time[2].text, time[3].text, date[0].text, date[1].text, gates[0].text, gates[1].text, gates[2].text, gates[3].text, baggage, color
# ------------------------------------------------------------------------------------------------------------------
# Checks to see if tracking is available yet
def verify_tracking(flight_number_input, date_input):
    # Takes the flight number and break it into airline code and flight number
    flight_number_arr = [*flight_number_input]
    flight_number_str = ''
    airline_code_arr = []
    airline_code_str = ''
    for i in range(2):
        airline_code_arr.append(flight_number_arr[0])
        flight_number_arr.pop(0)
    airline_code = airline_code_str.join(airline_code_arr)
    flight_number = flight_number_str.join(flight_number_arr)

    # Takes the date and breaks up to its respective month, day, and year
    date_arr = [*date_input]
    month = str(date_arr[0] + date_arr[1])
    day = str(date_arr[3] + date_arr[4])
    year = '20' + str(date_arr[8] + date_arr[9])

    # Gets the URL of the flight
    url = 'https://www.flightstats.com/v2/flight-tracker/' + str(airline_code) + '/' + str(flight_number) + '?year=' + str(year) + '&month=' + str(month) + '&date=' + str(day)

    # Access the page and obtain the HTML code that will be used for webscraping
    page = requests.get(url)
    flight_info = BeautifulSoup(page.text, 'html.parser')

    results = flight_info.find(id='__next')

    # Flight Status
    # If the flight is ontime
    flight_status_ontime = results.find_all('div', class_='text-helper__TextHelper-sc-8bko4a-0 iicbYn')
    # If the flight is delayed
    flight_status_delayed = results.find_all('div',class_='text-helper__TextHelper-sc-8bko4a-0 hYcdHE')

    if flight_status_ontime == []:
        flight_status = flight_status_delayed[0].text
    else:
        flight_status = flight_status_ontime[0].text

    speed = results.find_all('span', class_='bearing__HeadingValue-sc-2vsxtq-2 kLgywj')

    if speed == []:
       return "UNAVAILABLE"
    else:
       return "AVAILABLE"

# ------------------------------------------------------------------------------------------------------------------
# Function to grab active flight information such as time elapsed, distance travelled, etc
def active_flight_info(flight_number_input, date_input, reminder):
    # Takes the flight number and break it into airline code and flight number
    flight_number_arr = [*flight_number_input]
    flight_number_str = ''
    airline_code_arr = []
    airline_code_str = ''
    for i in range(2):
        airline_code_arr.append(flight_number_arr[0])
        flight_number_arr.pop(0)
    airline_code = airline_code_str.join(airline_code_arr)
    flight_number = flight_number_str.join(flight_number_arr)

    # Takes the date and breaks up to its respective month, day, and year
    date_arr = [*date_input]
    month = str(date_arr[0] + date_arr[1])
    day = str(date_arr[3] + date_arr[4])
    year = '20' + str(date_arr[8] + date_arr[9])

    # Gets the URL of the flight
    url = 'https://www.flightstats.com/v2/flight-tracker/' + str(airline_code) + '/' + str(flight_number) + '?year=' + str(year) + '&month=' + str(month) + '&date=' + str(day)

    # Access the page and obtain the HTML code that will be used for webscraping
    page = requests.get(url)
    flight_info = BeautifulSoup(page.text, 'html.parser')

    results = flight_info.find(id='__next')

    # Flight Status
    # If the flight is ontime
    flight_status_ontime = results.find_all('div', class_='text-helper__TextHelper-sc-8bko4a-0 iicbYn')
    # If the flight is delayed
    flight_status_delayed = results.find_all('div',class_='text-helper__TextHelper-sc-8bko4a-0 hYcdHE')

    if flight_status_ontime == []:
        flight_status = flight_status_delayed[0].text
    else:
        flight_status = flight_status_ontime[0].text

    # If the flight has departed, the speed, heading, and altitude gets webscraped
    if flight_status == "Departed":
        altitude = results.find_all('span', class_='alt-and-phase__ContentBox-sc-jihjun-3 bNZNxp')
        speed = results.find_all('span', class_='bearing__HeadingValue-sc-2vsxtq-2 kLgywj')
        heading = results.find_all('span', class_='speed__HeadingValue-sc-15dwb59-1 iZlHGH')

        real_altitude = altitude[0].text
        real_speed = speed[0].text
        real_heading = heading[0].text
    else:
        real_altitude = "empty"
        real_speed = "empty"
        real_heading = "empty"
    
    # Time Activity
    activity = results.find_all('h5', class_='labeled-columns__Value-sc-j3eq63-1 exDPyn')
    
    # Notification System
    if (len(activity[2].text) <= 3) and reminder == "YES":
       notify = "ON"
    elif activity[2].text == "0m" and reminder == "YES":
       notify = "OFF"
    else:
       notify = "OFF"

    #              0                 1                 2                3                 4                5                6             7             8         9
    return activity[0].text, activity[1].text, activity[2].text, activity[3].text, activity[4].text, activity[5].text, real_altitude, real_speed, real_heading, notify
# ------------------------------------------------------------------------------------------------------------------
def display_layout(flight_info,active_info,flight_number,date):
  # Colors the border of the status in the layout
  if str(flight_info[0]) == "Scheduled" or str(flight_info[0]) == "Arrived" or str(flight_info[0]) == "Departed": 
      flight_status = flight_info[16]
  else:
      flight_status = 'red'
  # Displays Aircraft Current Activity If Aircraft Has Departed
  if str(flight_info[0]) == "Departed": 
      flight_activity = True
  else:
      flight_activity = False

  # Notification Verfication
  if active_info[9] == "ON":
     notify_status = True
  else:
     notify_status = False
      
  # PRINTS FLIGHT INFORMATION
  # Title & Date 
  console.print("LATEST FLIGHT INFORMATION ON " + "[white]" + str(flight_number) + "[/white]", style="bold", justify="center")
  console.print("[white]" + str(date) + "[/white]", style="white i", justify="center")
  
  # Main Layout
  layout = Layout()
  # Main Layout Split into Three Rows
  layout.split_column(
    # Flight Status
    Layout(Panel(Text("FLIGHT STATUS: " + flight_info[0], justify="center"), border_style=flight_status),
            name="upper"),
    # Flight Departure/Arrival Information
    Layout(name="middle"),
    # Terminal/Gate Info
    Layout(name="gates"),
    # Altitude, Heading Cruise
    Layout(name="second_middle", visible=flight_activity),
    # Tracking Time
    Layout(name="lower"),
    # Notification
    Layout(Panel(Text("NOTIFICATION: This flight will be arriving soon!", justify='center'), border_style="yellow"), name="notify", visible=notify_status)
  )

  layout["upper"].size = 3

  # Middle layout splitted into two columns (DEPARTURE AND ARRIVAL INFORMATION)
  layout["middle"].split_row(
    # DEPARTURE
    Layout(Panel(Text(flight_info[1] + "\n" + flight_info[2] + "\n\n" + "Departure Time & Date\n" + flight_info[9] + "\n\nScheduled: " + flight_info[3] + "\nActual: " + flight_info[4], justify='center'),
                  border_style='cyan',
                  padding=(1, 0),
                  title="[bold]DEPARTURE INFORMATION[/bold]", title_align="center",), 
            name="departure"),
    # ARRIVAL
    Layout(Panel(Text(flight_info[5] + "\n" + flight_info[6] + "\n\n" + "Arrival Time & Date\n" + flight_info[10] + "\n\nScheduled: " + flight_info[7] + "\nActual: " + flight_info[8], justify='center'),
                  border_style='cyan',
                  padding=(1, 0),
                  title="[bold]ARRIVAL INFORMATION[/bold]", title_align="center",), 
            name="arrival"),
  )
  layout["middle"].size = 12

  layout["gates"].split_row(
    Layout(name="departuresinfo"),
    Layout(name="arrivalsinfo")
  )
  layout["gates"].size = 5

  layout["departuresinfo"].split_row(
     # DEPARTURE TERMINAL
    Layout(Panel(Text(flight_info[11], justify='center'),
                  border_style='cyan',
                  padding=(1, 0),
                  title="[bold]DEPARTURE TERMINAL[/bold]", title_align="center",), 
            name="departure_terminal"),
    # DEPARTURE GATE
    Layout(Panel(Text(flight_info[12], justify='center'),
                  border_style='cyan',
                  padding=(1, 0),
                  title="[bold]DEPARTURE GATE[/bold]", title_align="center",), 
            name="departure_gate"),
  )

  layout["arrivalsinfo"].split_row(
    # ARRIVAL TERMINAL
    Layout(Panel(Text(flight_info[13], justify='center'),
                  border_style='cyan',
                  padding=(1, 0),
                  title="[bold]ARRIVAL TERMINAL[/bold]", title_align="center",), 
            name="arrival_terminal"),
    # ARRIVAL GATE
    Layout(Panel(Text(flight_info[14], justify='center'),
                  border_style='cyan',
                  padding=(1, 0),
                  title="[bold]ARRIVAL GATE[/bold]", title_align="center",), 
            name="arrival_gate"),
    # BAGGAGE
    Layout(Panel(Text(flight_info[15], justify='center'),
                  border_style='cyan',
                  padding=(1, 0),
                  title="[bold]BAGGAGE CLAIM[/bold]", title_align="center",), 
            name="baggage"),

  )
  # Second Middle layout splitted into three columns (ALTITUDE, HEADING, SPEED)
  layout["second_middle"].split_row(
    # ALTITUDE
    Layout(Panel(Text(active_info[6], justify='center'),
                border_style='yellow',
                padding=(1, 0),
                title="[bold]ALTITUDE[/bold]", title_align="center",), 
          name="altitude"),
    # HEADING
    Layout(Panel(Text(active_info[7], justify='center'),
                border_style='yellow',
                padding=(1, 0),
                title="[bold]HEADING[/bold]", title_align="center",), 
          name="altitude"),
    # SPEED
    Layout(Panel(Text(active_info[8], justify='center'),
                border_style='yellow',
                padding=(1, 0),
                title="[bold]SPEED[/bold]", title_align="center",), 
          name="altitude"),
      
  )

  layout["lower"].split_row(
    # TOTAL TIME
    Layout(Panel(Text(active_info[0], justify='center'),
                border_style='cyan',
                padding=(1, 0),
                title="[bold]TOTAL TIME[/bold]", title_align="center",), 
          name="altitude"),
    # TIME ELAPSED
    Layout(Panel(Text(active_info[1], justify='center'),
                border_style='cyan',
                padding=(1, 0),
                title="[bold]TIME ELAPSED[/bold]", title_align="center",), 
          name="altitude"),
    # TIME REMAINING
    Layout(Panel(Text(active_info[2], justify='center'),
                border_style='cyan',
                padding=(1, 0),
                title="[bold]TIME REMAINING[/bold]", title_align="center",), 
          name="altitude"),
  )
  layout["second_middle"].size = 5
  layout["lower"].size = 5
  layout["notify"].size = 3

  console.print(layout)
# ------------------------------------------------------------------------------------------------------------------
def display_static_layout(flight_info,flight_number,date):
  # Colors the border of the status in the layout
  if str(flight_info[0]) == "Scheduled" or str(flight_info[0]) == "Arrived" or str(flight_info[0]) == "Departed": 
      flight_status = flight_info[16]
  else:
      flight_status = 'red'

  if str(flight_info[0]) == "Cancelled":
     visibility = False
  else:
     visibility = True

  # PRINTS FLIGHT INFORMATION
  # Title & Date 
  console.print("LATEST FLIGHT INFORMATION ON " + "[white]" + str(flight_number) + "[/white]", style="bold", justify="center")
  console.print("[white]" + str(date) + "[/white]", style="white i", justify="center")
  
  # Main Layout
  layout = Layout()
  # Main Layout Split into Three Rows
  layout.split_column(
    # Flight Status
    Layout(Panel(Text("FLIGHT STATUS: " + flight_info[0], justify="center"), border_style=flight_status),
            name="upper"),
    # Flight Departure/Arrival Information
    Layout(name="middle"),
    Layout(visible=visibility,name="gates")
  )

  # Middle layout splitted into two columns (DEPARTURE AND ARRIVAL INFORMATION)
  layout["middle"].split_row(
    # DEPARTURE
    Layout(Panel(Text(flight_info[1] + "\n" + flight_info[2] + "\n\n" + "Departure Time & Date\n" + flight_info[9] + "\n\nScheduled: " + flight_info[3] + "\nActual: " + flight_info[4], justify='center'),
                  border_style=flight_status,
                  padding=(1, 0),
                  title="[bold]DEPARTURE INFORMATION[/bold]", title_align="center",), 
            name="departure"),
    # ARRIVAL
    Layout(Panel(Text(flight_info[5] + "\n" + flight_info[6] + "\n\n" + "Arrival Time & Date\n" + flight_info[10] + "\n\nScheduled: " + flight_info[7] + "\nActual: " + flight_info[8], justify='center'),
                  border_style=flight_status,
                  padding=(1, 0),
                  title="[bold]ARRIVAL INFORMATION[/bold]", title_align="center",), 
            name="arrival"),
  )

  layout["gates"].split_row(
    Layout(name="departuresinfo"),
    Layout(name="arrivalsinfo")
  )
  layout["gates"].size = 5

  layout["departuresinfo"].split_row(
     # DEPARTURE TERMINAL
    Layout(Panel(Text(flight_info[11], justify='center'),
                  border_style=flight_status,
                  padding=(1, 0),
                  title="[bold]DEPARTURE TERMINAL[/bold]", title_align="center",), 
            name="departure_terminal"),
    # DEPARTURE GATE
    Layout(Panel(Text(flight_info[12], justify='center'),
                  border_style=flight_status,
                  padding=(1, 0),
                  title="[bold]DEPARTURE GATE[/bold]", title_align="center",), 
            name="departure_gate"),
  )

  layout["arrivalsinfo"].split_row(
    # ARRIVAL TERMINAL
    Layout(Panel(Text(flight_info[13], justify='center'),
                  border_style=flight_status,
                  padding=(1, 0),
                  title="[bold]ARRIVAL TERMINAL[/bold]", title_align="center",), 
            name="arrival_terminal"),
    # ARRIVAL GATE
    Layout(Panel(Text(flight_info[14], justify='center'),
                  border_style=flight_status,
                  padding=(1, 0),
                  title="[bold]ARRIVAL GATE[/bold]", title_align="center",), 
            name="arrival_gate"),
    # BAGGAGEs
    Layout(Panel(Text(flight_info[15], justify='center'),
                  border_style=flight_status,
                  padding=(1, 0),
                  title="[bold]BAGGAGE CLAIM[/bold]", title_align="center",), 
            name="baggage"),

  )
  layout["upper"].size = 3
  layout["middle"].size = 12

  console.print(layout)
# ------------------------------------------------------------------------------------------------------------------
# MAIN FUNCTION OF THE CODE
def main():
    try:
      # Displays the Title
      console.print("ENAE380 FLIGHT TRACKER w/ FLIGHTSTAT", style="bold",justify="center")
      print("\n")

      # Provides notice to the users
      console.print("[bold]NOTICE:[/bold] The flight data that is produced in this program does not belong to me, but to its rightful owner, FLIGHTSTATS.COM. In addition, the program can produce flight within the range of three days before or after of today. However, if that flight operates multiple times a day, the program will only be able to display the latest flight operated on that day.", justify="center")
      print("\n")

      console.print("Since the method used in this code is webscraping, there can be slight issues with the syntax itself, which is beyond our control, and it could cause a total program failure. If you do happen to run into this issue, just run the program again.", justify="center")
      print("\n")

      console.print("Finally, we recommend you to put the terminal window at fullscreen to show the entire layout.", justify="center")
      print("\n")

      # Asks the user to enter the flight number
      print("Please enter your flight number (IATA Format)")
      console.print("Ex: IATA Code for [bold][i][white]Southwest 1234[/white][/i][/bold] is [bold][i][white]WN1234[/white][/i][/bold].", style="white i")
      flight_number = input("Enter Here: ").upper().replace(" ", "")
      print("\n")

      # Ask the user to enter the date of the flight
      print("Please enter the date of the flight (MM-DD-YYYY)")
      date = input("Enter here: ").replace(" ", "")
      print("\n")

      while len(date) != 10:
        console.print("[red][bold]Error:[/bold][/red] Please enter the date of the flight (MM-DD-YYYY)")
        date = input("Enter here: ").replace(" ", "")
        print("\n")

      # Asks the user if they want to be notified for when an active flight is going to arrive soon
      print("Would you like for us to notify you one hour before arrival time?")
      reminder = input("Enter here: ").upper().replace(" ", "")
      print("\n")

      while (reminder != "YES" and reminder != "NO"):
        console.print("[red][bold]Error:[/bold][/red] Would you like for us to notify you one hour before arrival time?")
        reminder = input("Enter here: ").upper().replace(" ", "")
        print("\n")      

      # Checks to see if there's information on the requested flight
      verify_status = verify_flight(flight_number, date)

      # If there's information on the flight, it will run all the necessary displays
      if verify_status == "Success":
        # Collects information
        loop = 1
        while loop == 1:
          # Grabs basic flight information
          flight_info = basic_flight_info(flight_number, date)
          # Checks to see if there's flight tracking is available for the flight
          tracking = verify_tracking(flight_number, date)

          # If the flight is active, the active flight information will be collected
          if (flight_info[0] == "Departed" and tracking == "AVAILABLE") or flight_info[0] == "Arrived":
            active_info = active_flight_info(flight_number, date, reminder)
          
          # Displays information for Scheduled Flight
          if flight_info[0] == "Scheduled":
            os.system('cls')
            display_static_layout(flight_info,flight_number,date)
            console.print("Enter [yellow][bold]CTRL + C[/bold][/yellow] to exit the program!")
            time.sleep(60)
            loop = 1

          # Displays information for Departed Flight
          if flight_info[0] == "Departed":
            # Hard code to see if tracking is available
            tracking = verify_tracking(flight_number, date)
            # Displays active flight display
            if tracking == "AVAILABLE":
              os.system('cls')
              display_layout(flight_info,active_info,flight_number,date)
              console.print("Enter [yellow][bold]CTRL + C[/bold][/yellow] to exit the program!")
              time.sleep(60)
              loop = 1
            # Displays static flight display
            else:
              os.system('cls')
              display_static_layout(flight_info,flight_number,date)
              console.print("Enter [yellow][bold]CTRL + C[/bold][/yellow] to exit the program!")
              time.sleep(60)
              loop = 1 
          # Displays information for an Arrived Flight
          if flight_info[0] == "Arrived":
            os.system('cls')
            display_layout(flight_info,active_info,flight_number,date)
            loop = 0 

          # Displays information for a Cancelled Flight  
          if flight_info[0] == "Cancelled":
            os.system('cls')
            display_static_layout(flight_info,flight_number,date)
            loop = 0 
      # If there's no information on the flight, it will print an error and will run the main code again.
      else:
        console.print("\n\n[yellow][bold]Error:[/bold][/yellow] We were unable to find the flight that you requested. Please enter a different flight. \n\n")
        main()
    # If user wants to quit anytime during the program, the user has an option to hit Ctrl + C, and the program will be terminated.
    except KeyboardInterrupt:
        print("\n[bold yellow]Program terminated by user.[/bold yellow]")

if __name__ == "__main__":
    # Runs the Main Function
    main()
