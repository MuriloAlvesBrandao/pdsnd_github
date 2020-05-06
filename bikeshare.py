import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    
   
    while True:        
        city = input('\nWould you like to see the data for Chicago, New York City or Washington? ') .lower()
        if city not in CITY_DATA:
            print('\nhmm... i guess your input was invalid. Please type the name of one of the three cities with the exact same spelling as it appears in the question.')
        else:    
            print('\nGreat! Lets take a look at some data from {}!' .format(city.title()))
            break
           


    while True:
        month = input("\nWould you like to see the data for which month between January and June? If you want to see the whole data from January to June, type 'all': ") .lower()
        if month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'): 
           print("\nSorry, i could not recognize your input, please type the name of one specific month (or 'all') with the correct spelling (i only have data from the first six months, so please dont type the name of a month that is in the second semester of the year).")
        else:   
           print('\n{} it is, then!' .format(month.title()))
           break
        

    while True:
        day = input("\nWould you like to see the data for which day of the week? If you want to see the data for the whole week, please type 'all': ") .lower()
        if day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'): 
           print("\nOops, i could not get it. Please type the name of one specific week day (or 'all') with the correct spelling.")
        else:   
           print('\nGreat choice! Lets checkout the data from {}.' .format(day.title()))
           break
    
    print('\nSo, what we are looking for here is data from {}, in {} month(s) and {} weekday(s). Lets get it started!' .format(city.title(), month.title(), day.title()))
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
        
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    most_popular_month = df['month'].mode()[0]
    print('The month with most travels is the month number', most_popular_month,'.')


    most_popular_weekday = df['day_of_week'].mode()[0]
    print('\nThe day of the week with most travels is', most_popular_weekday, '.')


    df['hour'] = df['Start Time'].dt.hour
    most_popular_start_hour = df['hour'].mode()[0]
    print('\nThe most popular start hour is', most_popular_start_hour, "o'clock.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    most_popular_start_station = df['Start Station'].mode()[0]
    print('In the chosen city, the station on which our customers started the most travels in the given period is the', most_popular_start_station, 'station.')

    most_popular_end_station = df['End Station'].mode()[0]
    print('\nIn the chosen city, the station on which our customers finished the most travels in the given period is the', most_popular_start_station, 'station.')


    df['routs'] = 'from ' + df['Start Station'] + ' station to ' + df['End Station'] + ' station.' 
    most_popular_rout = df['routs'] .mode()[0]
    print('\nIn the chosen city, the most used rout by our customers in the given period is the one that goes', most_popular_rout)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    total_travel_time = df['Trip Duration'].sum()
    print('In the chosen city and in the given period, our customers traveled a combined amount of', total_travel_time, 'seconds')


    mean_travel_time = df['Trip Duration'].mean()
    print('\nIn the chosen city and in the given period, each travel had, on average, a duration time of', mean_travel_time, 'seconds')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    user_types_count = df['User Type'].value_counts()
    print("In the chosen city and in the given period, the total amount of travels made by each one of our three kinds of customers ('Customer', 'Subscriber' and 'Dependent') is provided in the frame below:\n\n", user_types_count)


    if 'Gender' in df:
        counts_of_gender = df['Gender'].value_counts()
        print("\n\nIn the chosen city and in the given period, the amount of travels made by men and women, individually, is provided in the frame below:\n\n", counts_of_gender)
    else:
        print("\nThere are no records of the amount of travels made by men and women in the chosen city.")

    if 'Birth Year' in df:
        older = df['Birth Year'].min()
        print("\n\nIn the chosen city and in the given period, our oldest customer to take a ride was born in the year", older)
        younger = df['Birth Year'].max()
        print("\nIn the chosen city and in the given period, our youngest customer to take a ride was born in the year", younger)
        most_common_birth_year = df['Birth Year'].mode()[0]
        print("\nIn the chosen city and in the given period, the majority of our customers that took a ride was born in the year", most_common_birth_year)
    else:
        print("\nThere are no records of the birth year of customers in the chosen city")    
   
              
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    print('\n\nWow that was fun! I Hope that the data provided above is usefull for you!! You can checkout some additional raw data from our database if you want.')
    
    
def additional_raw_data(df):
    rows_of_raw_data = 0
    while True:
        raw_data_input = input("\nWould you like to view 05 more rows of additional raw data (answer with 'yes' or 'no'): ").lower()           
        if raw_data_input == 'no':
            print("\nOK then! You can come back at anytime. You also can restart the whole process by answering 'yes' to the question below.")
            break
        elif raw_data_input == 'yes':
            rows_of_raw_data += 5
            print(df.iloc[: rows_of_raw_data])                         
        elif raw_data_input not in ('yes', 'no'):
            print("\nSorry, i could not recognize your answer. Make sure you are typing only the words 'yes' or 'no'.")
                            
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        additional_raw_data(df)

        restart = input("\nWould you like to restart? (answer with 'yes' or 'no'): ") .lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
