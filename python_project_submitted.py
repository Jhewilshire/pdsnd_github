# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 20:37:29 2021

@author: jhe
"""

import time
import pandas as pd
import numpy as np

# cities can be added/removed here in CITY_DATA dist
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv',
              } 

weekday_count = {0:'Monday', 1:'Tuesday', 2:'Wednesday',3:'Thursday', 4:'Friday', 5:;'Saturday', 6:'Sunday'}

months = ['january', 'february', 'march', 'april', 'may', 'june']

line = '-'*40

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
  
    city = None
    while city not in CITY_DATA:
        city = input("Which city's data would you like you see? Please choose Chicago, New York, or Washington?\n")
        city = city.lower()

    month = None
    while month not in months and month != 'all':
        month = input("Which month do you like to filter by? All, January, February, March, April, May, or June? Please type out the full month name.\n")
        month = month.lower()

    day = input("Which day of the week do you like to filter by? All, Monday, Tuesday, ..., Sunday? Monday is day 0.\n")
    day = day.lower().title() #change format to match day_of_week column in the dataframe
    if day.lower() != 'all':
        weekday_as_int = time.strptime(day.title(), "%A").tm_wday
        print("We are filtering by {}, {}th day of the week.".format(day,weekday_as_int))

    print(line)
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
    # load data file into a dataframe and covert time collumns to datetime
    df = pd.read_csv(CITY_DATA[city], parse_dates = ['Start Time','End Time'])
    
    # extract month and day of the week from Start Time column to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':
        df = df[df['day_of_week'] == day]    

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = months[df['month'].mode()[0]-1].title()
    print("Most popular month for traveling: \n{}".format(popular_month))

    popular_day = df['day_of_week'].mode()[0]
    print("Most popular day for traveling: \n{}".format(popular_day))

    df['start hour'] = df['Start Time'].dt.hour
    popular_hour = df['start hour'].mode()[0]
    print("Most popular hour of the day to start travelling: \n{}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(line)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print("Most popular start station: \n{}".format(popular_start_station))

    popular_end_station = df['End Station'].mode()[0]
    print("Most popular start station: \n{}".format(popular_end_station))

    df['combination station'] = df['Start Station'].map(str) + ' - ' + df['End Station'].map(str)
    popular_combination = df['combination station'].mode()[0]
    print("Most popular combination of start & end stations is: \n{}".format(popular_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(line)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("Total trip duration(in minutes) for the selected filter: ", df['Trip Duration'].sum()/60, "\nTrip Count:", df.size)

    print("Average trip duration(in minutes) for the selected filter: ", df['Trip Duration'].mean()/60)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(line)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    print("User type information:\n",df['User Type'].value_counts())
    
    # Washington city data doesn't include Gender or Birth Year, therefore, handling cities with User detailed info. here first. 
    if city not in CITY_DATA.key:
        print("User gender breakdown:\n", df['Gender'].value_counts())
        print("The oldest, youngest year of birth in the select filtered group:\n", int(df['Birth Year'].min()),",", int(df['Birth Year'].max()) ,",respectively")
        print("The most common year of birth is:\n", int(df['Birth Year'].mode()[0]))
    
    # Handling Washington city data here.
    else:
        print("User gender breakdown:\n{} has no gender data.".format(city))
        print("The oldest, youngest year of birth in the select filtered group:\n{} has no birth year data.".format(city))
        print("The most common year of birth is:\n{} has no birth year data.".format(city))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print(line)

    
def display_user(df):
    """Display raw user data upon requested by user."""
    
    n=0
    while n < len(df) or (n+5) <= len(df):
        print(df.iloc[n:(n+5),:])
        n += 5
        if n > len(df):
            break
        else:
            display_countine = input("Do you want to see more, yes or no:\n")
            if display_countine.lower() != 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # ask user if user wants to see raw data
        display = input("Do you want to see raw data, yes or no:\n")
        if display.lower() == 'yes':
            display_user(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
