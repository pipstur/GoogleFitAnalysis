from cProfile import label
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

podaci = pd.read_csv("F:\\fitnes\\Takeout\\Fit\\Daily activity metrics\Daily activity metrics.csv", parse_dates= True)


#Firstly, we need to clean all this data, some of the columns like the average weight and max height and so on are mostly empty, 
# since I haven't really kept up with my weight because it mostly stays the same, we will drop these columns

podaci.drop(['Average weight (kg)', 'Max weight (kg)', 'Min weight (kg)'], inplace=True, axis=1)
#This next line of code will parse strings as dates
podaci['Date'] = pd.to_datetime(podaci['Date'], dayfirst=True)

#we must fill the NA data, since 0's will not disrupt anything
podaci.fillna(0, inplace=True)

#Now it is crucial to convert most of the things to integers, and to something clearer as it will be easier and cleaner to graph
podaci['Calories (kcal)'] = (podaci['Calories (kcal)'] // 1).astype(int)
podaci['Distance (m)'] = (podaci['Distance (m)'] // 1).astype(int)
podaci['Average speed (m/s)'] = round(podaci['Average speed (m/s)'] * 3600 / 1000, 1)
podaci['Max speed (m/s)'] = round(podaci['Max speed (m/s)'] * 3600 / 1000, 1)
podaci['Min speed (m/s)'] = round(podaci['Min speed (m/s)'] * 3600 / 1000, 1)
podaci['Step count'] = podaci['Step count'].astype(int)
podaci['Walking duration (ms)'] = (podaci['Walking duration (ms)'] // 1000 // 60).astype(int)
podaci['Running duration (ms)'] = (podaci['Running duration (ms)'] // 1000 // 60).astype(int)

#And we will rename these columns so they represent the conversion from m/s to km/h
podaci.rename({'Average speed (m/s)': 'Average speed (km/h)', 
             'Max speed (m/s)': 'Max speed (km/h)', 
             'Min speed (m/s)': 'Min speed (km/h)', 
             'Walking duration (ms)': 'Walking duration (min)',
             'Running duration (ms)': 'Running duration (min)', }, axis=1, inplace=True)
            
#Adding days of the week as well
podaci['Day of Week'] = podaci['Date'].dt.dayofweek
days_of_week = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
podaci['Day of Week'].replace(days_of_week, inplace=True)
cols = ['Date', 'Day of Week', 'Calories (kcal)', 'Distance (m)', 'Average speed (km/h)', 'Max speed (km/h)', 'Min speed (km/h)', 'Step count', 'Move Minutes count', 'Walking duration (min)', 'Running duration (min)', 'Heart Points']
podaci = podaci[cols]


#Graphing the exact number of move minutes per day
fig = plt.figure(figsize=(8,5))
plt.plot(podaci['Date'], podaci['Move Minutes count'], color='b')
plt.title('Minutes of Activity per Day', fontsize=15)
plt.ylabel('Minutes of Activity', fontsize=12)
plt.xticks(rotation=45)
plt.tick_params(bottom=False, top=False, left=False, right=False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.grid()
plt.show()
#This graph is a bit unclear, let's try to get a weeks cumulative number of move minutes

week_activity = []
week_start = []
for day in range(0, len(podaci['Date']), 7):
    week = podaci['Move Minutes count'][day:day+6].sum()
    week_activity.append(week)
    week_start.append(podaci['Date'][day])

fig = plt.figure(1, figsize=(6, 3))
fig.add_axes([0, 0, 1, 1])
ax = plt.gca()

plt.plot(week_start[:-1], week_activity[:-1], color='b')
plt.axhline(300, linestyle='--', color='r', label='300 minutes', linewidth=0.5)
plt.title('Minutes of Activity per Week', fontsize=15)
plt.ylabel('Minutes of Activity', fontsize=12)
plt.xticks(rotation=45)
plt.ylim(0, 1200)
plt.tick_params(bottom=False, top=False, left=False, right=False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.grid()
plt.show()

fig = plt.figure(figsize=(7,5))
plt.hist(podaci['Move Minutes count'], 7, alpha=0.3, color='b', edgecolor='b')
plt.xticks(range(0, 360, 60))
plt.title('Intervals in minutes', fontsize=15)
plt.ylabel('Number of days', fontsize=12)
plt.tick_params(bottom=False, top=False, left=False, right=False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.show()
#The large amount of days where I didn't move at all must be because of the 2019 part of the graph, I do not know why else would it be like that


#Now let's see how each of the days compares
days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
active_minutes_per_day_of_week = podaci.groupby('Day of Week')['Move Minutes count'].sum()
number_of_days = podaci['Day of Week'].value_counts()
for day in days_of_week:
    average_active_minutes_per_day_of_week = active_minutes_per_day_of_week // number_of_days

fig = plt.figure(figsize=(7,3))
plt.plot(range(7), average_active_minutes_per_day_of_week, color='b')
plt.ylabel('Activity in minutes', fontsize=12)
plt.title('Average active Minutes per Day of Week', fontsize=15)
plt.xticks(range(7), days_of_week, rotation=45)
plt.yticks(range(0, 160, 20))
plt.tick_params(bottom=False, top=False, left=False, right=False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.show()

podaci['Walking duration (min)'].describe()
podaci['Distance (m)'].describe()


plt.plot(podaci['Date'], podaci['Step count'], color='b')
plt.title('Number of Steps per Day', fontsize=15)
plt.ylabel('Number of Steps', fontsize=12)
plt.axhline(10000, linestyle='--', color='r', label = '10 000 steps', linewidth=0.5)
plt.xticks(rotation=45)
plt.tick_params(bottom=False, top=False, left=False, right=False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.legend(loc='upper left', fontsize=12)
plt.show()


viseod10000 = sum(podaci['Step count']>10000)
print('{}%'.format(viseod10000/640*100))
#I went over the goal of 10000 steps in 62.5% of cases ! That's pretty good


plt.plot(podaci['Date'], podaci['Heart Points'], color='b')
plt.title('Number of heart points per day', fontsize=15)
plt.ylabel('Heart points', fontsize=12)
plt.xticks(rotation=45)
plt.tick_params(bottom=False, top=False, left=False, right=False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.legend(loc='upper left', fontsize=12)
plt.show()
#I see that the graphs for heart points and steps are pretty similar, let's see how they corelate with each other 

podaci['Day of Week'] = podaci['Day of Week'].astype('category')
podaci.describe(include='category')
list(podaci.columns)
sns.scatterplot(x="Step count", y="Heart Points", data=podaci)
sns.lmplot(x="Step count", y="Heart Points", data=podaci)

#With this we can see that there is a strong correlation between step count and heart points awarded