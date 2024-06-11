import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image


#DataFrame Creation

#Table for SQL Creation

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      password="postgres",
                      database="phone_pe",
                      port="5432")
cursor=mydb.cursor()

#agg_insurance_df
cursor.execute("SELECT * FROM agg_transaction")
mydb.commit()
table1=cursor.fetchall()

Agg_Insurance=pd.DataFrame(table1, columns=("States","Years","Quarter","Transaction_Type","Transaction_count","Transaction_Amount"))

#agg_transaction_df
cursor.execute("SELECT * FROM agg_transaction")
mydb.commit()
table2=cursor.fetchall()

Agg_Transaction=pd.DataFrame(table2, columns=("States","Years","Quarter","Transaction_Type","Transaction_count","Transaction_Amount"))

#agg_user_df
cursor.execute("SELECT * FROM agg_user")
mydb.commit()
table3=cursor.fetchall()

Agg_User=pd.DataFrame(table3, columns=("States","Years","Quarter","Brands","Transaction_count","Percentage"))


#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

Map_Insurance=pd.DataFrame(table4, columns=("States","Years","Quarter","District","Transaction_count","Transaction_Amount"))

#map_transaction_df
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()

Map_Transaction=pd.DataFrame(table5, columns=("States","Years","Quarter","District","Transaction_count","Transaction_Amount"))

#map_user_df
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

Map_User=pd.DataFrame(table6, columns=("States","Years","Quarter","Districts","RegisteredUser","AppOpens"))

#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

