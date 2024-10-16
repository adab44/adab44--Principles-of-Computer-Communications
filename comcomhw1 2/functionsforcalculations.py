#
import pandas as pd
import re
import matplotlib.pyplot as plt

def Load_Data(filename):
    data = []
    with open(filename, 'r') as file:
        current_day = None
        current_session = None
        for line in file:
            if '----' in line:
                match_day = re.search(r'----\s+(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+----', line)
                if match_day:
                    current_day = match_day.group(1)
                    hour = int(match_day.group(2)[:2])
                    if hour < 12:
                        current_session = 'morning'
                    elif hour < 18:
                        current_session = 'noon'
                    else:
                        current_session = 'evening'
            else:
                match = re.search(r'(\d+\.\d+\.\d+\.\d+) is reachable, taken time: (\d+\.\d+) ms', line)
                if match and current_day and current_session:
                    ip = match.group(1)
                    ping_value = float(match.group(2))
                    data.append([ip, ping_value, current_day, current_session])
    
    df = pd.DataFrame(data, columns=['IP', 'PingValue', 'Day', 'Session'])
    df['Day'] = pd.to_datetime(df['Day'])
    df['Weekday'] = df['Day'].dt.day_name()
    return df

#min max avg calc.
def calculate_min(df):
    return df.groupby(['IP', 'Session'])['PingValue'].min().reset_index()

def calculate_avg(df):
    return df.groupby(['IP', 'Session'])['PingValue'].mean().reset_index()

def calculate_max(df):
    return df.groupby(['IP', 'Session'])['PingValue'].max().reset_index()

def calculate_daily_min(df):
    return df.groupby(['Weekday', 'Session', 'IP'])['PingValue'].min().reset_index()

def calculate_daily_avg(df):
    return df.groupby(['Weekday', 'Session', 'IP'])['PingValue'].mean().reset_index()

def calculate_daily_max(df):
    return df.groupby(['Weekday', 'Session', 'IP'])['PingValue'].max().reset_index()

#ordeer ip
def sort_by_given_ip_order(df, ip_order):
    df['IP'] = pd.Categorical(df['IP'], categories=ip_order, ordered=True)
    df = df.sort_values('IP')
    return df

# türkiyeden başlayarak uzaklaşıyor
ip_order = ["160.75.25.62", "185.45.67.130", "185.104.182.64", "79.139.60.97", 
            "85.239.69.14", "141.101.90.96", "195.72.120.33", "185.18.139.126", 
            "104.17.157.36", "23.227.38.74"]

#ploting variables and saving as image
def Plot_Val(min_values, avg_values, max_values, title, filename):
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    
    #min
    axs[0].bar(min_values['IP'], min_values['PingValue'], color='lightblue', alpha=0.6)
    axs[0].plot(min_values['IP'], min_values['PingValue'], marker='o', color='blue', label='Min Ping Value')
    axs[0].set_title(f'{title} - Minimum Values')
    axs[0].set_ylabel('Ping (ms)')
    axs[0].tick_params(axis='x', rotation=45)
    axs[0].legend()

    #avg
    axs[1].bar(avg_values['IP'], avg_values['PingValue'], color='lightgreen', alpha=0.6)
    axs[1].plot(avg_values['IP'], avg_values['PingValue'], marker='o', color='green', label='Avg Ping Value')
    axs[1].set_title(f'{title} - Average Values')
    axs[1].set_ylabel('Ping (ms)')
    axs[1].tick_params(axis='x', rotation=45)
    axs[1].legend()

    #max
    axs[2].bar(max_values['IP'], max_values['PingValue'], color='lightcoral', alpha=0.6)
    axs[2].plot(max_values['IP'], max_values['PingValue'], marker='o', color='red', label='Max Ping Value')
    axs[2].set_title(f'{title} - Maximum Values')
    axs[2].set_ylabel('Ping (ms)')
    axs[2].tick_params(axis='x', rotation=45)
    axs[2].legend()

    plt.tight_layout()
    plt.savefig(filename)  #Save plot as a PNG 
    plt.close()

#daily min max avg plotting and saving
def Plot_daily_Val(daily_min, daily_avg, daily_max):
    days = daily_min['Weekday'].unique()
    sessions = ['morning', 'noon', 'evening']
    
    for day in days:
        for session in sessions:
            day_min = daily_min[(daily_min['Weekday'] == day) & (daily_min['Session'] == session)]
            day_avg = daily_avg[(daily_avg['Weekday'] == day) & (daily_avg['Session'] == session)]
            day_max = daily_max[(daily_max['Weekday'] == day) & (daily_max['Session'] == session)]
            
            title = f'{day} - {session.capitalize()}'
            filename = f'{day}_{session}_values.png'
            Plot_Val(day_min, day_avg, day_max, title, filename)

#all 4 days min max overall plotting and saving
def plot_overall_extremes(daily_min, daily_avg, daily_max):
    overall_min = daily_min.loc[daily_min['PingValue'].idxmin()]
    overall_avg = daily_avg.loc[daily_avg['PingValue'].idxmin()]
    overall_max = daily_max.loc[daily_max['PingValue'].idxmax()]

    print("Overall Min:\n", overall_min)
    print("Overall Avg:\n", overall_avg)
    print("Overall Max:\n", overall_max)

    #general min max avg
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    #min
    axs[0].bar([overall_min['IP']], [overall_min['PingValue']], color='blue', alpha=0.6)
    axs[0].plot([overall_min['IP']], [overall_min['PingValue']], marker='o', color='blue')
    axs[0].set_title('Overall Minimum')
    axs[0].set_ylabel('Ping (ms)')
    
    #avg
    axs[1].bar([overall_avg['IP']], [overall_avg['PingValue']], color='green', alpha=0.6)
    axs[1].plot([overall_avg['IP']], [overall_avg['PingValue']], marker='o', color='green')
    axs[1].set_title('Overall Average')
    axs[1].set_ylabel('Ping (ms)')
    
    #max
    axs[2].bar([overall_max['IP']], [overall_max['PingValue']], color='red', alpha=0.6)
    axs[2].plot([overall_max['IP']], [overall_max['PingValue']], marker='o', color='red')
    axs[2].set_title('Overall Maximum')
    axs[2].set_ylabel('Ping (ms)')
    
    plt.tight_layout()
    plt.savefig('overall_extremes.png')  #save the overall plot as PNG
    plt.close()


filename = 'dailypings.txt'
data = Load_Data(filename)


min_values_of_4days = calculate_min(data)
avg_values_of_4days = calculate_avg(data)
max_values_of_4days = calculate_max(data)
daily_min_values = calculate_daily_min(data)
daily_avg_values = calculate_daily_avg(data)
daily_max_values = calculate_daily_max(data)

min_values_of_4days = sort_by_given_ip_order(min_values_of_4days, ip_order)
avg_values_of_4days = sort_by_given_ip_order(avg_values_of_4days, ip_order)
max_values_of_4days = sort_by_given_ip_order(max_values_of_4days, ip_order)

daily_min_values = sort_by_given_ip_order(daily_min_values, ip_order)
daily_avg_values = sort_by_given_ip_order(daily_avg_values, ip_order)
daily_max_values = sort_by_given_ip_order(daily_max_values, ip_order)

Plot_Val(min_values_of_4days, avg_values_of_4days, max_values_of_4days, "All Days (IP and Session-based)", "all_days_values.png")
Plot_daily_Val(daily_min_values, daily_avg_values, daily_max_values)
plot_overall_extremes(daily_min_values, daily_avg_values, daily_max_values)
