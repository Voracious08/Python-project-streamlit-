import pandas as pd
import json 
from urllib.request import urlopen
import plotly.express as px
import streamlit as st
import time
from PIL import Image
import streamlit.components.v1 as components

# Formatting tiitle ---------------------------/-
st.markdown("<h1 style='text-align: center; '>CHHATTISGARH COVID  MAP</h1>", unsafe_allow_html=True)
st.markdown('  ')
st.markdown('  ')



# optimizing the dataframe-------------------/-

@st.cache
def df_open():
	df =pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv',usecols = ["District", "Confirmed", "Active","Recovered","Deceased"],nrows = 148)
	df=df[119:146]
	df.loc[120,"District"] = "Baloda-Bazar"
	df.loc[126,"District"] = "Dakshin-Bastar-Dantewada"
	df.loc[145,"District"] =  "Uttar-Bastar-Kanker"
	df.loc[122,"District"] =  "Bemetra"
	df.loc[130,"District"] =  "Janjgir-Champa"
	df.rename(columns = {"District" :"Dist_Name" }, inplace = True)
	return(df)




# Adding sidebar to the app ------------/-

selected_df = df_open()['Dist_Name'].tolist()
selected_option = st.sidebar.selectbox( "Search your district ", selected_df)

@st.cache
def some_function2():
	dict_req = {'Balod':119, 'Baloda-Bazar':120,'Balrampur':121,'Bemetra':122,'Bastar':123,'Bijapur':124,'Bilaspur':125,'Dakshin-Bastar-Dantewada':126,
	'Dhamtari':127,'Durg':128,'Gariaband':129,'Janjgir-Champa':130,'Jashpur':131,'Kabeerdham':132,'Kondagaon':133,'Korba':134,'Koriya':135,
	'Mahasamund':136,'Mungeli':137,'Narayanpur':138,'Raigarh':139,'Raipur':140,'Rajnandgaon':141,'Sukma':142,'Surajpur':143,'Surguja':144,'Uttar-Bastar-Kanker':145}
	return(dict_req)



for i in some_function2():
	if(i==selected_option):
		req_index = some_function2()[i]
		break;



# Displaying row from table --------------/-

st.table( df_open().loc[[req_index]])



@st.cache
def cgdf_open():
	df1 = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
	return(df1)



st.sidebar.markdown (" <h3> TOTAL CASES </h3>" , unsafe_allow_html = True)
st.sidebar.markdown(cgdf_open().loc[18, "Confirmed"])
st.sidebar.markdown (" <h3> RECOVERED </h3>" , unsafe_allow_html = True)
st.sidebar.markdown(cgdf_open().loc[18,"Recovered"])
st.sidebar.markdown (" <h3> ACTIVE </h3>" , unsafe_allow_html = True)
st.sidebar.markdown(cgdf_open().loc[18,"Active"])
st.sidebar.markdown (" <h3> DEATHS </h3>" , unsafe_allow_html = True)
st.sidebar.markdown(cgdf_open().loc[18,"Deaths"])
st.sidebar.markdown('       ')
st.sidebar.markdown('<H4> LAST UPDATED </H4>', unsafe_allow_html = True)
st.sidebar.markdown(cgdf_open().loc[18, "Last_Updated_Time"])




# Optimizing the geojson file---------------/-



@st.cache
def geojson_open():

	with urlopen('https://raw.githubusercontent.com/shklnrj/IndiaStateTopojsonFiles/master/Chhattisgarh.geojson')as response:
	    geojson = json.load(response)
	    geojson["features"][6]["properties"]["Dist_Name"] = "Uttar-Bastar-Kanker"
	    geojson["features"][17]["properties"]["Dist_Name"] = "Baloda-Bazar"
	    geojson["features"][22]["properties"]["Dist_Name"] = "Dakshin-Bastar-Dantewada"
	    return(geojson)







# Displaying the map and adjusting the layout-------------/-



fig = px.choropleth(data_frame = df_open() ,geojson = geojson_open() ,locations = 'Dist_Name', featureidkey = 'properties.Dist_Name',color = 'Confirmed',
	      hover_name = 'Dist_Name' , hover_data = {'Confirmed':True,'Dist_Name':False, 'Active':True, 'Deceased':True},  projection = "mercator" ,color_continuous_scale="Reds", labels = {  'Dist_Name': 'District'})

fig.update_geos(fitbounds="locations", visible = False , showframe = True, framecolor = '#210606', framewidth =2,bgcolor = '#6F6C5E',
		showland = False,showlakes = True)

fig.update_layout(margin={"r":250,"t":40,"l":80,"b":80, "autoexpand" : False}  , modebar = { "orientation":'h',
	 "bgcolor": '#E0414C' , "color": ' #1F2525', "activecolor": '#FFF2F3'}, hovermode = 'closest', hoverlabel = {"bgcolor": '#FEFBFB',
	   "bordercolor": '#FB1616', "font" : {"family": 'Times New Roman', "color":'#322F2F', "size": 15}  }, width = 750, height = 510)

st.plotly_chart(fig)




@st.cache 
def anotherdf():
	data = [['March', 9], ['April', 31], ['May', 458], ['June', 2360], ['July',6334], ['August',22311], ['September', 67062]]
	df = pd.DataFrame(data , columns = [ 'Month', 'Cases'])
	return(df)
fig1 = px.bar(data_frame = anotherdf() , x = "Month", y = "Cases", color = "Cases", hover_data = ["Cases"], text = "Cases",
	color_continuous_scale = "Portland")

fig1.update_layout(title = { "text": " Rise in Cases By Month ", "xref": "paper", "yref": "paper", "x":0.5 , "font": {"color": '#1A1717'}}, paper_bgcolor = '#D6D6D6'
		, plot_bgcolor = '#D6D6D6', hoverlabel={"bordercolor": '#EBEEEE'}, margin={"pad" :2}, width =700 , height = 400, font ={'color':'#191616'})


st.plotly_chart(fig1,use_container_width = True)

st.text('     ')
st.text('     ')
st.text('     ')
st.markdown("<h2 style='text-align: center; color: red;'>List of covid Health centres</h2>", unsafe_allow_html=True)
st.text('     ')
st.text('     ')
st.text('     ')
image = Image.open('hospitals_list.jpg')
st.image(image,use_column_width = True)
st.markdown("<h1 style='text-align: center;'>Poll</h1>", unsafe_allow_html=True)
st.markdown('   ')
components.iframe("https://www.opinionstage.com/api/v1/widgets/746208/iframe", height = 450, width = 450)
components.iframe("https://www.opinionstage.com/api/v1/widgets/746254/iframe", height = 420, width = 450)