Top_Insurance=pd.DataFrame(table7, columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_Amount"))

#top_transaction_df
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

Top_Transaction=pd.DataFrame(table8, columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_Amount"))

#top_user_df
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

Top_User=pd.DataFrame(table9, columns=("States","Years","Quarter","Pincodes","RegisteredUsers"))



def Transaction_amount_count_Year(df,  year):
    Trans=df[df["Years"]==year]
    Trans.reset_index(drop=True, inplace=True)


    transG=Trans.groupby("States")[["Transaction_count","Transaction_Amount"]].sum()
    transG.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_Amount=px.bar(transG, x="States", y="Transaction_Amount",  title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,  height=650,width=600)
        st.plotly_chart(fig_Amount)

    with col2:
        fig_Count=px.bar(transG, x="States", y="Transaction_count",  title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset, height=650,width=600)
        st.plotly_chart(fig_Count)


    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response=requests.get(url)
        data1=json.loads(response.content)

        state_name=[]
        for features in data1["features"]:
            state_name.append(features["properties"]["ST_NM"])
        state_name.sort()

        fig_ind_map1=px.choropleth(transG, geojson=data1, locations="States", featureidkey="properties.ST_NM", 
                                color= "Transaction_Amount", color_continuous_scale= "ylgnbu", 
                                range_color=(transG["Transaction_Amount"].min(), transG["Transaction_Amount"].max()),
                                hover_name="States", title=f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600,width=600)
        
        
        fig_ind_map1.update_geos(visible=False)
        st.plotly_chart(fig_ind_map1)


    with col2:
        fig_ind_map2=px.choropleth(transG, geojson=data1, locations="States", featureidkey="properties.ST_NM", 
                                color= "Transaction_count", color_continuous_scale= "ylgnbu", 
                                range_color=(transG["Transaction_count"].min(), transG["Transaction_count"].max()),
                                hover_name="States", title=f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height=600,width=600)
        
        
        fig_ind_map2.update_geos(visible=False)
        st.plotly_chart(fig_ind_map2)

    return Trans

def Transaction_amount_count_Year_Quarter(df,  quarter):
    Trans=df[df["Quarter"]==quarter]
    Trans.reset_index(drop=True, inplace=True)


    transG=Trans.groupby("States")[["Transaction_count","Transaction_Amount"]].sum()
    transG.reset_index(inplace=True)


    col1,col2=st.columns(2)
    with col1:
        fig_Amount=px.bar(transG, x="States", y="Transaction_Amount",  title=f"{Trans['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
        st.plotly_chart(fig_Amount)


    with col2:
        fig_Count=px.bar(transG, x="States", y="Transaction_count",  title=f"{Trans['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=600)
        st.plotly_chart(fig_Count)

    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response=requests.get(url)
        data1=json.loads(response.content)

        state_name=[]
        for features in data1["features"]:
            state_name.append(features["properties"]["ST_NM"])
        state_name.sort()

        fig_ind_map1=px.choropleth(transG, geojson=data1, locations="States", featureidkey="properties.ST_NM", 
                                color= "Transaction_Amount", color_continuous_scale= "ylgnbu", 
                                range_color=(transG["Transaction_Amount"].min(), transG["Transaction_Amount"].max()),
                                hover_name="States", title=f"{Trans['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600,width=600)
        
        
        fig_ind_map1.update_geos(visible=False)
        st.plotly_chart(fig_ind_map1)

    with col2:
        fig_ind_map2=px.choropleth(transG, geojson=data1, locations="States", featureidkey="properties.ST_NM", 
                                color= "Transaction_count", color_continuous_scale= "ylgnbu", 
                                range_color=(transG["Transaction_count"].min(), transG["Transaction_count"].max()),
                                hover_name="States", title=f"{Trans['Years'].min ()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                height=600,width=600)
        
        
        fig_ind_map2.update_geos(visible=False)
        st.plotly_chart(fig_ind_map2)

    return Trans


def Agg_Tran_Tras_Type(df, state):

    Trans=df[df["States"]==state]
    Trans.reset_index(drop=True, inplace=True)
    Trans
    transG=Trans.groupby("Transaction_Type")[["Transaction_count","Transaction_Amount"]].sum()
    transG.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_pie_A=px.pie(data_frame=transG, names="Transaction_Type", values="Transaction_Amount", 
                        width=600, title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.7)

        st.plotly_chart(fig_pie_A)

    with col2:
        fig_pie_B=px.pie(data_frame=transG, names="Transaction_Type", values="Transaction_count", 
                        width=600, title=f"{state.upper()}TRANSACTION AMOUNT", hole=0.7)

        st.plotly_chart(fig_pie_B)


#Aggre_User_Type
def Agg_User_Plot(df, year):
    tra_Agg_user=df[df["Years"]==year]
    tra_Agg_user.reset_index(drop=True, inplace=True)
    tra_Agg_user  

    tra_Agg_user_G=pd.DataFrame(tra_Agg_user.groupby("Brands")["Transaction_count"].sum())
    tra_Agg_user_G.reset_index(inplace=True)

    fig_bar_A=px.bar(tra_Agg_user_G, x="Brands", y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=800, color_discrete_sequence=px.colors.sequential.Jet, hover_name="Brands")

    st.plotly_chart(fig_bar_A)

    return tra_Agg_user

#Aggre_User_Type_2
def Agg_User_Plot_2(df, quarter):
    tra_Agg_user_Quarter=df[df["Quarter"]==quarter]
    tra_Agg_user_Quarter.reset_index(drop=True, inplace=True)

    tra_Agg_user_Quarter_group=pd.DataFrame(tra_Agg_user_Quarter.groupby("Brands")["Transaction_count"].sum())
    tra_Agg_user_Quarter_group.reset_index(inplace=True)

    fig_bar_A=px.bar(tra_Agg_user_Quarter_group, x="Brands", y="Transaction_count", title= f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width=800, color_discrete_sequence=px.colors.sequential.Jet, hover_name="Brands")

    st.plotly_chart(fig_bar_A)

    return tra_Agg_user_Quarter

#Aggre_User_Type_3
def Agg_User_Plot_3(df, state):
    Agg_user_year_Q_S=df[df ["States"]== state]
    Agg_user_year_Q_S.reset_index(drop=True, inplace=True)

    fig_Line_A=px.line(Agg_user_year_Q_S, x= "Brands", y= "Transaction_count", hover_data= "Percentage",
                    title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE", width=800, markers=True)
    st.plotly_chart(fig_Line_A)

#Map_Inssurance_district
def tra_Map_Insurance_District(df, state):

    Trans=df[df["States"]==state]
    Trans.reset_index(drop=True, inplace=True)

    transG=Trans.groupby("District")[["Transaction_count","Transaction_Amount"]].sum()
    transG.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_A=px.bar(transG, x= "Transaction_Amount", y= "District", orientation="h", height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Mint_r)

        st.plotly_chart(fig_bar_A)

    with col2:
        fig_bar_B=px.bar(transG, x= "Transaction_count", y= "District", orientation="h", height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_B)

# Map_User_Plot_1
def Map_User_Plot_1(df, year):
    tra_Map_user=df[df["Years"]==year]
    tra_Map_user.reset_index(drop=True, inplace=True) 

    tra_Map_user_G=tra_Map_user.groupby("States")[["RegisteredUser","AppOpens"] ].sum()
    tra_Map_user_G.reset_index(inplace=True)

    fig_Line_A=px.line(tra_Map_user_G, x= "States", y= ["RegisteredUser","AppOpens"],
                    title= f"{year} REGISTERED USER, APPOPENS", width=800,height=750, markers=True)
    st.plotly_chart(fig_Line_A)

    return tra_Map_user


# Map_User_Plot_2
def Map_User_Plot_2(df, quarter):
    tra_Map_user_Quarter=df[df["Quarter"]==quarter]
    tra_Map_user_Quarter.reset_index(drop=True, inplace=True) 

    tra_Map_user_Year_G=tra_Map_user_Quarter.groupby("States")[["RegisteredUser","AppOpens"] ].sum()
    tra_Map_user_Year_G.reset_index(inplace=True)

    fig_Line_B=px.line(tra_Map_user_Year_G, x= "States", y= ["RegisteredUser","AppOpens"],
                    title= f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTERED USER, APPOPENS", width=800,height=750, markers=True,
                    color_discrete_sequence=px.colors.sequential.Bluyl)
    st.plotly_chart(fig_Line_B)
    
    return tra_Map_user_Quarter


# Map_User_Plot_3
def Map_User_Plot_3(df, states):
    tra_Map_user_Quarter_State=df[df["States"]==states]
    tra_Map_user_Quarter_State.reset_index(drop=True, inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_map_user_bar_1=px.bar(tra_Map_user_Quarter_State, x= "RegisteredUser", y= "Districts", orientation="h",
                                title= f"{states.upper()} REGISTERED USER", height=1000, color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2=px.bar(tra_Map_user_Quarter_State, x= "AppOpens", y= "Districts", orientation="h",
                                title= f"{states.upper()} APPOPENS", height=1000, color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)

# Top_Insurance_Plot_1
def Top_Insurance_Plot_1(df, state):
    tra_Top_Insurance_State=df[df["States"]==state]
    tra_Top_Insurance_State.reset_index(drop=True, inplace=True) 

    tra_Top_Insurance_State_G=tra_Top_Insurance_State.groupby("Pincodes")[["Transaction_count","Transaction_Amount"] ].sum()
    tra_Top_Insurance_State_G.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_top_insurance_bar_1=px.bar(tra_Top_Insurance_State, x= "Quarter", y= "Transaction_Amount", hover_data="Pincodes",
                                title= "TRANSACTION AMOUNT", height=650, width=600,color_discrete_sequence=px.colors.sequential.Sunsetdark)
        st.plotly_chart(fig_top_insurance_bar_1)

    with col2:
        fig_top_insurance_bar_2=px.bar(tra_Top_Insurance_State, x= "Quarter", y= "Transaction_count", hover_data="Pincodes",
                                title= "TRANSACTION AMOUNT", height=650, width=600, color_discrete_sequence=px.colors.sequential.Sunsetdark)
        st.plotly_chart(fig_top_insurance_bar_2)

def Top_User_Plot_1(df, year):    
    tra_Top_User=df[df["Years"]==year]
    tra_Top_User.reset_index(drop=True, inplace=True)

    tra_Top_User_G=pd.DataFrame(tra_Top_User.groupby(["States", "Quarter"])["RegisteredUser"].sum())
    tra_Top_User_G.reset_index(inplace=True)
    tra_Top_User_G

    fig_Top_plot_1= px.bar(tra_Top_User_G, x= "States", y= "RegisteredUser", color= "Quarter", width= 600, height=650,
                        color_discrete_sequence=px.colors.sequential.Viridis, hover_name= "States",
                        title=f"{year} REGISTERED USER")
    st.plotly_chart(fig_Top_plot_1)

    return tra_Top_User


# Top_User_Plot_2
def Top_User_Plot_2(df, state):
    tra_Top_user_State=df[df["States"]== state]
    tra_Top_user_State.reset_index(drop=True, inplace=True)

    fig_Top_plot_2= px.bar(tra_Top_user_State, x= "Quarter", y= "RegisteredUser", title= "REGISTERED USER, PINCODES, QUARTER",
                        width=800, height=650, color= "RegisteredUser", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Hot_r)
    st.plotly_chart(fig_Top_plot_2)

#Table for SQL Creation

def Top_Chart_transaction_Amount(table_name):
        mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="postgres",
                        database="phone_pe",
                        port="5432")
        cursor=mydb.cursor()

        #query1
        query1= f'''SELECT States, SUM(Transaction_Amount) AS Transaction_Amount
                        FROM {table_name}
                        GROUP BY states
                        ORDER BY Transaction_Amount DESC
                        LIMIT 10;'''

        cursor.execute(query1)
        table_1=cursor.fetchall()
        mydb.commit()

        df_1=pd.DataFrame(table_1, columns=("States", "Transaction_Amount"))
        df_1

        col1,col2=st.columns(2)
        with col1:
            fig_Amount=px.bar(df_1, x="States", y="Transaction_Amount",  title= "TOP 10 OF TRANSACTION AMOUNT", hover_name="States",  
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
            st.plotly_chart(fig_Amount)

        #query2
        query2= f'''SELECT states, SUM(Transaction_Amount) AS Transaction_Amount
                        FROM {table_name}
                        GROUP BY states
                        ORDER BY Transaction_Amount
                        LIMIT 10;'''

        cursor.execute(query2)
        table_2=cursor.fetchall()
        mydb.commit()

        with col2:
            df_2=pd.DataFrame(table_2, columns=("States", "Transaction_Amount"))

            fig_Amount_B=px.bar(df_2, x="States", y="Transaction_Amount",  title= "LAST 10 OF TRANSACTION AMOUNT", hover_name="States",  
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
            st.plotly_chart(fig_Amount_B)


        #query3
        query3= f'''SELECT States, AVG(Transaction_Amount) AS Transaction_Amount
                        FROM {table_name}
                        GROUP BY States
                        ORDER BY Transaction_Amount;'''

        cursor.execute(query3)
        table_3=cursor.fetchall()
        mydb.commit()

        df_3=pd.DataFrame(table_3, columns=("States", "Transaction_Amount"))

        fig_Amount_C=px.bar(df_3, x="Transaction_Amount", y="States",  title= "AVERAGE OF TRANSACTION AMOUNT", hover_name="States", orientation="h", 
                        color_discrete_sequence=px.colors.sequential.Bluered, height=800, width=1000)
        st.plotly_chart(fig_Amount_C)

#Table for SQL Creation

def Top_Chart_transaction_count(table_name):
        mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="postgres",
                        database="phone_pe",
                        port="5432")
        cursor=mydb.cursor()

        #query1
        query1= f'''SELECT States, SUM(Transaction_count) AS Transaction_count
                        FROM {table_name}
                        GROUP BY states
                        ORDER BY Transaction_count DESC
                        LIMIT 10;'''

        cursor.execute(query1)
        table_1=cursor.fetchall()
        mydb.commit()

        df_1=pd.DataFrame(table_1, columns=("States", "Transaction_count"))

        col1,col2=st.columns(2)
        with col1:
            fig_Amount=px.bar(df_1, x="States", y="Transaction_count",  title= "TOP 10 OF TRANSACTION COUNT", hover_name="States",  
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
            st.plotly_chart(fig_Amount)

        #query2
        query2= f'''SELECT states, SUM(Transaction_count) AS Transaction_count
                        FROM {table_name}
                        GROUP BY states
                        ORDER BY Transaction_count
                        LIMIT 10;'''

        cursor.execute(query2)
        table_2=cursor.fetchall()
        mydb.commit()

        df_2=pd.DataFrame(table_2, columns=("States", "Transaction_count"))

        with col2:
            fig_Amount_B=px.bar(df_2, x="States", y="Transaction_count",  title= "LAST 10 OF TRANSACTION COUNT", hover_name="States",  
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
            st.plotly_chart(fig_Amount_B)

        #query3
        query3= f'''SELECT States, AVG(Transaction_count) AS Transaction_count
                        FROM {table_name}
                        GROUP BY States
                        ORDER BY Transaction_count;'''

        cursor.execute(query3)
        table_3=cursor.fetchall()
        mydb.commit()

        df_3=pd.DataFrame(table_3, columns=("States", "Transaction_count"))

        fig_Amount_C=px.bar(df_3, y="States", x="Transaction_count",  title= "AVERAGE OF TRANSACTION COUNT", hover_name="States", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered, height=650, width=600)
        st.plotly_chart(fig_Amount_C)


#Table for SQL Creation
def Top_Chart_Regustered_User(table_name, state):
        mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="postgres",
                        database="phone_pe",
                        port="5432")
        cursor=mydb.cursor()

        #query1
        query1= f'''SELECT Districts, SUM(RegisteredUser) AS RegisteredUser
                        From {table_name}
                        where states = '{state}'
                        GROUP BY Districts
                        ORDER BY RegisteredUser DESC
                        LIMIT 10;'''

        cursor.execute(query1)
        table_1=cursor.fetchall()
        mydb.commit()

        df_1=pd.DataFrame(table_1, columns=("Districts", "RegisteredUser"))

        col1,col2=st.columns(2)
        with col1:
            fig_Amount=px.bar(df_1, x="Districts", y="RegisteredUser",  title= "TOP 10 OF REGISTERED USER", hover_name="Districts",  
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
            st.plotly_chart(fig_Amount)

        #query2
        query2= f'''SELECT Districts, SUM(RegisteredUser) AS RegisteredUser
                        From {table_name}
                        where states = '{state}'
                        GROUP BY Districts
                        ORDER BY RegisteredUser
                        LIMIT 10;'''

        cursor.execute(query2)
        table_2=cursor.fetchall()
        mydb.commit()

        df_2=pd.DataFrame(table_2, columns=("Districts", "RegisteredUser"))

        with col2:
                fig_Amount_B=px.bar(df_2, x="Districts", y="RegisteredUser",  title= "LAST 10 OF REGISTERED USER", hover_name="Districts",  
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
                st.plotly_chart(fig_Amount_B)


        #query3
        query3= f'''SELECT Districts, AVG(RegisteredUser) AS RegisteredUser
                        From {table_name}
                        where states = '{state}'
                        GROUP BY Districts
                        ORDER BY RegisteredUser;'''

        cursor.execute(query3)
        table_3=cursor.fetchall()
        mydb.commit()

        df_3=pd.DataFrame(table_3, columns=("Districts", "RegisteredUser"))

        fig_Amount_C=px.bar(df_3, y="Districts", x="RegisteredUser",  title= "AVERAGE OF REGISTERED USER", hover_name="Districts", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered, height=650, width=600)
        st.plotly_chart(fig_Amount_C)

#Table for SQL Creation
def Top_Chart_AppOpens(table_name, state):
        mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="postgres",
                        database="phone_pe",
                        port="5432")
        cursor=mydb.cursor()

        #query1
        query1= f'''SELECT Districts, SUM(AppOpens) AS AppOpens
                        From {table_name}
                        where states = '{state}'
                        GROUP BY Districts
                        ORDER BY AppOpens DESC
                        LIMIT 10;'''

        cursor.execute(query1)
        table_1=cursor.fetchall()
        mydb.commit()

        df_1=pd.DataFrame(table_1, columns=("Districts", "AppOpens"))

        col1,col2=st.columns(2)
        with col1:
            fig_Amount=px.bar(df_1, x="Districts", y="AppOpens",  title= "TOP 10 OF APPOPENS", hover_name="Districts",  
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
            st.plotly_chart(fig_Amount)

        #query2
        query2= f'''SELECT Districts, SUM(AppOpens) AS AppOpens
                        From {table_name}
                        where states = '{state}'
                        GROUP BY Districts
                        ORDER BY AppOpens
                        LIMIT 10;'''

        cursor.execute(query2)
        table_2=cursor.fetchall()
        mydb.commit()

        df_2=pd.DataFrame(table_2, columns=("Districts", "AppOpens"))

        with col2:
            fig_Amount_B=px.bar(df_2, x="Districts", y="AppOpens",  title= "LAST 10 OF APPOPENS", hover_name="Districts",  
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
            st.plotly_chart(fig_Amount_B)


        #query3
        query3= f'''SELECT Districts, AVG(AppOpens) AS AppOpens
                        From {table_name}
                        where states = '{state}'
                        GROUP BY Districts
                        ORDER BY AppOpens;'''

        cursor.execute(query3)
        table_3=cursor.fetchall()
        mydb.commit()

        df_3=pd.DataFrame(table_3, columns=("Districts", "AppOpens"))

        fig_Amount_C=px.bar(df_3, y="Districts", x="AppOpens",  title= "AVERAGE OF APPOPENS", hover_name="Districts", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered, height=650, width=600)
        st.plotly_chart(fig_Amount_C)

#Table for SQL Creation

def Top_Chart_Top_Users(table_name):
        mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="postgres",
                        database="phone_pe",
                        port="5432")
        cursor=mydb.cursor()

        #query1
        query1= f'''SELECT States, SUM(RegisteredUsers) AS RegisteredUsers
                        From {table_name}
                        GROUP BY States
                        ORDER BY RegisteredUsers DESC
                        LIMIT 10;'''

        cursor.execute(query1)
        table_1=cursor.fetchall()
        mydb.commit()

        df_1=pd.DataFrame(table_1, columns=("States", "RegisteredUsers"))

        col1,col2=st.columns(2)
        with col1:
            fig_Amount=px.bar(df_1, x="States", y="RegisteredUsers",  title= "TOP 10 OF TOP USER", hover_name="States",  
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
            st.plotly_chart(fig_Amount)

        #query2
        query2= f'''SELECT States, SUM(RegisteredUsers) AS RegisteredUsers
                        From {table_name}
                        GROUP BY States
                        ORDER BY RegisteredUsers
                        LIMIT 10;'''

        cursor.execute(query2)
        table_2=cursor.fetchall()
        mydb.commit()

        df_2=pd.DataFrame(table_2, columns=("States", "RegisteredUsers"))

        with col2:
            fig_Amount_B=px.bar(df_2, x="States", y="RegisteredUsers",  title= "LAST 10 OF TOP USER", hover_name="States",  
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
            st.plotly_chart(fig_Amount_B)


        #query3
        query3= f'''SELECT States, AVG(RegisteredUsers) AS RegisteredUsers
                        From {table_name}
                        GROUP BY States
                        ORDER BY RegisteredUsers;'''

        cursor.execute(query3)
        table_3=cursor.fetchall()
        mydb.commit()

        df_3=pd.DataFrame(table_3, columns=("States", "RegisteredUsers"))

        fig_Amount_C=px.bar(df_3, y="States", x="RegisteredUsers",  title= "AVERAGE OF TOP USER", hover_name="States", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered, height=650, width=600)
        st.plotly_chart(fig_Amount_C)


#Streamlit Part

st.set_page_config(layout= "wide")
st.title("PHONPE DATA VISUALISATION AND EXPLORATION")

with st.sidebar:

    select=option_menu("MAIN MENU",["HOME","DATA EXPLORTION","TOP CHARTS"])

if select== "HOME":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
  
    with col2:
        st.video(r"C:\Users\dell\phonepe\PhonePe - Introduction(720P_HD).mp4")

    col3,col4= st.columns(2)
    
    with col3:
        st.video(r"C:\Users\dell\phonepe\PhonePe Motion Graphics in After Effects _ Naveen Shiva Sai _ Student Works(720P_HD).mp4")

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.video(r"C:\Users\dell\phonepe\PhonePe Motion Graphics(720P_HD).mp4")


elif select== "DATA EXPLORTION":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:

        method=st.radio("SELECT THE MEthOD",["Aggregated Insurance","Aggregated Transaction","Aggregated User"])

        if method=="Aggregated Insurance":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider('SELECT THE YEAR',Agg_Insurance["Years"].min(),  Agg_Insurance["Years"].max(), Agg_Insurance["Years"].min())
            tra_Y= Transaction_amount_count_Year(Agg_Insurance,  years)

            col1,col2= st.columns(2)
            with col1:

                quarters=st.slider('SELECT THE QUARTER',tra_Y["Quarter"].min(),  tra_Y["Quarter"].max(), tra_Y["Quarter"].min())

            tra_Agg_tra_Quarter= Transaction_amount_count_Year_Quarter(tra_Y,  quarters)


        elif method=="Aggregated Transaction":
            
            col1,col2=st.columns(2)
            with col1:

                years=st.slider('SELECT THE YEAR',Agg_Transaction["Years"].min(),  Agg_Transaction["Years"].max(), Agg_Transaction["Years"].min())
            tra_Agg_tra= Transaction_amount_count_Year(Agg_Transaction,  years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("SELECT THE STATE", tra_Agg_tra["States"].unique())

            Agg_Tran_Tras_Type(tra_Agg_tra, states)


            col1,col2= st.columns(2)
            with col1:

                quarters=st.slider('SELECT THE QUARTER',tra_Agg_tra["Quarter"].min(),  tra_Agg_tra["Quarter"].max(), tra_Agg_tra["Quarter"].min())
            tra_Agg_tra_Quarter=Transaction_amount_count_Year_Quarter(tra_Agg_tra, quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("SELECT THE STATE_TY", tra_Agg_tra_Quarter["States"].unique())

            Agg_Tran_Tras_Type(tra_Agg_tra_Quarter, states)

        elif method=="Aggregated User":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider('SELECT THE YEAR',Agg_User["Years"].min(),  Agg_User["Years"].max(), Agg_User["Years"].min())
            Agg_user_year= Agg_User_Plot(Agg_User, years)


            col1,col2= st.columns(2)
            with col1:

                quarters=st.slider('SELECT THE QUARTER',Agg_user_year["Quarter"].min(),  Agg_user_year["Quarter"].max(), Agg_user_year["Quarter"].min())
            Agg_user_year_Quarter=Agg_User_Plot_2(Agg_user_year, quarters)


            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("SELECT THE STATE", Agg_user_year_Quarter["States"].unique())

            Agg_User_Plot_3(Agg_user_year_Quarter, states)
    
    with tab2:

        method_B=st.radio("SELCET THE METHOS",["Map Insurance","Map Transaction","Map User"])

        if method_B=="Map Insurance":
          col1,col2=st.columns(2)
          with col1:

                years=st.slider('SELECT THE YEAR_MI',Map_Insurance["Years"].min(),  Map_Insurance["Years"].max(), Map_Insurance["Years"].min())
          tra_Map_Insurance_Year= Transaction_amount_count_Year(Map_Insurance,  years)  

          col1,col2=st.columns(2)
          with col1:
            states=st.selectbox("SELECT THE STATE_MI", tra_Map_Insurance_Year["States"].unique())

            tra_Map_Insurance_District(tra_Map_Insurance_Year, states)


          col1,col2= st.columns(2)
          with col1:

                quarters=st.slider('SELECT THE QUARTER_MI',tra_Map_Insurance_Year["Quarter"].min(),  tra_Map_Insurance_Year["Quarter"].max(), tra_Map_Insurance_Year["Quarter"].min())
          tra_Map_Insurance_Year_Quarter=Transaction_amount_count_Year_Quarter(tra_Map_Insurance_Year , quarters)


          col1,col2=st.columns(2)
          with col1:
                states=st.selectbox("SELECT THE STATE_TY", tra_Map_Insurance_Year_Quarter["States"].unique())

          tra_Map_Insurance_District(tra_Map_Insurance_Year_Quarter, states)
   

        elif method_B=="Map Transaction":
          col1,col2=st.columns(2)
          with col1:

                years=st.slider('SELECT THE YEAR_MT',Map_Transaction["Years"].min(),  Map_Transaction["Years"].max(), Map_Transaction["Years"].min())
          tra_Map_Transaction_Year= Transaction_amount_count_Year(Map_Transaction,  years)  

          col1,col2=st.columns(2)
          with col1:
            states=st.selectbox("SELECT THE STATE_MT", tra_Map_Transaction_Year["States"].unique())

            tra_Map_Insurance_District(tra_Map_Transaction_Year, states)


          col1,col2= st.columns(2)
          with col1:

                quarters=st.slider('SELECT THE QUARTER_MT',tra_Map_Transaction_Year["Quarter"].min(),  tra_Map_Transaction_Year["Quarter"].max(), tra_Map_Transaction_Year["Quarter"].min())
          tra_Map_Transaction_Year_Quarter=Transaction_amount_count_Year_Quarter(tra_Map_Transaction_Year , quarters)


          col1,col2=st.columns(2)
          with col1:
                states=st.selectbox("SELECT THE STATE_TY", tra_Map_Transaction_Year_Quarter["States"].unique())

          tra_Map_Insurance_District(tra_Map_Transaction_Year_Quarter, states)

        
        
        elif method_B=="Map User":
           col1,col2=st.columns(2)
           with col1:

                years=st.slider('SELECT THE YEAR_MU',Map_User["Years"].min(),  Map_User["Years"].max(), Map_User["Years"].min())
           tra_Map_User_Year= Map_User_Plot_1(Map_User,  years)

           
           col1,col2= st.columns(2)
           with col1:

                quarters=st.slider('SELECT THE QUARTER_MU',tra_Map_User_Year["Quarter"].min(),  tra_Map_User_Year["Quarter"].max(), tra_Map_User_Year["Quarter"].min())
           tra_Map_User_Year_Quarter=Map_User_Plot_2(tra_Map_User_Year , quarters)

           
           col1,col2=st.columns(2)
           with col1:
                    states=st.selectbox("SELECT THE STATE_MU", tra_Map_User_Year_Quarter["States"].unique())

           Map_User_Plot_3(tra_Map_User_Year_Quarter, states)
        

    with tab3:

        method_C=st.radio("SELCET THE METHOS",["Top Insurance","Top Transaction","Top User"])

        if method_C=="Top Insurance":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider('SELECT THE YEAR_TI',Top_Insurance["Years"].min(),  Top_Insurance["Years"].max(), Top_Insurance["Years"].min())
            tra_Top_Insurance_Year= Transaction_amount_count_Year(Top_Insurance,  years)

            col1,col2= st.columns(2)
            with col1:

                quarters=st.slider('SELECT THE QUARTER_TI',tra_Top_Insurance_Year["Quarter"].min(),  tra_Top_Insurance_Year["Quarter"].max(), tra_Top_Insurance_Year["Quarter"].min())
            tra_Top_Insurance_Year_Quarter=Transaction_amount_count_Year_Quarter(tra_Top_Insurance_Year , quarters)

            col1,col2=st.columns(2)
            with col1:
                    states=st.selectbox("SELECT THE STATE_TI", tra_Top_Insurance_Year["States"].unique())

            Top_Insurance_Plot_1(tra_Top_Insurance_Year, states)
     

        elif method_C=="Top Transaction":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider('SELECT THE YEAR_TT',Top_Transaction["Years"].min(),  Top_Transaction["Years"].max(), Top_Transaction["Years"].min())
            tra_Top_Transaction_Year= Transaction_amount_count_Year(Top_Transaction,  years)

            col1,col2= st.columns(2)
            with col1:

                quarters=st.slider('SELECT THE QUARTER_TT',tra_Top_Transaction_Year["Quarter"].min(),  tra_Top_Transaction_Year["Quarter"].max(), tra_Top_Transaction_Year["Quarter"].min())
            tra_Top_Transaction_Year_Quarter=Transaction_amount_count_Year_Quarter(tra_Top_Transaction_Year , quarters)

            col1,col2=st.columns(2)
            with col1:
                    states=st.selectbox("SELECT THE STATE_TT", tra_Top_Transaction_Year["States"].unique())

            Top_Insurance_Plot_1(tra_Top_Transaction_Year, states)
     

        elif method_C=="Top User":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider('SELECT THE YEAR_TT',Top_User["Years"].min(),  Top_User["Years"].max(), Top_User["Years"].min())
            tra_Top_User_Year= Top_User_Plot_1(Top_User,  years)

            col1,col2=st.columns(2)
            with col1:
                    states=st.selectbox("SELECT THE STATE_TT", tra_Top_User_Year["States"].unique())

            Top_User_Plot_2(tra_Top_User_Year, states)


elif select== "TOP CHARTS":
    
    question= st.selectbox("SELECT THE QUESTION",["1. Transaction Amount and Count of Aggregrated Insurance",
                                                  "2. Transaction Amount and Count of Map Insurance",
                                                  "3. Transaction Amount and Count of Top Insurance",
                                                  "4. Transaction Amount and Count of Aggregrated Transaction",
                                                  "5. Transaction Amount and Count of Map Transaction",
                                                  "6. Transaction Amount and Count of Top Transaction",
                                                  "7. Transaction Amount and Count of Aggregrated User",
                                                  "8. Registered User of Map User",
                                                  "9. AppOpens User of Map User",
                                                  "10. Registered User of Top User"])
    

    if question== "1. Transaction Amount and Count of Aggregrated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_transaction_Amount("agg_insurance")
   
        st.subheader("TRANSACTION COUNT")    
        Top_Chart_transaction_count("agg_insurance")


    elif question== "2. Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_transaction_Amount("map_insurance")
   
        st.subheader("TRANSACTION COUNT")    
        Top_Chart_transaction_count("map_insurance")

    
    elif question== "3. Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_transaction_Amount("top_insurance")
   
        st.subheader("TRANSACTION COUNT")    
        Top_Chart_transaction_count("top_insurance")


    elif question== "4. Transaction Amount and Count of Aggregrated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_transaction_Amount("agg_transaction")
   
        st.subheader("TRANSACTION COUNT")    
        Top_Chart_transaction_count("agg_transaction")


    elif question== "5. Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_transaction_Amount("map_transaction")
   
        st.subheader("TRANSACTION COUNT")    
        Top_Chart_transaction_count("map_transaction")

    
    elif question== "6. Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_transaction_Amount("top_transaction")
   
        st.subheader("TRANSACTION COUNT")    
        Top_Chart_transaction_count("top_transaction")

    
    elif question== "7. Transaction Amount and Count of Aggregrated User":

        st.subheader("TRANSACTION COUNT")    
        Top_Chart_transaction_count("agg_user") 

     
    elif question== "8. Registered User of Map User":

        states=st.selectbox("Select The State", Map_User["States"].unique())
        st.subheader("REGISTERED USER")
        Top_Chart_Regustered_User("map_user", states)  


    elif question== "9. AppOpens User of Map User":

        states=st.selectbox("Select The State", Map_User["States"].unique())
        st.subheader("APPOPENS")
        Top_Chart_AppOpens("map_user", states)  

    
    elif question== "10. Registered User of Top User":

        st.subheader("TOP USER")
        Top_Chart_Top_Users("top_user")
    
