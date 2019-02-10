# -*- coding: utf-8 -*-

###
### This build is a sample build of a deeper, per-class analysis.
### This layer of presentation would follow the initial dash system, once the
### gender bias is identified. This layer allows the user to find in what way
### has the data represented gender through other variables.
###


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


def generate_table(dataframe, max_rows=5):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Test Data
df = pd.read_csv(
    'data/hiring-patterns.csv')


#Params not represented:
#Skill Requirements met,
#Top 3 soft skills candidate selected from fixed list,
df.loc[df['Uni Ranking']<= 8, 'Uni Ranking'] = 1
df.loc[(df['Uni Ranking']> 8) & (df['Uni Ranking']<= 16), 'Uni Ranking'] = 2
df.loc[df['Uni Ranking']> 16, 'Uni Ranking'] = 3



gender_interviewd_df = df.groupby('Gender')['Interviewed'].apply(lambda x: (x=='Yes').sum()).reset_index(name='interviewed')
gender_hired_df = df.groupby('Gender')['Hired'].apply(lambda x: (x=='Yes').sum()).reset_index(name='hired')
gender_disabled_df = df.groupby('Gender')['Disabled'].apply(lambda x: (x=='Yes').sum()).reset_index(name='Disabled')
gender_not_disabled_df = df.groupby('Gender')['Disabled'].apply(lambda x: (x=='No').sum()).reset_index(name='Disabled')
gender_df = df.groupby('Gender').count()["Internships"].reset_index().join(gender_interviewd_df['interviewed']).join(gender_hired_df['hired'])
gender_df.rename(index=str, columns={"Internships": "total"}, inplace=True)
gender_df['ratio-interviewed'] = gender_df['interviewed']/gender_df['total']
gender_df['ratio-hired'] = gender_df['hired']/gender_df['interviewed']
gender_tier_male = df.groupby('Uni Ranking')['Gender'].apply(lambda x: (x=='Male').sum()).reset_index(name='Male')
gender_tier_female = df.groupby('Uni Ranking')['Gender'].apply(lambda x: (x=='Female').sum()).reset_index(name='Female')
gender_tier_female = gender_tier_female.drop(['Uni Ranking'], axis = 1)
gender_tier = pd.concat([gender_tier_male, gender_tier_female], axis = 1)

gender_tier_hire_male = df[df['Hired'] == 'Yes'].groupby('Uni Ranking')['Gender'].apply(lambda x: (x=='Male').sum()).reset_index(name='Male')
gender_tier_hire_female = df[df['Hired'] == 'Yes'].groupby('Uni Ranking')['Gender'].apply(lambda x: (x=='Female').sum()).reset_index(name='Female')
gender_tier_hire_female = gender_tier_hire_female.drop(['Uni Ranking'], axis = 1)
gender_hire_tier = pd.concat([gender_tier_hire_male, gender_tier_hire_female], axis = 1)

disabled_interviewd_df = df.groupby('Disabled')['Interviewed'].apply(lambda x: (x=='Yes').sum()).reset_index(name='interviewed')
disabled_hired_df = df.groupby('Disabled')['Hired'].apply(lambda x: (x=='Yes').sum()).reset_index(name='hired')
disabled_df = df.groupby('Disabled').count()["Internships"].reset_index().join(disabled_interviewd_df['interviewed']).join(disabled_hired_df['hired'])
disabled_df.rename(index=str, columns={"Internships": "total"}, inplace=True)
disabled_df['ratio-interviewed'] = disabled_df['interviewed']/disabled_df['total']
disabled_df['ratio-hired'] = disabled_df['hired']/disabled_df['interviewed']

