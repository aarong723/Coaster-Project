"""
Programmed by Aaron Gold
May 5th 2023
Data: Roller Coaster Database
This project allows for the user to view data about roller coasters in the United States via graphs and pivot tables,
and receive recommendations for coasters to try, as well as see reviews from 'celebrities' about coasters.
"""

import pandas as pd
import streamlit as st
from PIL import Image
import textwrap
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns


#Intro page for website
def welcomePage():
    st.header("_Navigate through the ups and downs of roller coaster parks!_")
    image = Image.open('kingda_ka.jpg')
    st.image(image, caption='Kingda Ka: Tallest roller coaster in the world')


#Creating a bar graph of the 10 tallest roller coasters, color-coded by state
def heightBarGraph(height_tuple_set):
    st.title(":blue[_Tallest Roller Coasters_]")
    height_items_printed = 0
    xs, ys = [], []
    for tup in height_tuple_set:
        if height_items_printed < 10:
            ys.append(tup[1])
            xs.append(tup[0])
            height_items_printed += 1
    wrapped_labels = [textwrap.fill(label, width=11) for label in ys]
    plt.bar(wrapped_labels, xs, width=0.5, color=["coral", "aquamarine", "fuchsia", "coral", "gold", "aquamarine",
                                                  "royalblue", "fuchsia", "coral", "coral"], edgecolor='black')
    plt.xlabel("Roller Coaster", fontweight='bold')
    plt.ylabel("Maximum Height(ft)", fontweight='bold')
    plt.title("10 Tallest Roller Coasters in the world", fontsize=26, fontweight='bold')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.xticks(fontsize=8, rotation=45)
    legend = {'California': 'aquamarine', 'Ohio': 'coral', 'North Carolina': 'fuchsia',
              'Texas': 'gold', 'New Jersey': 'royalblue'}
    labels = list(legend.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=legend[label]) for label in labels]
    for i, v in enumerate(xs):
        plt.text(i, v+3, str(v), ha='center', fontsize=7)
    plt.legend(handles, labels, title="States", prop={'size': 7})
    plt.ylim(top=450)
    st.pyplot()
    st.caption("This chart shows the 10 tallest roller coasters in the United States")
    for i in range(6):
        st.write("")
    dragster_image = Image.open("Top_thrill_dragster.jpg")
    st.image(dragster_image, caption='Top Thrill Dragster: Tallest roller coaster in the United States')


#Speed pie chart based on frequency of roller coasters in states
def stateGraph(df):
    st.title(":blue[_Frequency of Roller Coasters_]")
    count = (df['State'].value_counts())
    cols = ['lightcoral', 'teal', 'tomato', 'moccasin', 'blueviolet', 'pink', 'gold', 'springgreen',
            'saddlebrown', 'deepskyblue']
    plt.pie(count[0:10], labels=(count.index[0:10]), colors=cols, startangle=90, shadow=True, explode=[0.2, 0, 0, 0, 0,
                0, 0, 0, 0, 0], autopct='%1.1f%%')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    legend = {'TBD1': 'lightcoral', 'TBD2': 'teal', 'TBD3': 'tomato', 'TBD4': 'moccasin', 'TBD5': 'blueviolet',
              'TBD6': 'pink', 'TBD7': 'gold', 'TBD8': 'springgreen', 'TBD9': 'saddlebrown', 'TBD10': 'deepskyblue'}
    labels = list(legend.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=legend[label]) for label in labels]
    plt.title('10 States With Most Roller Coasters', fontweight='bold')
    plt.legend(handles, labels)
    plt.legend(title="States", bbox_to_anchor=(1.02, 1), prop={'size': 5})
    st.pyplot()
    st.caption("This chart shows the 10 states with the most roller coasters, demonstrated by percentages "
               "of coasters from total database")
    for i in range(6):
        st.write("")
    superman_image = Image.open('Superman_california.jpg')
    st.image(superman_image, caption='Superman the Escape: Biggest and fastest roller coaster in California')


#This graph shows the relationship between the maximum height and top speed of roller coasters
def heightSpeedCorrelation(height_and_speed_tuple_list):
    st.title(":blue[_Height and Speed Correlation_]")
    heights, speeds = [], []
    for i in range(len(height_and_speed_tuple_list)):
        if height_and_speed_tuple_list[i][0] > 0 and height_and_speed_tuple_list[i][1] > 0:
            heights.append(height_and_speed_tuple_list[i][1])
            speeds.append(height_and_speed_tuple_list[i][0])
    fig = plt.figure(figsize=(9, 7))
    plt.xlabel("Top Speed (mph)", fontweight='bold')
    plt.ylabel("Maximum Height(ft)", fontweight='bold')
    plt.title("Correlation Between Height and Speed", fontsize=26, fontweight='bold')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    df = pd.DataFrame(list(zip(heights, speeds)),
                      columns=['Max Height', 'Top Speed'])
    sns.scatterplot(data=df, x="Top Speed", y="Max Height", size="Max Height", hue="Max Height", sizes=(20, 200))
    st.pyplot(fig)
    st.caption("This chart shows the relationship between maximum height and top speed of roller coasters")
    for i in range(6):
        st.write("")
    hulk_image = Image.open("incredible_hulk.jpg")
    st.image(hulk_image, width=700, caption='The Incredible Hulk: Roller coaster at Universal in Orlando, Florida')


