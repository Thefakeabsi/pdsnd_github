import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}


def print_message(string):  #Delays each print statement by .7 seconds
    print(string)
    time.sleep(.7)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply
        no month
         filter
        (str) day - name of the day of week to filter by, or "all" to apply no
        day filter
    """
    print_message('Hello! Let\'s explore some US bikeshare data!')

    while True:  #Gets the user input for the city
        while True:
            cities = ['chicago', 'new york city', 'washington']
            city = input('Enter the city you want to view, Chicago, New York City, or Washington: \n').lower()
            if city not in cities:
                print_message('I\'m sorry, your input does not work.  Please try again.')
            else:
                break

    # Gets the user input to filter for the month
        while True:
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = input('Enter the month you want to filter with, from January to June: \n').lower()
            if month == 'all':
                break
            elif month not in months:
                print_message('I\'m sorry, your input does not work.  Please try again.')
            else:
                break
    # Gets the user input for the day of week (all, monday, tuesday, ... sunday)
        while True:
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            day = input('Enter the day of the week you want to filter with, from Monday to Sunday: \n').lower()
            if day == 'all':
                break
            elif day not in days:
                print_message('I\'m sorry, your input does not work.  Please try again.')
            else:
                break
        print_message('-'*40)
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

    # filters by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filters by the month to create the new dataframe
        df = df[df['month'] == month]

    # filters by the day of week if applicable
    if day != 'all':
        # filter by the day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]



    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print_message('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displays the most common month
    if month == 'all':
        common_month = df['month'].mode()[0]
        month_list = ['January', 'February', 'March', 'April', 'May', 'June']
        common_month = month_list[common_month - 1]
        print_message("The most common month to travel is {}.".format(common_month.title()))
    else:
        print_message('The selected data is filtered by {}.'.format(month.title()))
    # Displays the most common day of week
    if day == 'all':
        common_day = df['day_of_week'].mode()[0]
        print_message("The most common day of the week to travel is {}.".format(common_day))
    else:
        print_message("The selected data is filtered by {}.".format(day))

    # Displays the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    if common_hour > 12:
        common_hour -= 12
        print_message("The most common start hour is {} o'clock PM.".format(common_hour))
    else:
        print_message("The most common start hour is {} o'clock AM.".format(common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print_message('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print_message('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays the most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print_message(f"The most commonly used start station is {common_start}.")
    print(" ")
    # Displays the most commonly used end station
    common_end = df['End Station'].mode()[0]
    print_message(f"The most commonly used end station is {common_end}.")
    print(" ")
    # Displays the most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    common_trip = df['trip'].mode()[0]
    print_message(f"The most commonly used trip combination is {common_trip}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays the total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print_message(f'The total travel time is {hour} hours, {minute} minutes, and {second} seconds.')

    # Displays the mean travel time
    avg_duration = df['Trip Duration'].mean()
    m, s = divmod(avg_duration, 60)
    if m > 60:
        h, m = divmod(avg_duration, 60)
        print_message(f'The average trip time is {hour} hours, {minute} minutes, and {second} seconds.')
    else:
        print_message(f'The average trip time is {minute} minutes, and {second} seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays the counts of user types
    print_message("Here are the counts of the different user types.")
    print(df['User Type'].value_counts())

    # Displays the counts of gender
    if city != 'washington':
        print_message('Here are the counts of the different genders.')
        print(df['Gender'].value_counts())
        print('')
        print_message('Here is the earliest year of birth.')
        print(int(df['Birth Year'].min()))
        print_message('Here is the latest year of birth.')
        print(int(df['Birth Year'].max()))
        print_message('Here is the most common year of birth')
        print(int(df['Birth Year'].mode()))

    # Displays the earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df): # Allows user to view the raw data, 5 rows at a time
    start = 0
    end = 5
    answer = input('Do you wish to access the raw data?').lower()
    if 'yes' in answer:
        while end <= df.shape[0]-1:
            print_message(df.iloc[start:end,:])
            start += 5
            end += 5

            display = input("Do you want to see more raw data?: \n").lower()
            if display == 'no':
                break




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
