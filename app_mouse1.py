
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pprint import pprint

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

mouse_data = pd.read_csv("C:/Users/Anahit Petrosyan/Desktop/DataVizualization/Dash_Homework_Mouse_data/Mouse_metadata.csv")
study_results = pd.read_csv("C:/Users/Anahit Petrosyan/Desktop/DataVizualization/Dash_Homework_Mouse_data/Study_results.csv")
merged_df = pd.merge(mouse_data, study_results, on = 'Mouse ID')

# -------------------------------------------------------------------------------------------------------------- 

#										     	PART 1: DESIGN PARAMETERS

# --------------------------------------------------------------------------------------------------------------
# Here we will set the colors, margins, DIV height&weight and other parameters

color_choices = {
	'light-blue': '#7FAB8',
	'light-grey': '#F7EFED',
	'light-red':  '#F1485B',
	'dark-blue':  '#33546D',
	'middle-blue': '#61D4E2'
}

drug_colors = {
	'Placebo':		'#29304E',
	'Capomulin':	'#27706B',	
	'Ramicane':		'#71AB7F',
	'Ceftamin':		'#9F4440',
	'Infubinol':	'#FFD37B',
	'Ketapril':		'#FEADB9',
	'Naftisol':		'#B3AB9E',
	'Propriva':		'#ED5CD4',
	'Stelasyn':		'#97C1DF',
	'Zoniferol':	'#8980D4'
 
}

colors = {
		'full-background':		color_choices['light-grey'],
		'chart-background':		color_choices['light-grey'],
		'histogram-color-1':	color_choices['dark-blue'],
		'histogram-color-2':	color_choices['light-red'],
		'block-borders':		color_choices['dark-blue']
}

margins = {
		'block-margins': '10px 10px 10px 10px',
		'block-margins': '4px 4px 4px 4px'
}

sizes = {
		'subblock-heights': '290px'
}



# -------------------------------------------------------------------------------------------------------------- 

#									        		PART 2: ACTUAL LAYOUT

# --------------------------------------------------------------------------------------------------------------
# Here we will set the DIV-s and other parts of our layout
# We need to have a 2x2 grid
# I have also included 1 more grid on top of others, where we will show the title of the app



# -------------------------------------------------------------------------------------- DIV for TITLE
div_title = html.Div(children =	html.H1('Drug Efficacy Analysis: Mouse Dataset'),
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'text-align': 'center'
							}
					)

# ---------# -------------------------------------------------------------------------------------- DIV for first row (1.1 and 1.2)

# -------------------------------------------------------------- inside DIV 1.1
div_1_1_button = dcc.Checklist (
				id = 'weight-histogram-checklist',
		        options=[
		        	{'label': drug, 'value': drug} for drug in np.unique(mouse_data['Drug Regimen'])
		        ],
		        value=['Placebo'],
		        labelStyle={'display': 'inline-block'}
			)#This is a Dash Core Component Checklist component. It allows users to select one or more options from a list.

div_1_1_graph = dcc.Graph(
				id = 'weight-histogram',
		        
			)#This is a Dash Core Component Graph component. It represents the histogram graph for displaying the weight distribution of selected drug types. 

div_1_1 = html.Div(children = [div_1_1_button, div_1_1_graph],
				#className = 'test',
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '50%',
							# 'height': sizes['subblock-heights'],
					},
					        

				)# This is a Dash HTML Component Div component that contains both the div_1_1_button and div_1_1_graph components. 

# -------------------------------------------------------------- inside DIV 1.2
div_1_2 = html.Div(children=[
                        dcc.RadioItems(
                        id='overlay-drug-radio',
                        options=[{'label': drug, 'value': drug} for drug in np.unique(mouse_data['Drug Regimen'])],
                        value='Placebo',
                        labelStyle={'display': 'inline-block'}
                        ),
                        dcc.Graph(
                            id='weight-distribution-chart',
                            figure= {}
                        ),

                    ],
                    style={
                        'border': '1px {} solid'.format(colors['block-borders']),
                        'margin': margins['block-margins'],
                        'width': '50%',
                    },
                    )   