#Pivot tables that demonstrate the total coaster time per park and average speed per second by roller coaster
def speedPerSecond(df):
    st.title(":blue[_Specialized Data_]")
    st.header("_Maximize Roller Coaster Park Efficiency!_")
    st.subheader(":blue[Total Duration by Park]")
    df["Duration (seconds)"] = df["Duration"]
    total_duration_pivot = df.pivot_table(index=['Park', 'City', 'State'],
                           values=['Duration (seconds)'],
                           aggfunc='sum')
    total_duration_pivot = total_duration_pivot.sort_values(by=['Duration (seconds)'], ascending=False)
    st.write(total_duration_pivot)

    st.subheader(":blue[Average Speed by Coaster]")
    df["Feet per Second"] = df["Length"] / df["Duration"]
    speed_per_sec_pivot = df.pivot_table(index=['Coaster', 'Park', 'City', 'State'],
                                         values=['Feet per Second'])
    st.write(speed_per_sec_pivot)


#Map of all the roller coaster parks in the database
def coasterMap(df):
    st.title(":blue[_Roller Coaster Park Map_]")
    df = df.drop(columns=['Age_Group', 'Coaster', 'State', 'Type', 'Design', 'Year_Opened', 'Top_Speed',
                        'Max_Height', 'Drop', 'Length', 'Duration', 'Inversions', 'Num_of_Inversions'])
    view_state = pdk.ViewState(latitude=df['Latitude'].mean(), longitude=df['Longitude'].mean(), zoom=4, pitch=0)
    layer = pdk.Layer('ScatterplotLayer', data=df, get_position='[Longitude, Latitude]', get_radius=40000,
                      get_color=[20, 200, 255], elevation_scale=50,
                elevation_range=[0, 1000], pickable=True, extruded=True)
    tool_tip = {"html": "Amusement Park:<br/> <b>{Park}</b>", "style": {"backgroundColor": "deepskyblue",
                "color": "black", "edgecolor": 'black'}}
    coaster_map = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', initial_view_state=view_state,
                   layers=[layer], tooltip=tool_tip)
    st.pydeck_chart(coaster_map)


#Asks users for ideal speed, height, design, and states to give them roller coaster recommendations in giveRecs function
def coasterRec(state_list, design_list, dictionary):
    st.title(":blue[_Roller Coaster Recommendation_]")
    st.write("Let's find a roller coaster that's right for you!")
    st.write("How fast do you want the roller coaster to be in mph? ")
    speed = st.slider('Maximum speed:', 27.0, 120.0, 50.0)
    st.write("Your ideal speed is", str(speed), "mph")
    speed_calc = speed / 60

    st.write("How tall do you want the roller coaster to be in ft? ")
    height = st.slider('Maximum height:', 18.0, 420.0, 100.0)
    st.write("Your ideal height is", str(height), "ft")
    height_calc = height / 210

    st.write("Do you want inversions?")
    inversion_choices = ['Yes', 'No']
    inversion_input = st.radio("Select your choice: ", inversion_choices)
    inversion_input = inversion_input.lower()
    st.write("You've selected", inversion_input)

    if inversion_input == 'yes':
        inversion_points = 2
    else:
        inversion_points = 0
    design_choice_list = []
    unique_design_list = []
    for trick in design_list:
        if trick not in unique_design_list:
            unique_design_list.append(trick)
    unique_design_list = sorted(unique_design_list)
    st.write("Check all of the designs you would like to ride.")
    for design in range(len(unique_design_list)):
        design_checkbox = (st.checkbox(unique_design_list[design], key=f"checkbox_{design}"))
        if design_checkbox:
            design_choice_list.append(unique_design_list[design])
    design_points = len(design_choice_list)
    if design_points > 0:
        design_points = design_points / 2
        wants_inversion = 'Y'
    else:
        wants_inversion = 'N'

    total_calc = inversion_points + height_calc + speed_calc + design_points

    unique_state_list = []
    for state in state_list:
        if state not in unique_state_list:
            unique_state_list.append(state)
    unique_state_list = sorted(unique_state_list)
    state_choice_list = st.multiselect("Check all of the states you would like to ride a roller coaster in.",
                                   unique_state_list)
    st.write("You selected: ", ', '.join(state_choice_list))

    recommendation_button = st.button("Click for your roller coaster recommendation!", key="recommendation_button")
    if recommendation_button:
        st.write("Your capacity for adventure is", str(round(total_calc, 2)), "out of 10. Based on this, we have some"
                 " recommendations for you! :tada:")
        if inversion_points < 1:
            giveRecs(state_choice_list, float(speed), float(height), dictionary, round(total_calc, 2))
        else:
            giveRecs(state_choice_list, float(speed), float(height), dictionary, round(total_calc, 2),
                     wants_inversion)


