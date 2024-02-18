import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)
#------------------------------------------------------------------------------------------------
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)
#______________________________________________________________________________________________
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3, gap='medium')
    with col1:
        st.subheader("Editions")
        st.title(editions)
    with col2:
        st.subheader("Hosts")
        st.title(cities)
    with col3:
        st.subheader("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3, gap='medium')
    with col1:
        st.subheader("Events")
        st.title(events)
    with col2:
        st.subheader("Nations")
        st.title(nations)
    with col3:
        st.subheader("Athletes")
        st.title(athletes)

    region_over_time = helper.data_over_time(df, 'region')
    fig = px.line(region_over_time, x="Year", y="region count")
    fig.update_layout(
        xaxis=dict(showgrid=True, gridcolor='lightgrey'),  # Add grid to x-axis with light grey color
        yaxis=dict(showgrid=True, gridcolor='lightgrey'),  # Add grid to y-axis with light grey color
    )
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    Event_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(Event_over_time, x="Year", y="Event count")
    fig.update_layout(
        xaxis=dict(showgrid=True, gridcolor='lightgrey'),  # Add grid to x-axis with light grey color
        yaxis=dict(showgrid=True, gridcolor='lightgrey'),  # Add grid to y-axis with light grey color
    )
    st.title("Events over the years")
    st.plotly_chart(fig)

    Name_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(Name_over_time, x="Year", y="Name count")
    fig.update_layout(
        xaxis=dict(showgrid=True, gridcolor='lightgrey'),  # Add grid to x-axis with light grey color
        yaxis=dict(showgrid=True, gridcolor='lightgrey'),  # Add grid to y-axis with light grey color
    )
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    st.title("No. of Events over time(Every Sport)")
    if (len(x) > 0):
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
        st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    st.table(helper.most_successful(df, selected_sport))
#______________________________________________________________________________________________
if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    pt = helper.country_event_heatmap(df, selected_country)
    st.title(selected_country + " excels in the following sports")
    if(len(pt) > 0):
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)
    else:
        st.write("No athlete won any medal")

    st.title("Top athletes of " + selected_country)
    st.table(helper.most_successful_countrywise(df, selected_country))
#-----------------------------------------------------------------------------------------
if user_menu == 'Athlete wise Analysis':
    """athlete_df = df.drop_duplicates(subset=['Name', 'region', 'Year'])
    athlete_df = athlete_df.dropna(subset=['Medal'])

    x1 = athlete_df['Age']
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age']
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age']
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age']

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=500)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming', 'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball', 'Archery', 'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball', 'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=500)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)
    """
    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=800, height=500)
    st.plotly_chart(fig)
    

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    temp_df = temp_df.dropna(subset=['Height', 'Weight'])
    if(len(temp_df) == 0):
        st.write("No Complete Info")
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)


    import plotly.graph_objects as go

    athlete_df = df.drop_duplicates(subset=['Name', 'region', 'Year'])
    athlete_df = athlete_df.dropna(subset=['Medal'])

    x1 = athlete_df['Age']
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age']
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age']
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age']

    # Create Histogram traces
    hist1 = go.Histogram(x=x1, name='Overall Age', opacity=1)
    hist2 = go.Histogram(x=x2, name='Gold Medalist', opacity=0.5)
    hist3 = go.Histogram(x=x3, name='Silver Medalist', opacity=0.5)
    hist4 = go.Histogram(x=x4, name='Bronze Medalist', opacity=0.5)

    # Create figure object
    fig = go.Figure(data=[hist1, hist2, hist3, hist4])

    # Update layout
    fig.update_layout(autosize=False, width=800, height=500, barmode='overlay', title='Distribution of Age')
    fig.update_traces(marker_line_width=0)

    # Show plot using Streamlit
    st.plotly_chart(fig)