ethnicity_interviewd_df = df.groupby('Ethnicity')['Interviewed'].apply(lambda x: (x=='Yes').sum()).reset_index(name='interviewed')
ethnicity_hired_df = df.groupby('Ethnicity')['Hired'].apply(lambda x: (x=='Yes').sum()).reset_index(name='hired')
ethnicity_df = df.groupby('Ethnicity').count()["Internships"].reset_index().join(ethnicity_interviewd_df['interviewed']).join(ethnicity_hired_df['hired'])
ethnicity_df.rename(index=str, columns={"Internships": "total"}, inplace=True)
ethnicity_df['ratio-interviewed'] = ethnicity_df['interviewed']/ethnicity_df['total']
ethnicity_df['ratio-hired'] = ethnicity_df['hired']/ethnicity_df['interviewed']
white = df[df.Ethnicity == 'White']
bme = df[df.Ethnicity == 'BME']
male = df[df.Gender == 'Male']
female = df[df.Gender == 'Female']



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(className="container", children=[

    html.Div(className="row", children=[
        html.Div(className="three columns", children=[
            html.H2('Gender.Evaluation', style={'color': 'gray'})
        ]),
    ]),

    html.Div([
        html.Div([
            html.H5("Feature Comparisons with Gender"),
            html.P("These graphs represent a comparison between the Gender and several other features presented in the data set. ", style={'color': 'gray', 'fontSize': 14})
        ], className="twelve columns"),
    ], className="row"),

    html.Div([
        html.Div([
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=gender_disabled_df['Gender'],
                            y=gender_disabled_df['Disabled'],
                            name='Disabled',
                            marker=go.bar.Marker(
                                color='rgb(225, 128, 0)'
                            )
                        ),
                        go.Bar(
                            x=gender_not_disabled_df['Gender'],
                            y=gender_not_disabled_df['Disabled'],
                            name='Not Disabled',
                            marker=go.bar.Marker(
                                color='rgb(55, 83, 109)'
                            )
                        )
                    ],
                    layout=go.Layout(
                        title='Gender vs Disability',
                        showlegend=False,
                        #legend=go.layout.Legend(
                        #    x=0,
                        #    y=-1.0
                        #),
                        margin=go.layout.Margin(l=20, r=20, t=50, b=20)
                    )
                ),
                style={'height': 200,'width': '100%'},
                id='disabled-gender'
            ),
            #html.P("Interview Comparison: {:.0f}%".format(100*gender_df.loc[gender_df['Gender'] == 'Female']['ratio-interviewed'].values[0] / gender_df.loc[gender_df['Gender'] == 'Male']['ratio-interviewed'].values[0])),
            #html.P("Hiring Comparison: {:.0f}%".format(100*gender_df.loc[gender_df['Gender'] == 'Female']['ratio-hired'].values[0] / gender_df.loc[gender_df['Gender'] == 'Male']['ratio-hired'].values[0])),
        ], className="four columns"),


        html.Div([
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x= list(gender_tier[['Male', 'Female']]),
                            y= (gender_tier[['Male', 'Female']]).iloc[0],
                            name='Tier 1',
                            marker=go.bar.Marker(
                                color='rgb(225, 128, 0)'
                            )
                        ),
                        go.Bar(
                            x= list(gender_tier[['Male', 'Female']]),
                            y= (gender_tier[['Male', 'Female']]).iloc[1],
                            name='Tier 2',
                            marker=go.bar.Marker(
                                color='rgb(55, 83, 109)'
                            )
                        ),
                        go.Bar(
                            x= list(gender_tier[['Male', 'Female']]),
                            y= (gender_tier[['Male', 'Female']]).iloc[2],
                            name='Tier 3',
                            marker=go.bar.Marker(
                                color='rgb(26, 118, 255)'
                            )
                        )
                    ],
                    layout=go.Layout(
                        title='Gender vs University Ranking',

                        showlegend=False,
                        legend=go.layout.Legend(
                            x=0,
                            y=-1.0
                        ),
                        margin=go.layout.Margin(l=20, r=20, t=50, b=20)
                    )
                ),
                style={'height': 200,'width': '100%'},
                id='gender-univranking'
            ),
            html.P("Many female applicants come from high ranking universities"),
        ], className="four columns"),


        html.Div([
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x= ['Male', 'Female'],
                            y=[white[white.Gender == 'Male'].shape[0], white[white.Gender == 'Female'].shape[0]],
                            name='White',
                            marker=go.bar.Marker(
                                color='rgb(225, 128, 0)'
                            )
                        ),
                        go.Bar(
                            x= ['Male', 'Female'],
                            y=[bme[bme.Gender == 'Male'].shape[0], bme[bme.Gender == 'Female'].shape[0]],
                            name='BME',
                            marker=go.bar.Marker(
                                color='rgb(55, 83, 109)'
                            )
                        ),
                    ],
                    layout=go.Layout(
                        title='Ethnicity vs Gender',
                        showlegend=False,
                        legend=go.layout.Legend(
                            x=0,
                            y=-1.0
                        ),
                        margin=go.layout.Margin(l=20, r=20, t=50, b=20)
                    )
                ),
                style={'height': 200,'width': '100%'},
                id='ethnicity-disabled'
            ),
            html.P("Ethnicity Comparison: {:.0f}%".format(100*ethnicity_df.loc[ethnicity_df['Ethnicity'] == 'BME']['ratio-interviewed'].values[0] / ethnicity_df.loc[ethnicity_df['Ethnicity'] == 'White']['ratio-interviewed'].values[0]), style = {'color': "#c7004c", 'fontWeight': 'bold'}),
            #html.P("Hiring Comparison: {:.0f}%".format(100*ethnicity_df.loc[ethnicity_df['Ethnicity'] == 'BME']['ratio-hired'].values[0] / ethnicity_df.loc[ethnicity_df['Ethnicity'] == 'White']['ratio-hired'].values[0])),
        ], className="four columns"),

    ], className="row"),

    html.Div([
        html.Div([
            html.P("\n After passing the relevant data set through our system, the following graphs have displayed biases that can be mitigated. In the “Gender vs Disability” graph, a bias towards males are displayed. The “Ethnicity vs Gender” graph has shown a significant bias towards white (caucasian) males.", style = {'fontSize': 20
                })

        ], className="eight columns"),

        html.Div([
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=['1', '2', '3', '4', '5'],
                            y=[male[male.Internships == 1].shape[0],
                                   male[male.Internships == 2].shape[0],
                                   male[male.Internships == 3].shape[0],
                                   male[male.Internships == 4].shape[0],
                                   male[male.Internships == 5].shape[0]],
                            name='Male'

                        ),
                        go.Bar(
                             x=['1', '2', '3', '4', '5'],
                            y=[female[female.Internships == 1].shape[0],
                               female[female.Internships == 2].shape[0],
                               female[female.Internships == 3].shape[0],
                               female[female.Internships == 4].shape[0],
                               female[female.Internships == 5].shape[0]],
                            name='Female'

                        )
                    ],
                    layout=go.Layout(
                        title='Gender vs Internships',
                        xaxis=dict(
                            title='Number of Internships',
                        ),

                        showlegend=False,
                        margin=go.layout.Margin(l=20, r=20, t=50, b=50)
                    )
                ),
                style={'height': 200,'width': '100%'},
                id='deptartment'
            ),
        ], className="four columns")

    ], className="row"),

])


if __name__ == '__main__':
    app.run_server(debug=True)