# -------------------------------------------------------------- inside DIV 2.1
div_2_1 = html.Div(
    children=[
        dcc.Checklist(
            id='drug-group-checklist',
            options=[
                {'label': 'Lightweight', 'value': 'lightweight'},
                {'label': 'Heavyweight', 'value': 'heavyweight'},
                {'label': 'Placebo', 'value': 'placebo'}
            ],
            value=['placebo'],  # Default selected group
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(
            id='survival-function-chart',
            figure={}
        ),
        html.Div(id='sub-drug-options'),
        html.Div(id='hidden-drug-checklist', style={'display': 'none'})
    ],
    style={
        'border': '1px solid',  # Adjust the border style as needed
        'margin': '10px',  # Adjust the margin as needed
        'width': '50%',  # Adjust the width as needed
    }
)


# -------------------------------------------------------------- inside DIV 2.2
div_2_2 = html.Div(
    children=[
        dcc.Graph(
            id='survival-function-time-chart',
            figure={}
        ),
        dcc.Checklist(
            id='drug-group-time-checklist',
            options=[
                {'label': 'Lightweight', 'value': 'lightweight'},
                {'label': 'Heavyweight', 'value': 'heavyweight'},
                {'label': 'Placebo', 'value': 'placebo'}
            ],
            value=['placebo'],  # Default selected group
            labelStyle={'display': 'inline-block'}
        )
    ],
    style={
        'border': '1px {} solid'.format(colors['block-borders']),
        'margin': margins['block-margins'],
        'width': '50%',
    }
) 

# -------------------------------------------------------------------------------------- Collecting all DIV-s in the final layout

# -------------------------------------------------------------------------------------- Collecting all DIV-s in the final layout
# Here we collect all DIV-s into a final layout DIV
app.layout = html.Div([
    div_title,  # Title row
    html.Div([div_1_1, div_1_2], style={'display': 'flex'}),  # First row
    html.Div([div_2_1, div_2_2], style={'display': 'flex'})  # Second row
],
    style={
        'backgroundColor': colors['full-background']
    }
)
# -------------------------------------------------------------------------------------------------------------- 

# histogram of mice weights' for each drug
# it is a stacked histogram which lets us put histograms on top of each other 


# -------------------------------------------------------------- Chart 1
@app.callback(
    Output(component_id='weight-histogram', component_property='figure'),
    [Input(component_id='weight-histogram-checklist', component_property='value')]
)
def update_weight_histogram(drug_names):
    
    traces = []

    for drug in drug_names:
    	traces.append(go.Histogram(x=mouse_data[mouse_data['Drug Regimen']==drug]['Weight (g)'],
    							name = drug,
    							opacity = 0.9,
    							marker = dict(color=drug_colors[drug]))
    				)

    return {
        'data': traces,
        'layout': dict(
        	barmode='stack',
            xaxis={'title': 'Mouse weight',
   					'range': [merged_df['Weight (g)'].min(), merged_df['Weight (g)'].max()],
   					'showgrid': False
   					},
            yaxis={'title': 'Number of mice', 
            		'showgrid': False,
            		'showticklabels': True
            		},
            autosize=False,
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
        )
    }


# -------------------------------------------------------------- Chart 2
@app.callback(
    Output(component_id='weight-distribution-chart', component_property='figure'),
    [Input(component_id='overlay-drug-radio', component_property='value')]
)
def update_weight_distribution(selected_drug):
    traces = []

    # Overall weight distribution
    overall_distribution = go.Histogram(x=mouse_data['Weight (g)'],
                                        name='All mice',
                                        opacity=0.5,
                                        marker=dict(color='gray'))

    traces.append(overall_distribution)

    # Weight distribution for the selected drug
    if selected_drug:
        if selected_drug in drug_colors:  # Check if the selected drug is valid
            selected_distribution = go.Histogram(x=mouse_data[mouse_data['Drug Regimen'] == selected_drug]['Weight (g)'],
                                                name=selected_drug,
                                                opacity=0.9,
                                                marker=dict(color=drug_colors[selected_drug]))

            traces.append(selected_distribution)
        else:
            print(f"Color for drug '{selected_drug}' not found in drug_colors dictionary.")

    return {
        'data': traces,
        'layout': dict(
            barmode='overlay',
            xaxis={'title': 'Mouse Weight','showgrid': False},
            yaxis={'title': 'Number of Mice','showgrid': False},
            autosize=False,
            paper_bgcolor=colors['chart-background'],
            plot_bgcolor=colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
        )
    }

    
# -------------------------------------------------------------- Chart 3
@app.callback(
    Output('survival-function-chart', 'figure'),
    [Input('drug-group-checklist', 'value')]
)
def update_survival_function(selected_group):
    traces = []

    if 'lightweight' in selected_group:
        lightweight_drugs = ['Ramicane', 'Capomulin']
        for drug in lightweight_drugs:
            drug_data = merged_df[merged_df['Drug Regimen'] == drug]
            traces.append(go.Histogram(
                x=drug_data['Weight (g)'],
                name=drug,
                marker=dict(color=drug_colors[drug])
            ))

    if 'heavyweight' in selected_group:
        heavyweight_drugs = ['Ceftamin', 'Infubinol', 'Ketapril', 'Naftisol', 'Propriva', 'Stelasyn', 'Zoniferol']
        for drug in heavyweight_drugs:
            drug_data = merged_df[merged_df['Drug Regimen'] == drug]
            traces.append(go.Histogram(
                x=drug_data['Weight (g)'],
                name=drug,
                marker=dict(color=drug_colors[drug])
            ))

    if 'placebo' in selected_group:
        placebo_data = merged_df[merged_df['Drug Regimen'] == 'Placebo']
        traces.append(go.Histogram(
            x=placebo_data['Weight (g)'],
            name='Placebo',
            marker=dict(color=drug_colors['Placebo'])
        ))

    return {
        'data': traces,
        'layout': dict(
            barmode='overlay',
            xaxis={'title': 'Mouse Weight ','showgrid': False},
            yaxis={'title': 'Number of Mice','showgrid': False},
            autosize=False,
            paper_bgcolor=colors['chart-background'],
            plot_bgcolor=colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
        )
    }


# -------------------------------------------------------------- Chart 4
@app.callback(
    Output('survival-function-time-chart', 'figure'),
    [Input('drug-group-time-checklist', 'value')]
)
def update_survival_function_time(selected_group):
    traces = []

    if 'lightweight' in selected_group:
        lightweight_drugs = ['Ramicane', 'Capomulin']
        for drug in lightweight_drugs:
            drug_data = merged_df[merged_df['Drug Regimen'] == drug]
            # Placeholder data for now
            timepoints = sorted(drug_data['Timepoint'].unique())
            mice_alive = [len(drug_data[drug_data['Timepoint'] == tp]) for tp in timepoints]
            traces.append(go.Scatter(
                x=timepoints,
                y=mice_alive,
                mode='lines+markers',
                name=drug,
                marker=dict(color=drug_colors[drug])  # Set color for the drug
            ))

    if 'heavyweight' in selected_group:
        heavyweight_drugs = ['Ceftamin', 'Infubinol', 'Ketapril', 'Naftisol', 'Propriva', 'Stelasyn', 'Zoniferol']
        for drug in heavyweight_drugs:
            drug_data = merged_df[merged_df['Drug Regimen'] == drug]
            # Placeholder data for now
            timepoints = sorted(drug_data['Timepoint'].unique())
            mice_alive = [len(drug_data[drug_data['Timepoint'] == tp]) for tp in timepoints]
            traces.append(go.Scatter(
                x=timepoints,
                y=mice_alive,
                mode='lines+markers',
                name=drug,
                marker=dict(color=drug_colors[drug])  # Set color for the drug
            ))

    if 'placebo' in selected_group:
        placebo_data = merged_df[merged_df['Drug Regimen'] == 'Placebo']
        # Placeholder data for now
        timepoints = sorted(placebo_data['Timepoint'].unique())
        mice_alive = [len(placebo_data[placebo_data['Timepoint'] == tp]) for tp in timepoints]
        traces.append(go.Scatter(
            x=timepoints,
            y=mice_alive,
            mode='lines+markers',
            name='Placebo',
            marker=dict(color=drug_colors['Placebo'])  # Set color for the placebo
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Time', 'showgrid': False},
            yaxis={'title': 'Number of Mice Alive', 'showgrid': False},
            autosize=False,
            paper_bgcolor=colors['chart-background'],
            plot_bgcolor=colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 1, 'y': 1, 'xanchor': 'right'},  # Set xanchor to 'right'
        )
    }


# -------------------------------------------------------------------------------------------------------------- 

#								             			PART 4: RUNNING THE APP

# --------------------------------------------------------------------------------------------------------------
# >> use __ debug=True __ in order to be able to see the changes after refreshing the browser tab,
#			 don't forget to save this file before refreshing
# >> use __ port = 8081 __ or other number to be able to run several apps simultaneously
if __name__ == '__main__':
	app.run_server(debug=True, port = 8081)