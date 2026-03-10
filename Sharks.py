import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv('Shark_tank.csv')

################################### Investor Details #######################333


# Function for calculating the total amount invested by an individual shark
def func(name):
    return df[name].sum()

# Function for calculating the total equity bought by an individual shark

def fun1(name) :
    L = ['Ashneer Investment Equity', 'Namita Investment Equity', 'Anupam Investment Equity', 'Aman Investment Equity',
         'Peyush Investment Equity' , 'Ghazal Investment Equity', 'Amit Investment Equity','Vineeta Investment Equity']

    for i in L :
        if name == i[:-18] :
            return df[i].sum()

def fun2(name):
    return df[df[name]>0].count()[1]

def fun3(name):
    k = ' Debt Amount'
    return df[name+k].sum()

def load_investor(name) :
    st.title(name)
    col1 , col2 , col3 , col4= st.columns(4)
    with col1 :
        amt = func(name)
        st.metric('Total Investment',str(round(float(amt/10),2))+' M')

    with col2 :
        eqt = fun1(name)
        st.metric('Total Equity bought',str(round(float(eqt) , 2))+'%')

    with col3 :
        total = fun2(name)
        st.metric('Invested In ',str(total)+' Companies')

    with col4 :
        debt = fun3(name)
        st.metric('Total Debt',str(round(float(debt/10) , 2))+' M')

    st.markdown("<h2 style='text-align: center;'>Top 5 Biggest Investments</h2>", unsafe_allow_html=True)
    col1 , col2 = st.columns(2)

    with col1:

        new = ' Investment Equity'
        big = df[df[name]>0][[name,'Industry','Startup Name',name+new]].reset_index(drop = True).sort_values(by=name,ascending = False).head(5)
        st.dataframe(big )

        k = df.groupby('Industry')[name].sum().reset_index().sort_values(by = name , ascending =False).head(5)
        k = k[k[name] > 0].sort_values(by=name).reset_index(drop=True)

        fig , ax = plt.subplots(figsize = (8,6))
        ax.pie(k[name],labels = k['Industry'],autopct = '%0.2f%%',textprops={'fontsize': 7})
        plt.title('Top 5 Industry wise Investment')
        st.pyplot(fig)

    with col2:
        fig , ax = plt.subplots(figsize =(5,5.2))
        sns.barplot(x = big['Startup Name'],y=big[name] , ax = ax,palette='Set1' )
        plt.xticks(fontsize=12, rotation=90)
        plt.yticks(fontsize=8)
        plt.ylabel('Investment Amount (in lakhs)')
        st.pyplot(fig)

    st.subheader('Season Wise Investment')
    fig , ax = plt.subplots(figsize=(5,2))
    sns.barplot(x = df['Season Number'] , y=df[name] , ax = ax , estimator = 'sum',palette="Set1",ci=None)
    plt.ylabel('Amount (lakhs)')
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    st.pyplot(fig)


############################## Startup Details ######################3


def load_Startup(start):
    st.title(start)
    d = df[df['Startup Name']==start]['Business Description'].reset_index(drop=True)[0]
    st.text(f"A business which deals in - '{d}'")

    col1 , col2 , col3 , col4 = st.columns(4)

    with col1 :
        amt = df[df['Startup Name']==start]['Original Ask Amount'].reset_index(drop=True)[0]
        st.metric('Amount Requested',str(amt/10)+ ' M')

    with col2 :
        amt2 = df[df['Startup Name']== start ]['Total Deal Amount'].reset_index(drop=True)[0]
        st.metric('Amount Recieved' , str(amt2/10)+' M')

    with col3 :
        eqt1 = df[df['Startup Name']== start ]['Original Offered Equity'].reset_index(drop=True)[0]
        st.metric('Equity Offered',str(eqt1)+'%')

    with col4 :
        eqt2 = df[df['Startup Name']== start ]['Total Deal Equity'].reset_index(drop=True)[0]
        st.metric('Equity bought',str(eqt2)+'%')


    st.subheader('Presenters Info ')
    col1 ,col2 ,col3 , col4=st.columns(4)
    with col1 :
        male = df[df['Startup Name']== start ]['Male Presenters']
        st.metric('No. of Males',int(male))

    with col2:
        female = df[df['Startup Name'] == start]['Female Presenters']
        st.metric('No. of Females', int(female))

    with col3 :
        trans = df[df['Startup Name'] == start]['Transgender Presenters']
        st.metric('No. of Trangenders', int(trans))

    with col4 :
        avg = df[df['Startup Name'] == start]['Pitchers Average Age'].reset_index(drop = True)[0]
        st.metric("Pitcher's Avg Age" , str(avg))

    st.subheader(f"Sharks Invested in {start} are :")
    e = df[df['Startup Name'] == start]

    S = ['Ashneer', 'Namita', 'Anupam', 'Aman', 'Vineeta', 'Peyush', 'Ghazal', 'Amit']
    p = 1
    for i in S:
        r = e[i].reset_index(drop=True)[0]
        if r > 0:
            st.text(f'{p}. {i} invested {r / 10} M')
            p = p +1
    if p == 1 :
        st.text(f"{start} didn't got investment from Sharks")

