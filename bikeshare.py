import time
from datetime import datetime as dt
import pandas as pd
import numpy as np
import statistics as st


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Creating my own period dictionaries to simplify user input

months = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June', 100:'All'}
days = {6:'Sunday',0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',100:'All'}
cities = ['Chicago', 'Washington', 'New York City']

#FOR MY SOLUTION I WILL COMBINE MY DATASETS INTO ONE DATAFRAME - to learn appending dataframes
#I start by adding a CITY field in each dataset before appending them
chicago = pd.DataFrame(pd.read_csv(CITY_DATA['chicago']))
chicago['City'] = 'Chicago'

nyc = pd.DataFrame(pd.read_csv(CITY_DATA['new york city']))
nyc['City'] = 'New York City'

wash = pd.DataFrame(pd.read_csv(CITY_DATA['washington']))
wash['City'] = 'Washington'

#APPENDING ALL DATAFRAMES INTO ONE 'DF' DATAFRAME
df = chicago.append(nyc)
df = df.append(wash)


# creating the additional fields I will need

df['Start Time'] = pd.to_datetime(df['Start Time']) # Converting time fields to type datetime
df['End Time'] = pd.to_datetime(df['End Time'])     # Converting time fields to type datetime
df['Trip Duration'] = pd.to_numeric(df['Trip Duration']) # convert duration to a number for calculations

df['month'] = pd.to_numeric(df['Start Time'].dt.month)         # month of the year (1-12)
df['year'] = pd.to_numeric(df['Start Time'].dt.year)           # year as a numeric value
df['day'] = pd.to_numeric(df['Start Time'].dt.dayofweek)       # day of the week Mon = 0, Sat = 6
df['start hour'] = df['Start Time'].dt.hour                    # hour of trip start time
df['end hour'] = df['End Time'].dt.hour                        # hour of trip end time
df['trip'] = df['Start Station'] + ' : ' + df['End Station']   #concatinated string of from and destination station



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in cities:
        city = input('Choose a city to explore:chicago, new york city OR washington : ').title()
    print('Thanks, you selected ', city)




    # TO DO: get user input for month (all, january, february, ... , june)
    month = ''
    while month not in months:
        m_holder = input('Do you want to analyse a particular month? Choose 1 - 6 OR 100 for ALL: ')
        month = int(m_holder)



    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = 1000 #starting day choice to be FALSE
    while day not in days:
        d_holder =input('Do you want to analyse a particular day of the week? Choose Mon = 0, Sun = 6 OR 100 for ALL: ')
        day =int(d_holder)



    print('-'*40)
    return city, month, day


def load_data(city, month, day,df):

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """


    df = df[df['City'] == city]                 #Filters data by selected city

    if month != 100:
        df = df[df['month'] == month]           #Filters data by selected month

    if day != 100:                              #Filters data by selected day
        df = df[df['day'] == day]






    return df

def view_data(df,city):
    # Offering the user an option to see the first 5 records of filtered data
    answers = ['Yes','No']
    response = ''
    while response not in answers:
        if response == 'No':
            break
        else:
            response = input('Would you like to see the 1st 5 records in your data? enter yes or no: ').title()


    print('Here are the 1st 5 records in',city,' dataset')
    print(df.iloc[0:5])








def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode().iloc[0]
    print('Most Common Month: ', months[common_month]) # utilises months dictionary to display month name


    # TO DO: display the most common day of week
    common_day = df['day'].mode().iloc[0]
    print('Most Common Day: ', days[common_day])       # utilises the 'days' dictionary to display day name


    # TO DO: display the most common start hour
    common_hour = df['start hour'].mode().iloc[0]
    print('Most Common Hour: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def month_growth_stats(df,city):

    """Displays statistics on the growth of rides over the start and latest month in the dataset.
       Formular: (Latest month rides / earliest month rides - 1)*100
       inputs: 1) dataset with user-defined filters, 2) city selected by the user"""

    print('\nCalculating BikeShare rides growth since the earliest MONTH with user data filters...\n')
    start_time = time.time()

    start_month = df['month'].min()
    end_month = df['month'].max()
    rides_latest_month = df[df['month'] == end_month]['Start Time'].count()
    rides_start_month = df[df['month'] == start_month]['Start Time'].count()
    rides_growth = round((rides_latest_month / rides_start_month - 1)*100,1)

    print('In', city,'Bike Share began in', months[start_month],'with',f"{round(rides_start_month,0):,d}",'rides recorded,\n')
    print('By',months[end_month],'total rides were',f"{rides_latest_month:,d}")
    print('Total Rides Growth = ',rides_growth,'%')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = st.mode(df['Start Station'])
    print('Most Common Start Station: ', common_start_station)


    # TO DO: display most commonly used end station
    common_end_station = st.mode(df['End Station'])
    print('Most Common End Station: ', common_end_station)


    # TO DO: display most frequent combination of start station and end station trip
    common_trip = st.mode(df['trip'])
    print('Most Common Trip: ', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: ',f"{ int(total_travel_time):,d}")


    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time: ',f"{ int(mean_travel_time):,d}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if city != 'Washington':
        print(df['User Type'].value_counts())
    else:
        print('NO USER TYPE DATA AVAILABLE FOR WASHINGTON')





    # TO DO: Display counts of gender
    if city != 'Washington':                                #Washington dataset does not have a gender field
        female_user_count = df[df['Gender']== 'Female']['Gender'].count()
        male_user_count = df[df['Gender']== 'Male']['Gender'].count()
        female_percentage = round((female_user_count /(female_user_count +  male_user_count))*100,2)
        print('Females are', female_percentage,'% of the users','Males are', 100.0 - female_percentage,'%')
        print(df['Gender'].value_counts())
    else:
        print('NO GENDER DATA AVAILABLE FOR WASHINGTON')


    # TO DO: Display earliest, most recent, and most common year of birth
    if city != 'Washington':
        print('Earliest Year of Birth: ',int(df['Birth Year'].min()))
        print('Latest Year of Birth: ',int(df['Birth Year'].max()))
        print('Most Common Year of Birth: ',int(st.mode(df['Birth Year'])))
    else:
        print('NO DATE OF BIRTH DATA AVAILABLE FOR WASHINGTON')





    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df_filtered = load_data(city, month, day,df)

        view_data(df,city)
        time_stats(df_filtered)
        month_growth_stats(df_filtered,city)
        station_stats(df_filtered)
        trip_duration_stats(df_filtered)
        user_stats(df_filtered,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
