from flask import Flask, render_template, request
import pymysql.cursors
import pandas as pd 
import numpy as np
import bokeh.plotting as plt
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import HoverTool
import bokeh.plotting as bp

app = Flask(__name__)

# Connect with mysql database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='031218',
                             db='prac',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `xom`"
        cursor.execute(sql)
        df = pd.DataFrame(cursor.fetchall())
        df['Date'] = pd.to_datetime(df['Date'])

finally:
        connection.close()

feature_names = df.columns.values
feature_names = feature_names[feature_names != 'Date']

time = df['Date'].values
time = time.astype(str)
df['date_formatted'] = time

def create_figure(current_feature_name):

    hover = HoverTool(tooltips=[
    	('Price', '$y'),
    ])
    
    TOOLS = [hover, 'pan', 'wheel_zoom', 'box_zoom', 'reset', 'save']

    p = plt.figure(tools = TOOLS, title=current_feature_name, x_axis_label='Date', y_axis_label='Price', x_axis_type="datetime", width=1300, height=500, toolbar_location="above")
    p.line(df['Date'], df[current_feature_name], line_width=2)

    return(p)


@app.route("/")
def sample_table():

    current_feature_name = request.args.get("feature_name")
    if current_feature_name == None:
       current_feature_name = "Open"

    # Create the plot and generate html code 
    plot = create_figure(current_feature_name)

    script, div = components(plot)
    return render_template('index.html', script=script, div=div, feature_names=feature_names,  current_feature_name=current_feature_name)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)






