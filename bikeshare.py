
import time
import pandas as pd
import numpy as np



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def df_is_null(df):
    """Checks if the data frame is null and returns a print statement if null."""
    
    if df.shape[0] == 0:
        print("There is no data for this filter.")
        return True
    return False



def get_filters():
    
    #fixes month and day parameters to all if there is no filter specified.
    
    month = 'all'
    day = 'all'
    
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city = input("Please enter the city you want to analyze: chicago, new york city or washington.\n")
    
    #check if city name is valid.
    
    while city.lower() != 'chicago' and city.lower() != 'new york city' and city.lower() != 'washington':
        city = input("Please enter a valid city name: chicago, new york city or washington.\n")
        
    city = city.lower()
    
    #ask the user if they want filter and which one:
    
    filter_dm = input('Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.\n')
    
    while filter_dm.lower() != 'month' and filter_dm.lower() != 'day' and filter_dm.lower() != 'none' and filter_dm.lower() != 'both':
        filter_dm = input('Please enter a valid filter: month, day, both, or none.')


    # get user input for month (all, january, february, ... , june)
    
    if filter_dm.lower() == 'both' or filter_dm.lower() == 'month':
        month = input("Please enter a month to filter by from january to june.\n")
        while month.lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input("Please enter a valid month: january, february, march, april, may, june.\n")
            
        month = month.lower()
        
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    
    if filter_dm.lower() == 'both' or filter_dm.lower() == 'day':
        day = input("Please enter the name of the day of week you want to filter in integer (i.e. monday=0,...,sunday=6).\n")
        while int(day) not in [0,1,2,3,4,5,6]:
            day = input("Please enter a valid day in integer (i.e. monday=0,...,sunday=6).\n")


    print('-'*40)
    return city, month, day

"""
           day input
    """

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
    
    #reads the selected city's file
   
    df = pd.read_csv(CITY_DATA[city])
    
    #convert start time to datetime type

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #gets the month and day of week columns to filter.
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == int(day.title())]


    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    
    if month == 'all':
        print("The most common month is:", months[df['month'].mode()[0] - 1])
    else:
        print("There is no common month since you've selected", month)


    # display the most common day of week
    
    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    
    if day == 'all':
        print("The most common day of week is:", days[df['day_of_week'].mode()[0]])
    else:
        print("There is no common day since you've selected", days[int(day)])


    # display the most common start hour
    
    df['Start Hour'] = df['Start Time'].dt.hour
    
    if df['Start Hour'].shape[0] == 0:
        print("There is no common start hour for your filter %s and %s." % (month, day))
    else:
        print("The most common start hour is:", df['Start Hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    
    print("The most commonly used start station is:", df['Start Station'].value_counts().index[0])
    print("Count:", df['Start Station'].value_counts()[0])


    # display most commonly used end station
    
    print("The most commonly used end station is:", df['End Station'].value_counts().index[0])
    print("Count:", df['End Station'].value_counts()[0])


    # display most frequent combination of start station and end station trip
    
    df['Start-End Trip'] = df['Start Station'] + " and " + df['End Station']
    print("The most frequent combination of start station and end station trip is:", df['Start-End Trip'].value_counts().index[0])
    print("Count:", df['Start-End Trip'].value_counts()[0])

 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def convert(seconds): 
    
    """Converts seconds into a string of hour, minutes, and seconds."""
    
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds) 




def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    
    seconds = df['Trip Duration'].sum()
    print("The total travel time is: %s hh:mm:ss" % (convert(seconds)))


    # display mean travel time
    
    seconds_mean = df['Trip Duration'].mean()
    
    print("The mean travel time is: %s hh:mm:ss" % (convert(seconds_mean)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    
    print("The counts of user types: ", df['User Type'].value_counts())
    

    # Display counts of gender
    
    try:
        gender = df['Gender'].fillna("Not Specified")
        print("The counts of user types: ", gender.value_counts())
    except:
        print("There is no gender information.")
      


    # Display earliest, most recent, and most common year of birth
    
    try:
        birth_year = df['Birth Year'].dropna()
    
        print("The earliest year of birth is:", birth_year.min())
        print("The most recent year of birth is: ", birth_year.max())
        print("The most common year of birth is: ", birth_year.mode()[0])
    except:
        print("There is no birth information.")
            
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def dictionary_filter(df):
    
    df_new = df.rename(columns = {'Unnamed: 0' : 'Customer ID'})
    
    customer_view = input("Do you like to view some individual trips?\n")
    
    row = len(df_new.index)
    
    if customer_view.lower() == "yes":
        print("Total customer count with this filter is", row)
        n = int(input("How many customers would you like to view?\n"))
        if n <= row:
            for i in range(n):
                print(df_new.iloc[i,:])
                print()
        else: print("Sorry, we don't have %d customers." % (n))
        
     


        
    
                
        


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df_is_null(df):
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        
        else:
            time_stats(df, month, day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            dictionary_filter(df)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break


if __name__ == "__main__":
	main()

