import time
import pandas as pd
import numpy as np
import datetime as dt
import os

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

months = ('january', 'february', 'march', 'april', 'may', 'june')
weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')


def choice(prompt, choices=('y', 'n')):
    """Return a valid input from the user given an array of possible answers."""
    while True:
        user_input = input(prompt).lower().strip()
        if user_input == 'end':
            raise SystemExit
        elif ',' in user_input:
            user_choices = [i.strip().lower() for i in user_input.split(',')]
            if all(item in choices for item in user_choices):
                return user_choices
        elif user_input in choices:
            return user_input

        print("Something is not right. Please ensure you enter a valid option.\n")


def get_filters():
    """Ask user to specify city(ies) and filters, month(s), and weekday(s)."""
    print("\n\nLet's explore some US bikeshare data!\n")
    print("Type 'end' at any time if you would like to exit the program.\n")

    while True:
        city = choice("\nFor what city do you want to select data: "
                      "New York City, Chicago, or Washington? "
                     , list(CITY_DATA.keys()))
        month = choice("\nFrom January to June, for what month(s) do you "
                       "want to filter data? \n>",
                       months)
        day = choice("\nFor what day you want to filter bikeshare (sunday, monday, tuesday, wednesday, thursday, friday, saturday) "
                     "data? \n>", weekdays)

        confirmation = choice("\nConfirm that you like to apply "
                              "the following filter to the bikeshare data."
                              "\n\n City(ies): {}\n Month(s): {}\n Weekday(s): {}\n\n [y] Yes - [n] No\n\n>"
                              .format(city, month, day))
        if confirmation == 'y':
            break
        else:
            print("\nLet's try this again!")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Load data for the specified filters of city(ies), month(s), and day(s)."""
    print("\nThe program is loading the data for the filters of your choice.")
    start_time = time.time()

    # Load data for the selected city filters
    if isinstance(city, list):
        df = pd.concat(map(lambda c: pd.read_csv(CITY_DATA[c]), city), sort=True)
    else:
        df = pd.read_csv(CITY_DATA[city])

    # Reorganize DataFrame columns after a city concat
    try:
        df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time', 'Trip Duration', 
                                 'Start Station', 'End Station', 'User Type', 'Gender', 
                                 'Birth Year'])
    except KeyError:
        pass

    # Create columns to display statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday
    df['Start Hour'] = df['Start Time'].dt.hour

    # Filter the data according to month(s) and weekday(s)
    if isinstance(month, list):
        df = df[df['Month'].isin([months.index(m) + 1 for m in month])]
    else:
        df = df[df['Month'] == months.index(month) + 1]

    if isinstance(day, list):
        df = df[df['Weekday'].isin([weekdays.index(d) for d in day])]
    else:
        df = df[df['Weekday'] == weekdays.index(day)]

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

    return df


def time_stats(df):
    """Display statistics on the most frequent times of travel."""
    print('\nDisplaying the statistics on the most frequent times of travel...\n')
    start_time = time.time()

    most_common_month = df['Month'].mode()[0]
    print('For the selected filter, the month with the most travels is: ' +
          str(months[most_common_month-1]).title() + '.')

    most_common_day = df['Weekday'].mode()[0]
    print('For the selected filter, the most common day of the week is: ' +
          weekdays[most_common_day].title() + '.')

    most_common_hour = df['Start Hour'].mode()[0]
    print('For the selected filter, the most common start hour is: ' +
          str(most_common_hour) + '.')

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def station_stats(df):
    """Display statistics on the most popular stations and trip, including user type."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    print("For the selected filters, the most common start station is: " +
          most_common_start_station)

    most_common_end_station = df['End Station'].mode()[0]
    print("For the selected filters, the most common end station is: " +
          most_common_end_station)

    most_common_user_type = df['User Type'].mode()[0]
    print("For the selected filters, the most common user type is: " +
          most_common_user_type)

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (f"{total_travel_time // 86400}d " +
                         f"{(total_travel_time % 86400) // 3600}h " +
                         f"{(total_travel_time % 3600) // 60}m " +
                         f"{total_travel_time % 60}s")
    print('For the selected filters, the total travel time is : ' +
          total_travel_time + '.')

    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (f"{mean_travel_time // 60}m {mean_travel_time % 60}s")
    print("For the selected filters, the mean travel time is : " +
          mean_travel_time + ".")

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def user_stats(df, city):
    """Display statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types_count = df['User Type'].value_counts()
    print("For the selected filters, the user type count is:\n" +
          str(user_types_count))

    if city != 'washington':
        gender_count = df['Gender'].value_counts()
        print("\nFor the selected filters, the gender count is:\n" +
              str(gender_count))

        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print(f"\nFor the selected filters, the earliest year of birth is: {earliest_birth_year}.")
        print(f"For the selected filters, the most recent year of birth is: {most_recent_birth_year}.")
        print(f"For the selected filters, the most common year of birth is: {most_common_birth_year}.")

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def raw_data(df):
    """Display data upon request by the user."""
    print('\nThis section show data from the dataframe.')
    display_raw = choice("\nWould you like to load some data? [y] Yes - [n] No\n>")
    if display_raw == 'y':
        counter = 0
        while True:
            print(df.iloc[counter:counter + 5])
            counter += 5
            more_data = choice("\nWould you like to load more data? [y] Yes - [n] No\n>")
            if more_data != 'y':
                break
        print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = choice("\nWould you like to restart the program? [y] Yes - [n] No\n>")
        if restart != 'y':
            print("\nThank you for using the US bikeshare data application.")
            break


if __name__ == "__main__":
    main()
