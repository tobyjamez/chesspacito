#!/usr/bin/env python
#  -*- coding: utf-8 -*-

# 3rd party imports ------------------------------------------------------------
from flask import Flask, request
from webexteamssdk import WebexTeamsAPI, Webhook
import json

# local imports ----------------------------------------------------------------
import parser
from helpers import (read_yaml_data,
                     get_ngrok_url,
                     find_webhook_by_name,
                     delete_webhook, create_webhook)


flask_app = Flask(__name__)
teams_api = None


@flask_app.route('/teamswebhook', methods=['POST'])
def teamswebhook():
    if request.method == 'POST':

        json_data = request.json
        print("\n")
        print("WEBHOOK POST RECEIVED:")
        print(json_data)
        print("\n")

        webhook_obj = Webhook(json_data)
        # Details of the message created
        room = teams_api.rooms.get(webhook_obj.data.roomId)
        message = teams_api.messages.get(webhook_obj.data.id)
        person = teams_api.people.get(message.personId)
        email = person.emails[0]

        print("NEW MESSAGE IN ROOM '{}'".format(room.title))
        print("FROM '{}'".format(person.displayName))
        print("MESSAGE '{}'\n".format(message.text))

        # Message was sent by the bot, do not respond.
        # At the moment there is no way to filter this out, there will be in the future
        me = teams_api.people.me()
        if message.personId == me.id:
            return 'OK'
        else:
            print(message)

            if message.text.lower()[:3] == "new":
                dest = "board.bd"
                board = parser.Board(dest=dest)
                chess_response = str(board)
                teams_api.messages.create(roomId=room.id, text=chess_response)
                teams_api.messages.create(toPersonEmail=message.text.lower()[4:],
                                          text=str(person.displayName + 
                                                   " invited you to play Chess"))
                opponent_email = message.text.lower()[4:]
                board.save(dest)
                teams_api.messages.create(toPersonEmail=opponent_email,
                                          text=chess_response)
                with open('players.json', 'w') as f:
                    print("\nSaving...\n")
                    json.dump([{str(person.emails[0]): {'board': str(dest),
                                                'opponent_email': opponent_email},
                               opponent_email: {'board': str(dest),
                                                'opponent_email': str(person.emails[0])}},
                                                {'turn': person.emails[0]}],
                              f)

            else:
                with open('players.json', 'r') as f:
                    status_dict = json.loads(f.read())
                    game_dict = status_dict[0]
                    turn_email = status_dict[1]['turn']
                    dest = game_dict[person.emails[0]]['board']
                    board = parser.load_board(dest)
                    opponent_email = game_dict[person.emails[0]]['opponent_email']


                if turn_email != person.emails[0]:
                    chess_response = "It is not your turn."
                    teams_api.messages.create(toPersonEmail=person.emails[0],
                                              text=chess_response)
                    print(turn_email)
                    return 1
                    
                if message.text == "?":
                    s = str(board.legal_moves).split('(')[1].split('(')
                    chess_response = str(s)[2:-4]
                    teams_api.messages.create(toPersonEmail=person.emails[0],
                                              text=chess_response)
                elif message.text.lower() == "show":
                    chess_response = str(board)
                    teams_api.messages.create(toPersonEmail=person.emails[0],
                                              text=chess_response)
                    
                else:
                    try:
                        board.push_san(message.text)
                        chess_response = "```\n" + str(board) + "\n```"
                        with open('players.json', 'w') as f:
                            json.dump([game_dict, {'turn': str(opponent_email)}], f)
                        if board.is_checkmate():
                            chess_response =  str(person.displayName) + " wins!"
                        if board.is_stalemate():
                            chess_response = "Stalemate!"
                    except(Exception) as e:
                        chess_response = "Illegal move!"
                        teams_api.messages.create(toPersonEmail=person.emails[0],
                                                  text=chess_response)
                        return 1

                    teams_api.messages.create(toPersonEmail=person.emails[0],
                                              markdown=chess_response)
                    teams_api.messages.create(toPersonEmail=opponent_email,
                                              markdown=chess_response)
                    board.save(board.dest)
                

    else:
        print('received none post request, not handled!')


if __name__ == '__main__':
    config = read_yaml_data('/opt/config/config.yaml')['hello_bot']
    teams_api = WebexTeamsAPI(access_token=config['teams_access_token'])

    ngrok_url = get_ngrok_url()
    webhook_name = 'hello-bot-wb-hook'
    dev_webhook = find_webhook_by_name(teams_api, webhook_name)
    if dev_webhook:
        delete_webhook(teams_api, dev_webhook)
    create_webhook(teams_api, webhook_name, ngrok_url + '/teamswebhook')

    flask_app.run(host='0.0.0.0', port=5000)
