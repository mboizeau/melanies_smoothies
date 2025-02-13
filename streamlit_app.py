# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
cnx =  st.connection("snowflake")

# Write directly to the app
st.title("Customize you SMOOTHIE!! :cup_with_straw:")
st.write(
    """Choose the fruits  you want 
    """
)
name_of_order  = st.text_input("Name on Smoothie")
st.write (f"Smoothie  on your smoothie wille be {name_of_order}")
#session = get_active_session()
session =  cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect("Choose up to  5 ingredients"
                                 ,my_dataframe,
                                 max_selections = 5)
if ingredients_list:
    ingredients_string = ""

    # Boucle for pour itérer sur chaque élément de la liste
    for ingredient in (ingredients_list):
        ingredients_string += ingredient +" " 
        st.subheader(ingredient + ' Nutrition info')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ingredient)
        sf_df =  st.dataframe(data  = smoothiefroot_response.json(), use_container_width = True)

    #st.write(", ".join(ingredients_list))
    #st.write(ingredients_string)
    #st.text(ingredients_list)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" +name_of_order+"""')"""
    #st.write(my_insert_stmt)
    time_to_insert =  st.button ('submit Order')
    #st.stop()
    if time_to_insert    :
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_of_order}!', icon="✅")