#Personally most proud of this function. Give viewers recommendations for roller coasters based on data they input to
#coasterRec function
def giveRecs(chosen_states, chosen_speed, chosen_height, coaster_dict, adventure_input, inversion_preference='N'):
    rec_list, count_list = [], []
    max_speed = chosen_speed + 30
    min_speed = chosen_speed - 30
    max_height = chosen_height + 80
    min_height = chosen_height - 80

    if max_speed > 120:
        max_speed = 120
    if min_speed < 27:
        min_speed = 27
    if max_height > 420:
        max_height = 420
    if min_height < 18:
        min_height = 18
    if inversion_preference == 'Y':
        inversion_points = 4
    else:
        inversion_points = 0
    for pick in coaster_dict:

        if ((coaster_dict[pick][1] in chosen_states) and (inversion_preference == coaster_dict[pick][3]) and
            (float(coaster_dict[pick][6]) <= max_speed) and
                (float(coaster_dict[pick][6]) >= min_speed) and (float(coaster_dict[pick][5]) >= min_height) and
                (float(coaster_dict[pick][5]) <= max_height) and (float(coaster_dict[pick][6]) > 0) and
                (float(coaster_dict[pick][5])) and (len(coaster_dict[pick][3]) < 3)):
            adventure_score = (((coaster_dict[pick][4]) / 210) + ((coaster_dict[pick][5]) / 60)
                             + inversion_points)
            if adventure_score > adventure_input:
                adventure_dif = adventure_score - adventure_input
            else:
                adventure_dif = adventure_input - adventure_score
            if adventure_score > 0:
                adventure_score = round(adventure_score, 2)
                current_rec = (round(adventure_dif, 2), adventure_score, coaster_dict[pick][8], coaster_dict[pick][1],
                               coaster_dict[pick][0], coaster_dict[pick][3], coaster_dict[pick][4],
                               coaster_dict[pick][5], coaster_dict[pick][9])
                rec_list.append(current_rec)
    #Lambda function to sort list by adventure score (formula I created to evaluate coasters' danger/thrill)
    rec_list = sorted(rec_list, key=lambda x: x[0])
    count = 1
    for i in range(len(rec_list)):
        count_list.append(count)
        count += 1
    if len(rec_list) >= 1:
        max_recs = str(len(rec_list))
        st.subheader("Found " + max_recs + " coasters with your guidelines!")
        st.subheader(":blue[_Here are your roller coaster recommendations:_]")
        if current_rec[5] == "N":
            inversion_status = " does not have inversion(s),"
        else:
            inversion_status = " has inversion(s),"
        for rec in range(len(rec_list)):
            st.write(f":green[{str(int(rec + 1))}:]", f":blue[{rec_list[rec][4]}]", "at", f":orange[{rec_list[rec][8]}]"
                     , "in", f":orange[{str(rec_list[rec][2])}], ", f":orange[{rec_list[rec][3]}].", "It has a max"
                     " speed of", f":violet[{str(rec_list[rec][7])}]", "mph, a max height of",
                     f":violet[{str(rec_list[rec][6])}]", "ft,", f":red[{inversion_status}]", "and an adventure score"
                     " of", f":violet[{str(rec_list[rec][1])}]", ", just", f":violet[{str(rec_list[rec][0])}]",
                     "off from your score!")
    else:
        st.subheader("_Unfortunately, there are no roller coasters with these guidelines. Try again!_")


