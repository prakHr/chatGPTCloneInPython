import dash
dash.register_page(__name__,path = '/promptGenerator')

from dash import dcc, html, Input, State, Output, callback

import dash_bootstrap_components as dbc
import json
import requests
from config import api_key,api_host,config_file_path
from furl import furl
from pprint import pprint
import pyrebase
import requests
import json
layout  = html.Div(children = [
        html.H1("Create"),
        html.P("Generate an imaginative text through CHAT-GPT"),
        dcc.Input(id="prompt-command", type="text", placeholder="", style={'marginRight':'10px'}),
     	html.Div(id='text-generator-component',children=[]),
     	html.Div(id='text-getter-component',children=[]),
     	html.Button('GENERATE TEXT',id='submit-text-val',n_clicks=0),
     	html.Button('START FROM SCRATCH',id = 'submit-forget-val',n_clicks=0)
])

@callback(
	[
		Output("text-generator-component","children"),
		Output("text-getter-component","children"),
	],
	[
		Input("prompt-command","value"),
		Input("stored-data","data"),
		Input("submit-text-val","n_clicks"),
		Input("submit-forget-val","n_clicks"),
		Input('text-generator-component',"children"),
		Input("text-getter-component","children"),
	]
,prevent_initial_call = False)
def trigger_ImageGeneration(prompt_string_input,data,n_clicks,n_forget_clicks,children,feedback_children):
	input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
	if n_forget_clicks>0 and input_id =="submit-forget-val":
		feedback_children = []
	elif n_clicks>0 and input_id=="submit-text-val":

		# print(f"data={data}")
		email = data['email']
		password = data['password']
		# print(f"email={email}")
		# print(f"password={password}")
		f = open(config_file_path)

		try:
			#####################
			# user1@gmail.com ###
			# 123456 ############
			#####################

			# returns JSON object as 
			# a dictionary
			firebaseConfig = json.load(f)
			firebase = pyrebase.initialize_app(firebaseConfig)
			auth = firebase.auth()
			auth.sign_in_with_email_and_password(email,password)
			# print("Reached here!")
			url = f"https://{api_host}/chat/completions"
			previous_response = ""
			if len(feedback_children)>0:

				previous_response = feedback_children[-1]
				feedback_children = [feedback_children[-1]]
			feedback_prompt = previous_response + prompt_string_input
			# print(f"feedback_prompt={feedback_prompt}")
			feedback_children.append(feedback_prompt)
			payload = {
				"model": "gpt-3.5-turbo",
				"messages": [
					{
						"role": "user",
						"content": feedback_prompt
					}
				]
			}
			headers = {
				"content-type": "application/json",
				"X-RapidAPI-Key": api_key,
				"X-RapidAPI-Host": api_host
			}
			# print("Reached here2!")
			response = requests.request("POST", url, json=payload, headers=headers)
			# print("Reached here3!")
			# print(response.text)
			json_dict = json.loads(response.text)
			# print(f"json_dict={json_dict}")
			# image_url = json_dict["data"][0]["url"]
			# print("Reached here4!")
			# print(f"image_url={image_url}")
			
			chatgpt_response_query = json_dict['choices'][0]['message']['content']
			# print(f"chatgpt_response_query={chatgpt_response_query}")
			children=[html.Div(chatgpt_response_query)]
		except Exception as e:
			children=[html.Div(f"{e}")]
			# feedback_children.append("Got Error")
		f.close()
		return children,feedback_children
	return children,feedback_children




