import plotly.graph_objects as go
import pandas as pd

url='https://docs.google.com/spreadsheets/d/18X1VM1671d99V_yd-cnUI1j8oSG2ZgfU_q1HfOizErA/export?format=csv&id'
data=pd.read_csv(url)
data=data.fillna(0)

#trying to see the data.
data.head()

#SOME VARIABLES INITIATIONS
fig=go.Figure()
col_name=data.columns
n_col=len(data.columns)
date_list=[]
init=4
n_range=int((n_col-5)/2)

#LOOPING FOR DATA SPLITTING AND FIGURES 
for i in range(n_range):
    col_case=init+1
    col_dead=col_case+1
    init=col_case+1
    df_split=data[['latitude','longitude','country','location',col_name[col_case],col_name[col_dead]]]
    df=df_split[(df_split[col_name[col_case]]!=0)]
    lat=df['latitude']
    lon=df['longitude']
    case=df[df.columns[-2]].astype(int)
    deaths=df[df.columns[-1]].astype(int)
    df['text']=df['country']+'<br>'+df['location']+'<br>'+'confirmed cases: '+ case.astype(str)+'<br>'+'deaths: '+deaths.astype(str)
    date_label=deaths.name[7:17]
    date_list.append(date_label)
    
    #ADDING GEOSCATTER PLOT
    fig.add_trace(go.Scattergeo(
    name='',
    lon=lon,
    lat=lat,
    visible=False,
    hovertemplate=df['text'],
    text=df['text'],
    mode='markers',
    marker=dict(size=15,opacity=0.6,color='Red', symbol='circle'),
    ))

#SLIDER PART
steps = []
for i in range(len(fig.data)):
    step = dict(
        method="restyle",
        args=["visible", [False] * len(fig.data)],
        label=date_list[i],
    )
    step["args"][1][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)
    
sliders = [dict(
    active=0,
    currentvalue={"prefix": "Date: "},
    pad={"t": 1},
    steps=steps
)]

#SET FIRST FIGURE VISIBLE
fig.data[0].visible=True

#SHOW THE FIGURE
fig.update_layout(sliders=sliders,title='Coronavirus Spreading Map'+'<br>geodose.com',height=600)
fig.show()