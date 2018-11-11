from flask import Flask, request
import json
from webexteamssdk import WebexTeamsAPI, Webhook
import parser
from helpers import (read_yaml_data,
                     get_ngrok_url,
                     find_webhook_by_name,
                     delete_webhook, create_webhook)

from conf import access_token

flask_app = Flask(__name__)
teams_api = None

@flask_app.route('/teamswebhook', methods=['POST'])
def teamswebhook():
    """
    Handle 
    """
    print("\n" + str(request.method) + " received\n")
    print(request.json)

    json_data = request.json
    webhook_obj = Webhook(json_data)
    room = teams_api.rooms.get(webhook_obj.data.roomId)
    message = teams_api.messages.get(webhook_obj.data.id)

    # Don't respond to yourself
    if message.personId == teams_api.people.me().id:
        return 'OK'
    else:
        teams_api.messages.create(room.id, text=chess_response)
        person = teams_api.people.get(message.personId)
       
        with open('players.json') as f:
            player_json = f.read()

        try:
            board_dest = json.loads(player_json)[0][person]['active']
        except(Exception) as e:
            board_dest = "board.bd"
            board_dict = json.loads(player_json)[0]
            board_dict[person]['active'] = board_dest
            with open('players.json', 'w') as f:
                json.dump(board_dict, f)
                

        board = parser.Board(dest=board_dest)
        chess_response = parser.parse(board, message)

if __name__ == '__main__':

    teams_api = WebexTeamsAPI(access_token=access_token)
    ngrok_url = get_ngrok_url()

    webhook_name = 'hello-bot-wb-hook'
    dev_webhook = find_webhook_by_name(teams_api, webhook_name)
    if dev_webhook:
        delete_webhook(teams_api, dev_webhook)
    create_webhook(teams_api, webhook_name, ngrok_url + '/teamswebhook')

    flask_app.run(host='0.0.0.0', port=5000)