############################  Overall Analysis ##########################333

def load_all():
    select = st.selectbox('Select Season',['Season 1' , 'Season 2'])
    st.markdown(f"<h2 style='text-align: center;'>{select}</h2>", unsafe_allow_html=True)
    if select == 'Season 1' :
        d = df[df['Season Number']== 1]

    else :
        d = df[df['Season Number'] == 2]

    col1 , col2 , col3 , col4 = st.columns(4)

    with col1 :
        total = d['Startup Name'].count()
        st.metric('Startups Participated' , int(total))
    with col2 :
        deal = d['Accepted Offer'].sum()
        st.metric('Deal', int(deal))

    with col3 :
        no_deal = total - deal
        st.metric('No Deal',int(no_deal))

    with col4 :
        amt_total = d['Total Deal Amount'].sum()
        st.metric('Total Investment Amt',str(round(float(amt_total/10),2))+' M')


    col1 , col2 = st.columns(2)
    with col1 :
        st.subheader('Top 5 Biggest investment')
        max = d.sort_values(by='Total Deal Amount' , ascending = False)
        fig , ax = plt.subplots()
        sns.barplot(x='Startup Name' , y= 'Total Deal Amount' , data = max.head(5),ax=ax , palette='Set1'  )
        plt.xticks(rotation = 90 , fontsize = 9)
        st.pyplot(fig)

    with col2 :
        st.subheader('Top 5 Lowest Investments')
        min = d[d['Total Deal Amount']>0].sort_values(by = 'Total Deal Amount')
        fig, ax = plt.subplots()
        sns.barplot(x='Startup Name', y='Total Deal Amount', data=min.head(5), ax=ax, palette='Set1')
        plt.xticks(rotation=60, fontsize = 9)
        st.pyplot(fig)

    col1 , col2 = st.columns(2)

    with col1 :
        st.subheader('Top 5 No Bargain Deal')
        no_bar = d[(d['Original Ask Amount'] == d['Total Deal Amount']) &(d['Original Offered Equity']==d['Total Deal Equity'])][['Startup Name',\
        'Original Ask Amount','Original Offered Equity','Number of sharks in deal']].sort_values(by='Original Ask Amount',ascending=False).head(5)
        st.dataframe(no_bar)


    with col2 :
        st.subheader('Top 5 Sharky Deal')
        shark_deal = d[d['Total Deal Equity'] > d['Original Offered Equity']][['Startup Name','Original Offered Equity','Total Deal Equity',\
                        'Number of sharks in deal']].sort_values(by='Total Deal Equity',ascending = False).head(5)
        st.dataframe(shark_deal)

    st.markdown("<h2 style='text-align: center;'>Industry wise Investment Amount</h2>", unsafe_allow_html=True)
    fig,ax = plt.subplots(figsize=(10,3))
    sns.barplot(x=d['Industry'],y=d['Total Deal Amount'],palette = 'Set1', ax= ax , data =d , ci=None,estimator='sum')
    plt.xticks(rotation = 90 , fontsize =7)
    st.pyplot(fig)

selected = st.sidebar.selectbox('Select One' , ['Overall Analysis' , 'Investors' , 'Startups'])

if selected == 'Investors' :
    name = st.sidebar.selectbox('Select One',['Ashneer' , 'Namita' , 'Anupam' , 'Aman','Peyush'\
     , 'Ghazal' , 'Amit','Vineeta'] )

    btn = st.sidebar.button('Find Details')
    if btn :
        load_investor(name)
elif selected == 'Startups' :
    start = st.sidebar.selectbox('Select One',sorted(df['Startup Name']))
    btn1 = st.sidebar.button('Find Details')

    if btn1 :
        load_Startup(start)
else :
    load_all()


