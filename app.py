import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')




years = [
    1896, 1900, 1904, 1908, 1912, 1920, 1924, 1928, 1932, 1936,
    1948, 1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1984,
    1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016
]

df = df[df['Year'].isin(years)]


df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
image_path = "blue-gf531a3d9a_1920-670x474.jpg"
st.sidebar.image(image_path, use_column_width=True)
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].nunique() 
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()
    st.title("Top Statistics")
    columns = st.columns(3)
    with columns[0]:
        st.header("Editions")
        st.title(editions)
    with columns[1]:
        st.header("Hosts")
        st.title(cities)
    with columns[2]:
        st.header("Sports")
        st.title(sports)

    columns = st.columns(3)
    with columns[0]:
        st.header("Events")
        st.title(events)
    with columns[1]:
        st.header("Nations")
        st.title(nations)
    with columns[2]:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df)
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)
    
    events_over_time = helper.event_over_time(df)
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.ath_over_time(df)
    fig = px.line(athlete_over_time, x="Edition", y="Name", labels={"Name": "Number of Athletes"})
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)
    
    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

if user_menu == 'Athlete wise Analysis':
      
    
    # Assuming df is your DataFrame and is already loaded
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    
    # Create DataFrame for age distributions
    age_distribution = pd.DataFrame({
        'Overall Age': athlete_df['Age'].dropna(),
        'Gold Medalist': athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna(),
        'Silver Medalist': athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna(),
        'Bronze Medalist': athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    })
    
    # Melt DataFrame to long format
    age_distribution_melted = age_distribution.melt(var_name='Category', value_name='Age')
    
    # Plot overall age distribution
    fig = px.line(age_distribution_melted, x=age_distribution_melted.index, y='Age', color='Category')
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)
    
    # Creating age distribution per sport for gold medalists
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming', 'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball', 'Archery', 'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball', 'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        if not temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna().empty:
            x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna().tolist())
            name.append(sport)
    
    # Create DataFrame for sports age distribution
    sports_age_distribution = pd.DataFrame({
        'Age': [item for sublist in x for item in sublist],
        'Sport': [sport for sport, ages in zip(name, x) for _ in ages]
    })
    
    # Plot age distribution by sport
    fig = px.line(sports_age_distribution, x=sports_age_distribution.index, y='Age', color='Sport')
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports (Gold Medalist)")
    st.plotly_chart(fig)
    
    # Men vs Women participation over the years
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    
    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
    # athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # x1 = athlete_df['Age'].dropna()
    # x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    # x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    # x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    # fig = ff.px.line([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    # fig.update_layout(autosize=False,width=1000,height=600)
    # st.title("Distribution of Age")
    # st.plotly_chart(fig)

    # x = []
    # name = []
    # famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
    #                  'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
    #                  'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
    #                  'Water Polo', 'Hockey', 'Rowing', 'Fencing',
    #                  'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
    #                  'Tennis', 'Golf', 'Softball', 'Archery',
    #                  'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
    #                  'Rhythmic Gymnastics', 'Rugby Sevens',
    #                  'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    # for sport in famous_sports:
    #     temp_df = athlete_df[athlete_df['Sport'] == sport]
    #     x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
    #     name.append(sport)

    # fig = px.line(x, name, show_hist=False, show_rug=False)
    # fig.update_layout(autosize=False, width=1000, height=600)
    # st.title("Distribution of Age wrt Sports(Gold Medalist)")
    # st.plotly_chart(fig)

    # sport_list = df['Sport'].unique().tolist()
    # sport_list.sort()
    # sport_list.insert(0, 'Overall')

    # st.title("Men Vs Women Participation Over the Years")
    # final = helper.men_vs_women(df)
    # fig = px.line(final, x="Year", y=["Male", "Female"])
    # fig.update_layout(autosize=False, width=1000, height=600)
    # st.plotly_chart(fig)

    
   
  
  
   

    
