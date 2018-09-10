import pandas as pd
from analysis import analysis
from bokeh.plotting import figure, curdoc
from bokeh.models import LabelSet
from bokeh.layouts import column,row
from bokeh.client import push_session, pull_session
from bokeh.models.widgets import Select
from bokeh.io import show
import pickle

def update_plot(attrname, old, new):    
    rootLayout = curdoc().get_model_by_name('mainLayout')
    listOfSubLayouts = rootLayout.children
    plotToRemove = curdoc().get_model_by_name('plot')
    drop = curdoc().get_model_by_name('extra')
    if plotToRemove!=None:
        listOfSubLayouts.remove(plotToRemove)
    if drop!=None:
        listOfSubLayouts.remove(drop)    
    
    if dropdown.value=="Overall Analysis":
        data=pickle.load(open("overall.pkl", 'rb'))
        data_plot=data[dropdown_sub.value]
        x=list(data_plot.keys())
        y=list(data_plot.values())
        p = figure(name='plot',title=dropdown.value+"-"+dropdown_sub.value,toolbar_location='right',x_range=x, plot_width=750, plot_height=500)
        p.vbar(x,top=y,width=0.15,color='grey')
        p.xaxis.axis_label = 'Options'
        p.yaxis.axis_label = 'Fractions'
        listOfSubLayouts.append(p)

    elif dropdown.value=="Statewise Analysis":
        data=pickle.load(open("statwise.pkl", 'rb'))
        dropdown_sub_region.update(options=list(data.keys()))
        listOfSubLayouts.insert(1,dropdown_sub_region)
        data_plot=data[dropdown_sub_region.value][dropdown_sub.value]
        x=list(data_plot.keys())
        y=list(data_plot.values())
        p = figure(name='plot',title=dropdown.value+"-"+dropdown_sub_region.value+"-"+dropdown_sub.value,toolbar_location='right',x_range=x, plot_width=750, plot_height=500)
        p.vbar(x,top=y,width=0.15,color='grey')
        p.xaxis.axis_label = 'Options'
        p.yaxis.axis_label = 'Fractions'
        listOfSubLayouts.append(p)

    elif dropdown.value=="Qualification Analysis":
        data=pickle.load(open("qualificationwise.pkl", 'rb'))
        dropdown_sub_qualification.update(options=list(data.keys()))
        listOfSubLayouts.insert(1,dropdown_sub_qualification)
        data_plot=data[dropdown_sub_qualification.value][dropdown_sub.value]
        x=list(data_plot.keys())
        y=list(data_plot.values())
        p = figure(name='plot',title=dropdown.value+"-"+dropdown_sub_qualification.value+"-"+dropdown_sub.value,toolbar_location='right',x_range=x, plot_width=750, plot_height=500)
        p.vbar(x,top=y,width=0.15,color='grey')
        p.xaxis.axis_label = 'Options'
        p.yaxis.axis_label = 'Fractions'
        listOfSubLayouts.append(p)      

def update_plot_region(attrname, old, new):    
    rootLayout = curdoc().get_model_by_name('mainLayout')
    listOfSubLayouts = rootLayout.children
    plotToRemove = curdoc().get_model_by_name('plot')
    if plotToRemove!=None:
        listOfSubLayouts.remove(plotToRemove)
    
    if dropdown.value=="Statewise Analysis":
        data=pickle.load(open("statwise.pkl", 'rb'))
        data_plot=data[dropdown_sub_region.value][dropdown_sub.value]
        print(dropdown_sub_region.value)
        x=list(data_plot.keys())
        y=list(data_plot.values())
        p = figure(name='plot',title=dropdown.value+"-"+dropdown_sub_region.value+"-"+dropdown_sub.value,toolbar_location='right',x_range=x, plot_width=750, plot_height=500)
        p.vbar(x,top=y,width=0.15,color='grey')
        p.xaxis.axis_label = 'Options'
        p.yaxis.axis_label = 'Fractions'
        listOfSubLayouts.append(p)      

def update_plot_qualification(attrname, old, new):    
    rootLayout = curdoc().get_model_by_name('mainLayout')
    listOfSubLayouts = rootLayout.children
    plotToRemove = curdoc().get_model_by_name('plot')
    if plotToRemove!=None:
        listOfSubLayouts.remove(plotToRemove)
    if dropdown.value=="Qualification Analysis":
        data=pickle.load(open("qualificationwise.pkl", 'rb'))
        data_plot=data[dropdown_sub_qualification.value][dropdown_sub.value]
        x=list(data_plot.keys())
        y=list(data_plot.values())
        p = figure(name='plot',title=dropdown.value+"-"+dropdown_sub_qualification.value+"-"+dropdown_sub.value,toolbar_location='right',x_range=x, plot_width=750, plot_height=500)
        p.vbar(x,top=y,width=0.15,color='grey')
        p.xaxis.axis_label = 'Options'
        p.yaxis.axis_label = 'Fractions'
        listOfSubLayouts.append(p)      


#Name of the response file 
df=pd.read_csv("Alcohol Survey  (Responses) - Form Responses 1.csv")
analysis(df)

dropdown = Select(title="Analysis Type", value='overall', options=["Overall Analysis","Statewise Analysis","Qualification Analysis"])
dropdown.on_change('value',update_plot)
#initial plot
data=pickle.load(open("overall.pkl", 'rb'))
dropdown_sub= Select(title="Question", value=list(data.keys())[0], options=list(data.keys()))
dropdown_sub.on_change('value',update_plot)

dropdown_sub_region= Select(title="Region", value="Delhi", options=[" "," "," "],name='extra')
dropdown_sub_region.on_change('value',update_plot_region)

dropdown_sub_qualification= Select(title="Qualification", value="Basic Education", options=[" "," "," "],name='extra')
dropdown_sub_qualification.on_change('value',update_plot_qualification)


#list(data.keys())[0] --> first question
x=list(data[list(data.keys())[0]].keys())
y=list(data[list(data.keys())[0]].values())

p = figure(name='plot',title="Overall Analysis",toolbar_location='right',x_range=x, plot_width=750, plot_height=500)
data_inner=list(data.values())
p.vbar(x,top=y,width=0.15,color='grey')
p.xaxis.axis_label = 'Options'
p.yaxis.axis_label = 'Fractions'
mainLayout = column(row(dropdown,dropdown_sub,name='Widgets'),p,name='mainLayout')
curdoc().add_root(mainLayout)
#create a session
session = push_session(curdoc())
session.loop_until_closed()