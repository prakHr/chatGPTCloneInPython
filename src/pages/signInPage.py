import dash
dash.register_page(__name__,path = '/')

from dash import dcc, html, Input, State, Output, callback

import dash_bootstrap_components as dbc
import json
import requests
from config import api_key,api_host,config_file_path
from furl import furl
from pprint import pprint
import pyrebase

layout  = html.Div(children = [
            
        
        dcc.Input(id="email", type="email", placeholder="", style={'marginRight':'10px'}),
        dcc.Input(id="password", type="password", placeholder="", debounce=True),
        html.Button('SIGN IN',id='submit-val',n_clicks=0),

        html.H5(id='message',children=[]),
        dcc.Link(
            dbc.Button('PROMPT ENGINEERING USING CHATGPT'),
            href='/promptGenerator',
            refresh = False
        ),
        
])
def validate(email,password):
	if password is None or len(password)==0:
		return "Dont give empty password!"
	if email is None or len(email)==0:
		return "Dont give empty email!"
	if not email.endswith("@gmail.com"):
		return "Email should end with @gmail.com!"
	return True

@callback(
	[
		Output("message","children"),
		Output("stored-data","data")
	],
	[
		Input("email","value"),
		Input("password","value"),
		Input("submit-val","n_clicks"),
		Input("message","children"),
		State("stored-data","data")
	]
)
def trigger_signIn(email,password,n_clicks,children,data):
	input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
	if n_clicks>0 and input_id=="submit-val":
		check = validate(email,password)
		if check==True:
			f = open(config_file_path)
			#####################
			# user1@gmail.com ###
			# 123456 ############
			#####################

			# returns JSON object as 
			# a dictionary
			firebaseConfig = json.load(f)
			firebase = pyrebase.initialize_app(firebaseConfig)
			auth = firebase.auth()
			try:
				auth.sign_in_with_email_and_password(email,password)
				data['email'] = email
				data['password'] = password
				
				children = ["Successfully Signed In\n"]
			except:
				try:
					auth.create_user_with_email_and_password(email,password)
					children = ["Successfully Registered You In &"]
					auth.sign_in_with_email_and_password(email,password)
					children += ["Successfully Signed In\n"]
					data['email'] = email
					data['password'] = password
				except Exception as e:
					children = [f"{e}\n"]
			f.close()
			return children,data
		return [check],data

	return children,data


