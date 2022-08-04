import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'nyc': 'nyc.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please select data for by entering: Chicago, NYC, or Washington:\n")
        if city.lower() not in ('chicago', 'nyc', 'washington'):
            print("Oops, make sure you selected a city from the list, try again.")
            continue
        else:
            break
    print('\nThe city you selected was:', city.title())
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nType the complete name of a month (January - June) of the year to filter the data, or type 'all':\n")
        if month.lower() not in ('january', 'february', 'march', 'april', 'may',
        'june', 'all'):
            print("Oops, make sure you chose a valid month, try again.")
            continue
        else:
            break
    print('\nYou selected ', month.title())
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nType a day (i.e. Monday) to filter the data, or type all:\n")
        if day.lower() not in ('sunday','monday', 'tuesday', 'wednesday',
        'thursday', 'friday', 'saturday', 'all'):
            print("Oops, make sure you chose a valid day, try again.")
            continue
        else:
            break
    print('\nYou selected ', day.title())
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    #print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode().iloc[0]
    print('The most popular month of bike use is: ', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode().iloc[0]
    print('The most popular day of bike use is: ', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode().iloc[0]
    print('The most popular starting hour of bike use is: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print('The most popoular starting station for bike users is: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print('The most popular ending station for bike users is: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['popular_trip'] = df['Start Station'] + ' - ' +  df['End Station']
    popular_trip = df['popular_trip'].value_counts().idxmax()
    print('The most popular bike route is: ', popular_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time during the selected period was ', total_travel_time/60, ' minutes.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average trip duration during the selected period was ', mean_travel_time/60, ' minutes.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print(user_types)

        # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(gender)
    except KeyError:
        print('WARNING: No gender data available for your selection.')

    # Display earliest, most recent, and most common year of birth
    try:
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        average_year = df['Birth Year'].mode().iloc[0]
        print('The oldest user was born in ', int(oldest))
        print('The youngest user was born in', int(youngest))
        print('The most common birth of year of selected users was: ', int(average_year))
    except KeyError:
        print('WARNING: No birth year data available for your selection.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# Function to display raw data
def raw_data(df):
    """Allows user to choose to view raw data. """
    
    start_loc = 0
    while True:
        view_raw_data = input("Would you like to see 5 rows of raw data? Enter 'yes' or 'no'.\n").lower()

        if view_raw_data == 'yes':
            print(df.iloc[start_loc : start_loc + 5])
            start_loc += 5

        elif view_raw_data == 'no':
            break

        else:
            print("Oops, I didn't get that. Please enter 'yes' or 'no'.\n")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
