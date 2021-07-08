import requests, time, glob, os
from PIL import Image, ImageFont, ImageDraw

print('bot active')

file = open('./token.txt')
auth = file.read()
file.close()

# Ballchasing auth
token = {
        'Authorization': f'{auth}'
        }

file = open('./oldreplay.txt')
old_replay = file.read()
file.close()

first_instance = True

while True:

    path = os.path.join('E:/Documents/My Games/Rocket League/TAGame/Demos', '*')
    newest_replay = max(glob.iglob(path), key=os.path.getctime)

    if newest_replay != old_replay:
        # When new replay added, post replay to Ballchasing group
        replay = newest_replay
        replay_file = open(replay, 'rb')
        files = {
                        'file': (replay,
                                 replay_file),
                    }
        replay_send = requests.post(f'https://ballchasing.com/api/v2/upload?', headers=token, files=files)
        location = replay_send.json()['id']

        file1 = open('./oldreplay.txt', 'w')
        file1.write(f'{newest_replay}')
        file1.close()
        file2 = open('./oldreplay.txt', 'r')
        old_replay = file2.read()
        file2.close()
        replay_file.close()
        # Wait for replay to process, then get request from group
        time.sleep(10)

        group_stats = requests.get(f'https://ballchasing.com/api/replays/{location}', headers=token)

        # Image setup
        match_image = Image.open('./PostMatchScreen.png')
        edit_match = ImageDraw.Draw(match_image)

        #print(group_stats.json())

        if replay_send.reason != 'Yes':

            # Organize team objects
            team_1 = group_stats.json()['blue']
            team_2 = group_stats.json()['orange']

            # Edit scoreboard on image
            scoreboard_font = ImageFont.truetype('./Gobold_Bold.ttf', 50)
            text = str(team_1['name'])
            w, h = edit_match.textsize(text, scoreboard_font)
            edit_match.text(((1170 - w) / 2, 60), text, (255, 255, 255), font=scoreboard_font)
            text = str(team_2['name'])
            w, h = edit_match.textsize(text, scoreboard_font)
            edit_match.text(((2690 - w) / 2, 60), text, (255, 255, 255), font=scoreboard_font)
            text = str(team_1['stats']['core']['goals'])
            w, h = edit_match.textsize(text, scoreboard_font)
            edit_match.text(((1770 - w) / 2, 210), text, (0, 0, 0), font=scoreboard_font)
            text = str(team_2['stats']['core']['goals'])
            w, h = edit_match.textsize(text, scoreboard_font)
            edit_match.text(((2080 - w) / 2, 210), text, (0, 0, 0), font=scoreboard_font)
            result_font = ImageFont.truetype('./Gobold_Bold.ttf', 40)
            if team_1['stats']['core']['goals'] > team_2['stats']['core']['goals']:
                text = 'VICTORY'
                w, h = edit_match.textsize(text, result_font)
                edit_match.text(((1170 - w) / 2, 135), text, (0, 0, 0), font=result_font)
                text = 'DEFEAT'
                w, h = edit_match.textsize(text, result_font)
                edit_match.text(((2690 - w) / 2, 135), text, (0, 0, 0), font=result_font)
            if team_1['stats']['core']['goals'] < team_2['stats']['core']['goals']:
                text = 'DEFEAT'
                w, h = edit_match.textsize(text, result_font)
                edit_match.text(((1170 - w) / 2, 135), text, (0, 0, 0), font=result_font)
                text = 'VICTORY'
                w, h = edit_match.textsize(text, result_font)
                edit_match.text(((2690 - w) / 2, 135), text, (0, 0, 0), font=result_font)

            # Edit bars at bottom of image
            total = team_1['stats']['boost']['amount_collected']+team_2['stats']['boost']['amount_collected']
            bar1 = team_1['stats']['boost']['amount_collected'] / total
            bar2 = team_2['stats']['boost']['amount_collected'] / total
            x1 = 386 * bar2
            x2 = 386 * bar1
            edit_match.rectangle([771, 915, 1157 - x1, 945], fill=(137, 204, 255))
            edit_match.rectangle([771 + x2, 915, 1157, 945], fill=(255, 209, 100))
            edit_match.rectangle([771 + x2 - 2, 910, 771 + x2 + 2, 950], fill=(255, 255, 255))
            percent1 = str(int(round(bar1*100, 0)))
            text = f'{percent1}%'
            w, h = edit_match.textsize(text, result_font)
            edit_match.text(((1420 - w) / 2, 900), text, (255, 255, 255), font=result_font)
            percent2 = str(int(round(bar2*100, 0)))
            text = f'{percent2}%'
            w, h = edit_match.textsize(text, result_font)
            edit_match.text(((2430 - w) / 2, 900), text, (255, 255, 255), font=result_font)


            total = team_1['stats']['positioning']['time_offensive_half']+team_2['stats']['positioning']['time_offensive_half']
            bar1 = team_1['stats']['positioning']['time_offensive_half'] / total
            bar2 = team_2['stats']['positioning']['time_offensive_half'] / total
            x1 = 386 * bar2
            x2 = 386 * bar1
            edit_match.rectangle([771, 1035, 1157 - x1, 1065], fill=(137, 204, 255))
            edit_match.rectangle([771 + x2, 1035, 1157, 1065], fill=(255, 209, 100))
            edit_match.rectangle([771 + x2 - 2, 1030, 771 + x2 + 2, 1070], fill=(255, 255, 255))
            percent1 = str(int(round(bar1*100, 0)))
            text = f'{percent1}%'
            w, h = edit_match.textsize(text, result_font)
            edit_match.text(((1420 - w) / 2, 1020), text, (255, 255, 255), font=result_font)
            percent2 = str(int(round(bar2*100, 0)))
            text = f'{percent2}%'
            w, h = edit_match.textsize(text, result_font)
            edit_match.text(((2430 - w) / 2, 1020), text, (255, 255, 255), font=result_font)

            # Player stats
            title_font = ImageFont.truetype('./Gobold_Bold.ttf', 35)
            team_1_players = [team_1['players'][0], team_1['players'][1], team_1['players'][2]]
            team_2_players = [team_2['players'][0], team_2['players'][1], team_2['players'][2]]

            for player in range(0,6):
                if player == 0:
                    x = 295
                if player == 1:
                    x = 800
                if player == 2:
                    x = 1300
                if player == 3:
                    x = 2560
                if player == 4:
                    x = 3040
                if player == 5:
                    x = 3530
                if player <= 2:
                    text = str(team_1_players[player]['name'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 335), text, (255, 255, 255), font=title_font)
                    text = str(team_1_players[player]['stats']['core']['goals'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 420), text, (255, 255, 255), font=title_font)
                    text = str(team_1_players[player]['stats']['core']['assists'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 475), text, (255, 255, 255), font=title_font)
                    text = str(team_1_players[player]['stats']['core']['shots'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 535), text, (255, 255, 255), font=title_font)
                    text = str(team_1_players[player]['stats']['core']['saves'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 590), text, (255, 255, 255), font=title_font)
                    text = str(team_1_players[player]['stats']['core']['score'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 645), text, (255, 255, 255), font=title_font)
                    text = str(team_1_players[player]['stats']['demo']['inflicted'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 705), text, (255, 255, 255), font=title_font)
                    text = str(team_1_players[player]['stats']['boost']['amount_stolen'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 765), text, (255, 255, 255), font=title_font)
                if player >= 3:
                    text = str(team_2_players[player-3]['name'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 335), text, (255, 255, 255), font=title_font)
                    text = str(team_2_players[player-3]['stats']['core']['goals'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 420), text, (255, 255, 255), font=title_font)
                    text = str(team_2_players[player-3]['stats']['core']['assists'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 475), text, (255, 255, 255), font=title_font)
                    text = str(team_2_players[player-3]['stats']['core']['shots'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 535), text, (255, 255, 255), font=title_font)
                    text = str(team_2_players[player-3]['stats']['core']['saves'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 590), text, (255, 255, 255), font=title_font)
                    text = str(team_2_players[player-3]['stats']['core']['score'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 645), text, (255, 255, 255), font=title_font)
                    text = str(team_2_players[player-3]['stats']['demo']['inflicted'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 705), text, (255, 255, 255), font=title_font)
                    text = str(team_2_players[player-3]['stats']['boost']['amount_stolen'])
                    w, h = edit_match.textsize(text, title_font)
                    edit_match.text(((x - w) / 2, 765), text, (255, 255, 255), font=title_font)

        # Save image
        print('Image Updated')
        match_image.save('./PostMatchScreenUpdated.png')
    # loop timer
    time.sleep(2)