#Demonstrates made-up reviews of coasters. Allows for user to add a review to the site
def giveReview():
    st.title(":blue[_Coaster Reviews_]")

    st.subheader(":green[Top Thrill Dragster, Cedar Point Sandusky:] :orange[_4.8/5_]")
    st.write('''"_Had a great time, the speed is unmatched_"''''')
    kendrick_image = Image.open("kendrick_lamar.jpg")
    st.image(kendrick_image, caption="-Kendrick Lamar, California")
    for i in range(6):
        st.write("")

    st.subheader(":green[Whizzer, Six Flags Great America Illinois:] :orange[_2.1/5_]")
    st.write('''"_Incredibly slow and boring. Will not be coming back_"''''')
    brady_image = Image.open("brady.jpg")
    st.image(brady_image, caption="-Tom Brady, Florida")
    for i in range(6):
        st.write("")

    st.subheader(":green[Big Bad Wolf, Busch Gardens Virginia:] :orange[_3.7/5_]")
    st.write('''"_The suspended aspect of the coaster definitely made the ride so much fun!_"''''')
    selena_image = Image.open("selena.jpg")
    st.image(selena_image, caption="-Selena Gomez, Texas")
    for i in range(6):
        st.write("")

    st.subheader(":green[Superman The Escape, Six Flags Magic Mountain California:] :orange[_5/5_]")
    st.write('''"_I've been riding roller coasters for 50 years. This is easily the best roller coaster I've ever been 
             on_"''''')
    rock_image = Image.open("the_rock.jpg")
    st.image(rock_image, caption="-Dwayne 'The Rock' Johnson, Virginia")
    for i in range(6):
        st.write("")


#Creates dictionary and dataframe of all the items from an Excel file
def dictCreation():
    key_list = []
    coasterDict = {}
    pd.options.display.max_rows = 999
    df = pd.read_excel("RollerCoasters-Geo.xlsx")
    name_list = list(df['Coaster'])
    state_list = list(df['State'])
    city_list = list(df['City'])
    height_list = list(df['Max_Height'])
    speed_list = list(df['Top_Speed'])
    inversions_list = list(df['Inversions'])
    design_list = list(df['Design'])
    park_list = list(df['Park'])
    lat_list = list(df['Latitude'])
    long_list = list(df['Longitude'])
    #As no column had entirely unique values, I had to create a key by joining the roller coaster name, park name, and
    #state name. I assumed no park had the same roller coaster name and no state had parks with the same name
    for name in range(len(name_list)):
        new_key = str(name_list[name]) + '_' + str(park_list[name] + '_' + (str(state_list[name])))
        key_list.append(new_key)
    for key in range(len(key_list)):
        coasterDict[key_list[key]] = (name_list[key], state_list[key], design_list[key], inversions_list[key],
                                      float(height_list[key]), float(speed_list[key]), float(lat_list[key]),
                                      float(long_list[key]), city_list[key], park_list[key])
    return df, coasterDict, state_list, design_list, name_list


#Creates tuples of keys with heights, speed, and both to make graphing simpler
def dictToOrderedReversedTuples(coaster_dict):
    tupleHeightList, tuple_height_speed_list = [], []
    for i in range(len(coaster_dict)):
        tupleKey = list(coaster_dict.keys())[i]
        tupleName = list(coaster_dict.values())[i][0]
        tupleHeight = list(coaster_dict.values())[i][4]
        tupleSpeed = list(coaster_dict.values())[i][5]
        tupleHeightSet = (float(tupleHeight), tupleName, tupleKey)
        tuple_height_speed_set = (float(tupleSpeed), float(tupleHeight), tupleKey)
        tuple_height_speed_list.append(tuple_height_speed_set)
        tupleHeightList.append(tupleHeightSet)

    tupleHeightList = [tup for tup in tupleHeightList if tup[0] > 0]
    tuple_height_speed_list = [tup for tup in tuple_height_speed_list if tup[0] > 0]
    tupleHeightList = sorted(tupleHeightList, key=lambda x: x[0], reverse=True)
    tuple_height_speed_list = sorted(tuple_height_speed_list, key=lambda x: x[0], reverse=True)
    return tupleHeightList, tuple_height_speed_list


def main():
    df, dictionary, list_states, list_design, names_list = dictCreation()
    height_tuples, speed_and_height_tuple_list = dictToOrderedReversedTuples(dictionary)
    with st.sidebar:
        menu_select = st.selectbox('Prompt:', ('Welcome Page', 'Coasters by State', 'Tallest Coasters',
                            'Height and Speed Correlation', 'Get a Recommendation', 'Reviews', 'Roller Coaster Map',
                            'Specified Coaster Analysis'))
    if menu_select == 'Welcome Page':
        welcomePage()
    if menu_select == 'Coasters by State':
        stateGraph(df)
    elif menu_select == "Tallest Coasters":
        heightBarGraph(height_tuples)
    elif menu_select == 'Height and Speed Correlation':
        heightSpeedCorrelation(speed_and_height_tuple_list)
    elif menu_select == "Get a Recommendation":
     coasterRec(list_states, list_design, dictionary)
    elif menu_select == "Reviews":
        giveReview()
    elif menu_select == 'Roller Coaster Map':
        coasterMap(df)
    elif menu_select == 'Specified Coaster Analysis':
        speedPerSecond(df)


main()
