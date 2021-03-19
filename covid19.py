# Python Project – COVID-19 Spread Analysis with Flask
# Load the dataset and collect the top 15 regions having the largest corona cases
#import pandas as pd
#corona_df = pd.read_csv('dataset.csv')
#by_country = corona_df.groupby('Country_Region').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
#n = 15
# cdf = by_country.nlargest(n, 'Confirmed')[['Confirmed']]

# Function that will return the updated data frame
def find_top_confirmed(n = 15):

  import pandas as pd
  corona_df = pd.read_csv('dataset.csv')
  by_country = corona_df.groupby('Country_Region').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
  cdf = by_country.nlargest(n, 'Confirmed')[['Confirmed']]
  return cdf

cdf=find_top_confirmed()
pairs=[(Country_Region,confirmed) for Country_Region,confirmed in zip(cdf.index,cdf['Confirmed'])]


# Make a sample map using the folium package and write a function to make circles on active corona cases regions
import folium
import pandas as pd
corona_df = pd.read_csv('dataset.csv')

corona_df=corona_df.dropna()

m=folium.Map(location=[34.223334,-82.461707],
            tiles='Stamen toner',
            zoom_start=8)

def circle_maker(x):
    folium.Circle(location=[x[0],x[1]],
                 radius=float(x[2])*10,
                 color="red",
                 popup='{}\n confirmed cases:{}'.format(x[3],x[2])).add_to(m)
corona_df[['Lat','Long_','Confirmed','Combined_Key']].apply(lambda x:circle_maker(x),axis=1)

html_map=m._repr_html_()

# Now do the required settings for flask app
from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html",table=cdf, cmap=html_map,pairs=pairs)

if __name__ == '__main__':
    app.run(debug=True)

# Now create two HTML pages inside templates folder: base.html and home.html and paste the below code in it
