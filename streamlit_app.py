# Import python packages
import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Reste Ye Pylgrimme! :cup_with_straw:")
st.write("An Blended and Moste Frozen Concoction awaites. Beholde thy choyces:")


cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)

pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    ingredients_string=''

    time_to_insert = st.button('Submit Order')
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie Is Ordered, '+name_on_order+'!', icon="✅")
        ingredients_list=[]
        name_on_order=None





