import random
from operator import itemgetter

def load_members():
    while True:
        try:
            file = open("members.txt","r")
            members = {}
            for line in file:
                name, passwd, tries, wins, best_score = line.strip('\n').split(', ')
                members[name] = (passwd,int(tries),int(wins),int(best_score))
            file.close()
            return members
        except FileNotFoundError:
            input("""Make "members.txt" file and try again.
Press Enter if you're ready. """)

def store_members(members):
    file = open("members.txt","w+")
    names = members.keys()
    for name in names:
        passwd, tries, wins, best_score = members[name]
        line = name + ', ' + passwd + ', ' + str(tries) + ', ' + str(wins) + ", " + str(best_score) + '\n'              
        file.write(line)
    file.close()

def login(members):
    username = input("Enter your name: (4 letters max) ")
    while len(username) > 4:
        username = input("Enter your name: (4 letters max) ")
    trypasswd = input("Enter your password: ")
    if username in members:
        if trypasswd == members[username][0]:
            tries = members[username][1]
            wins = members[username][2]
            best_score = members[username][3]
            print("You played", tries, "games and won", wins, "of them.")
            print("Your all-time winning percentage is", percentDivide(wins,tries),"%")
            print("Your best score is",best_score)
            return username, tries, wins, best_score, members
        else:
            return login(members)
    else:
        members[username] = (trypasswd, 0, 0, 0)
        return username, 0, 0, 0, members

def percentDivide(x,y):
    return 100*(x/y) if y > 0 else 0

def fresh():
    ranks = {0,1,2,3,4,5,6,7,8,9,10,11,"J"}
    left_black = []
    left_white = []
    for rank in ranks:
        left_black.append({"color" : "B", "rank" : rank})
        left_white.append({"color" : "W", "rank" : rank})
    random.shuffle(left_black)
    random.shuffle(left_white)
    return left_black, left_white

def pick(left):
    if not left == []:
        return left[0], left[1:]

def random_pick(left_black, left_white):
    if not left_black == [] and not left_white == []:
        if random.randint(0,1):
            return left_black[0], left_black[1:], left_white
        else:
            return left_white[0], left_black, left_white[1:]
    elif left_black == []:
        return left_white[0], left_black, left_white[1:]
    elif left_white == []:
        return left_black[0], left_black[1:], left_white

def howSortJoker(tiles,color):
    print("You have",end=' ')
    if color == 'B':
        print("black joker.")
    else:
        print("white joker.")
    show_player_tiles(tiles)
    index = int(input("Joker will be RIGHT of ___\n(just type tile number, and type 0 if you want joker to be placed FIRST.) : "))
    while index not in range(len(tiles)+1):
        index = int(input("Joker will be RIGHT of ___\n(just type tile number, and type 0 if you want joker to be placed FIRST.) : "))
    if color == 'B':
        tiles.insert(index,{'color' : 'B', 'rank' : 'J'})
    else:
        tiles.insert(index,{'color' : 'W', 'rank' : 'J'})
    return tiles

def com_sort(tiles):
    if not {'color' : 'B', 'rank' : 'J'} in tiles and not {'color' : 'W', 'rank' : 'J'} in tiles:
        tiles = sorted(tiles,key=itemgetter('rank','color'),reverse=True)
    if {'color' : 'B', 'rank' : 'J'} in tiles and {'color' : 'W', 'rank' : 'J'} in tiles:
        tiles.remove({'color' : 'B', 'rank' : 'J'})
        tiles.remove({'color' : 'W', 'rank' : 'J'})
        tiles = sorted(tiles,key=itemgetter('rank','color'),reverse=True)
        tiles.insert(random.randint(0,len(tiles)-1),{'color' : 'B', 'rank' : 'J'})
        tiles.insert(random.randint(0,len(tiles)-1),{'color' : 'W', 'rank' : 'J'})
    elif {'color' : 'B', 'rank' : 'J'} in tiles:
        tiles.remove({'color' : 'B', 'rank' : 'J'})
        tiles = sorted(tiles,key=itemgetter('rank','color'),reverse=True)
        tiles.insert(random.randint(0,len(tiles)-1),{'color' : 'B', 'rank' : 'J'})
    elif {'color' : 'W', 'rank' : 'J'} in tiles:
        tiles.remove({'color' : 'W', 'rank' : 'J'})
        tiles = sorted(tiles,key=itemgetter('rank','color'),reverse=True)
        tiles.insert(random.randint(0,len(tiles)-1),{'color' : 'W', 'rank' : 'J'})
    return tiles

def player_sort(tiles):
    if not {'color' : 'B', 'rank' : 'J'} in tiles and not {'color' : 'W', 'rank' : 'J'} in tiles:
        tiles = sorted(tiles,key=itemgetter('rank','color'))
    if {'color' : 'B', 'rank' : 'J'} in tiles and {'color' : 'W', 'rank' : 'J'} in tiles:
        tiles.remove({'color' : 'B', 'rank' : 'J'})
        tiles.remove({'color' : 'W', 'rank' : 'J'})
        tiles = sorted(tiles,key=itemgetter('rank','color'))
        tiles = howSortJoker(tiles,'B')
        tiles = howSortJoker(tiles,'W')
    elif {'color' : 'B', 'rank' : 'J'} in tiles:
        tiles.remove({'color' : 'B', 'rank' : 'J'})
        tiles = sorted(tiles,key=itemgetter('rank','color'))
        tiles = howSortJoker(tiles,'B')
    elif {'color' : 'W', 'rank' : 'J'} in tiles:
        tiles.remove({'color' : 'W', 'rank' : 'J'})
        tiles = sorted(tiles,key=itemgetter('rank','color'))
        tiles = howSortJoker(tiles,'W')
    return tiles

def show_player_tiles(player):
    print("-----")
    for x in range(1,len(player)+1):
        print(x,end='  ')
    print()
    for tile in player:
        print(tile["color"],tile["rank"],sep='',end=' ')
    print()
    print("-----")

def new_show_tiles(player,com,public_player,public_com,new_index):
    print('-----')
    for x in range(len(com),0,-1):
        print(x,end='  ')
    print()
    for tile in com:
        if tile in public_com:
            print(tile["color"],tile["rank"],sep='', end=' ')
        else:
            print(tile["color"],'?',sep='',end=' ')
    print()
    print("Tile",len(com)-new_index,"is new!")
    for x in range(1,len(player)+1):
        print(x,end='  ')
    print()
    for tile in player:
        print(tile["color"],tile["rank"],sep='',end=' ')
    print()
    x = 0
    for index in range(len(player)):
        if player[index] in public_player:
            print(index+1,end=' ')
            x = 1
    if x == 0:
        print("Nothing is public.")
    else:
        print("is public.")
    print('-----')

def show_tiles(player,com,public_player,public_com):
    print('-----')
    for x in range(len(com),0,-1):
        print(x,end='  ')
    print()
    for tile in com:
        if tile in public_com:
            print(tile["color"],tile["rank"],sep='', end=' ')
        else:
            print(tile["color"],'?',sep='',end=' ')
    print()

    for x in range(1,len(player)+1):
        print(x,end='  ')
    print()
    for tile in player:
        print(tile["color"],tile["rank"],sep='',end=' ')
    print()
    x = 0
    for index in range(len(player)):
        if player[index] in public_player:
            print(index+1,end=' ')
            x = 1
    if x == 0:
        print("Nothing is public.")
    else:
        print("is public.")
    print('-----')

def ask(message):
    answer = input(message)
    while not answer in ('y', 'n'):
        answer = input(message)
    return answer == 'y'

def show_top5(members):
    dict = {}
    for username in members:
        dict[username] = members[username]
    sorted_members = sorted(dict.items(),key=lambda x: x[1][3],reverse=True)
    print("All-time Top 5 based on best score")
    prize = 1
    for person in sorted_members:
        if prize > 5:
            return
        if person[1][3] > 0:
            print(prize,'. ',person[0], ' : ',person[1][3],sep='')
            prize += 1
        else:
            return

def renew_members(username,tries,wins,best_score,members):
    members[username] = (members[username][0],tries,wins,best_score)
    return members

def chooseColor():
    x = input("Choose the tile color!(B/W): ")
    if not x in ('B','W'):
        return chooseColor()
    return x

def new_sort_player(new_tile,player):
    if new_tile["rank"] == 'J':
        if new_tile["color"] == 'B':
            player = howSortJoker(player,'B')
            return player
        else: #white joker
            player = howSortJoker(player,'W')
            return player
    else:
        if not {'color' : 'B', 'rank' : 'J'} in player and not {'color' : 'W', 'rank' : 'J'} in player:
            player.append(new_tile)
            return sorted(player,key=itemgetter('rank','color'))
        elif {'color' : 'B', 'rank' : 'J'} in player and {'color' : 'W', 'rank' : 'J'} in player:
            if abs(player.index({'color' : 'B', 'rank' : 'J'})-player.index({'color' : 'W', 'rank' : 'J'})) == 1:#연속해있으면
                if player.index({'color' : 'B', 'rank' : 'J'}) < player.index({'color' : 'W', 'rank' : 'J'}):#B가앞
                    jokers = [{'color' : 'B', 'rank' : 'J'}, {'color' : 'W', 'rank' : 'J'}]
                    joker_index = player.index({'color' : 'B', 'rank' : 'J'})
                else:#W가앞
                    jokers = [{'color' : 'W', 'rank' : 'J'}, {'color' : 'B', 'rank' : 'J'}]
                    joker_index = player.index({'color' : 'W', 'rank' : 'J'})
                if not joker_index == 0:
                    pre_tile = player[joker_index-1]
                else:
                    pre_tile = 0
                player.remove({'color' : 'B', 'rank' : 'J'})
                player.remove({'color' : 'W', 'rank' : 'J'})
                player.append(new_tile)
                player = sorted(player,key=itemgetter('rank','color'))
                if not pre_tile == 0:
                    pre_index = player.index(pre_tile)
                    player[pre_index+1:pre_index+1] = jokers
                    return player
                else:
                    return jokers + player
        elif {'color' : 'B', 'rank' : 'J'} in player:
            joker_index = player.index({'color' : 'B', 'rank' : 'J'})
            if not joker_index == 0:
                pre_tile = player[joker_index-1]
            else:
                pre_tile = 0
            player.remove({'color' : 'B', 'rank' : 'J'})
            player.append(new_tile)
            player = sorted(player,key=itemgetter('rank','color'))
            if not pre_tile == 0:
                pre_index = player.index(pre_tile)
                player.insert(pre_index+1,{'color' : 'B', 'rank' : 'J'})
                return player
            else:
                return [{'color' : 'B', 'rank' : 'J'}] + player
        elif {'color' : 'W', 'rank' : 'J'} in player:
            joker_index = player.index({'color' : 'W', 'rank' : 'J'})
            if not joker_index == 0:
                pre_tile = player[joker_index-1]
            else:
                pre_tile = 0
            player.remove({'color' : 'W', 'rank' : 'J'})
            player.append(new_tile)
            player = sorted(player,key=itemgetter('rank','color'))
            if not pre_tile == 0:
                pre_index = player.index(pre_tile)
                player.insert(pre_index+1,{'color' : 'W', 'rank' : 'J'})
                return player
            else:
                return [{'color' : 'W', 'rank' : 'J'}] + player

def new_sort_com(new_tile,com):
    if new_tile["rank"] == 'J':
        new_index = random.randint(0,len(com))
        com.insert(new_index ,new_tile)
        return com, new_index
    else:
        if not {'color' : 'B', 'rank' : 'J'} in com and not {'color' : 'W', 'rank' : 'J'} in com:
            com.append(new_tile)
            com = sorted(com,key=itemgetter('rank','color'),reverse=True)
            return com, com.index(new_tile)
        elif {'color' : 'B', 'rank' : 'J'} in com and {'color' : 'W', 'rank' : 'J'} in com:
            if abs(com.index({'color' : 'B', 'rank' : 'J'})-com.index({'color' : 'W', 'rank' : 'J'})) == 1:#연속해있으면
                if com.index({'color' : 'B', 'rank' : 'J'}) < com.index({'color' : 'W', 'rank' : 'J'}):#B가앞
                    jokers = [{'color' : 'B', 'rank' : 'J'}, {'color' : 'W', 'rank' : 'J'}]
                    joker_index = com.index({'color' : 'B', 'rank' : 'J'})
                else:#W가앞
                    jokers = [{'color' : 'W', 'rank' : 'J'}, {'color' : 'B', 'rank' : 'J'}]
                    joker_index = com.index({'color' : 'W', 'rank' : 'J'})
                if not joker_index == 0:
                    pre_tile = com[joker_index-1]
                else:
                    pre_tile = 0
                com.remove({'color' : 'B', 'rank' : 'J'})
                com.remove({'color' : 'W', 'rank' : 'J'})
                com.append(new_tile)
                com = sorted(com,key=itemgetter('rank','color'),reverse=True)
                if not pre_tile == 0:
                    pre_index = com.index(pre_tile)
                    com[pre_index+1:pre_index+1] = jokers
                    return com, com.index(new_tile)
                else:
                    return jokers + com, com.index(new_tile)
        elif {'color' : 'B', 'rank' : 'J'} in com:
            joker_index = com.index({'color' : 'B', 'rank' : 'J'})
            if not joker_index == 0:
                pre_tile = com[joker_index-1]
            else:
                pre_tile = 0
            com.remove({'color' : 'B', 'rank' : 'J'})
            com.append(new_tile)
            com = sorted(com,key=itemgetter('rank','color'),reverse=True)
            if not pre_tile == 0:
                pre_index = com.index(pre_tile)
                com.insert(pre_index+1,{'color' : 'B', 'rank' : 'J'})
                return com, com.index(new_tile)
            else:
                com = [{'color' : 'B', 'rank' : 'J'}] + com
                return com, com.index(new_tile)
        elif {'color' : 'W', 'rank' : 'J'} in com:
            joker_index = com.index({'color' : 'W', 'rank' : 'J'})
            if not joker_index == 0:
                pre_tile = com[joker_index-1]
            else:
                pre_tile = 0
            com.remove({'color' : 'W', 'rank' : 'J'})
            com.append(new_tile)
            com = sorted(com,key=itemgetter('rank','color'),reverse=True)
            if not pre_tile == 0:
                pre_index = com.index(pre_tile)
                com.insert(pre_index+1,{'color' : 'W', 'rank' : 'J'})
                return com, com.index(new_tile)
            else:
                com = [{'color' : 'W', 'rank' : 'J'}] + com
                return com, com.index(new_tile)

def player_turn(com,player,public_com,public_player,left_black,left_white,score):
    print("It's your turn!")
    if left_black == [] and left_white == []:
        pass
    elif left_black == []:
        print("You can only choose white tile.")
        tile, left_white = pick(left_white)
    elif left_white == []:
        print("You can only choose black tile.")
        tile, left_black = pick(left_black)
    else:
        if chooseColor() == 'B':
            tile, left_black = pick(left_black)
        else:
            tile, left_white = pick(left_white)
    player = new_sort_player(tile,player)
    while True:
        show_tiles(player, com, public_player, public_com)
        index = len(com)-int(input("Now guess!\nTile's index(only number): "))
        guess = input("Tile's num(number or 'J'): ")
        if not guess == 'J':
            guess = int(guess)
        if com[index]["rank"] == guess:
            print("That's right")
            public_com.append(com[index])
            score += 10
            if guess == 'J' or guess == 6:
                score += 20
            if com == public_com:
                score += 50
            if len(com) == len(public_com):
                break
            if not ask("More guess?(y/n): "):
                break
        else:
            print("That's wrong")
            public_player.append(tile)
            break
    show_tiles(player,com,public_player,public_com)
    if not len(com) == len(public_com) and not len(player) == len(public_player):
        com,player,public_com,public_player,left_black,left_white,score = com_turn(com,player,public_com,public_player,left_black,left_white,score)
    return com,player,public_com,public_player,left_black,left_white,score

def com_guess(com, player, public_com, public_player,tile):
    guess = []
    count = []
    all = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 'J']
    for _ in range(len(player)):
        guess.append([])
    for index in range(len(player)):
        if player[index] in public_player:
            guess[index] = -1
            count.append(-1)
        else:
            if player[index]['color'] == 'B':
                for num in all:
                    if not {"color":'B', "rank":num} in com:
                        guess[index].append(num)
            else:
                for num in all:
                    if not {"color":'W', "rank":num} in com:
                        guess[index].append(num)
            count.append(len(guess[index]))
    while True:
        min = 13
        for index in range(len(count)):
            if not count[index] == -1 and count[index] < min:
                min = count[index]
                min_index = index
        index = min_index
        _guess = random.choice(guess[index])
        print("Does tile",index+1,"mean",_guess,"?")
        if player[index]["rank"] == _guess:
            public_player.append(player[index])
            print("I'm right")
            if len(player) == len(public_player):
                break
            if random.randint(0,1):
                break
            show_tiles(player,com,public_player,public_com)
        else:
            print("I'm wrong")
            public_com.append(tile)
            guess[index].remove(_guess)
            break
    return com, player, public_com, public_player

def com_turn(com,player,public_com,public_player,left_black,left_white,score):
    print("It's my turn!")
    if not left_black == [] or not left_white == []:
        tile, left_black, left_white = random_pick(left_black, left_white)
        com,new_index = new_sort_com(tile, com)
        new_show_tiles(player,com,public_player,public_com,new_index)
    com, player,public_com ,public_player = com_guess(com,player,public_com,public_player,tile)
    show_tiles(player,com,public_player,public_com)
    if not len(com) == len(public_com) and not len(player) == len(public_player):
        com,player,public_com,public_player,left_black,left_white,score = player_turn(com,player,public_com,public_player,left_black,left_white,score)
    return com,player,public_com,public_player,left_black,left_white,score

def davincicode():
    com = []
    player = []
    public_com = []
    public_player = []
    score = 0
    left_black, left_white = fresh()

    for _ in range(4):
        if chooseColor() == 'B':
            tile, left_black = pick(left_black)
        else:
            tile, left_white = pick(left_white)
        player.append(tile)
        tile, left_black, left_white = random_pick(left_black, left_white)
        com.append(tile)
    com = com_sort(com)
    player = player_sort(player)
    show_tiles(player,com,public_player,public_com)

    if random.randint(0,1) == 1:
        print("You first.")
        com,player,public_com,public_player,left_black,left_white,score = player_turn(com,player,public_com,public_player,left_black,left_white,score)
    else:
        print("Me first.")
        com,player,public_com,public_player,left_black,left_white,score = com_turn(com,player,public_com,public_player,left_black,left_white,score)
    
    if len(public_com) == len(com):
        print("You win!")
        for tile in player:
            if not tile in public_player and not tile["rank"] == 'J':
                score += tile["rank"]
        return 1, score
    else:
        print("You lose!")
    return 0, score

def main():
    print("Hello! Let's play DA VINCI CODE!")
    username, tries, wins, best_score, members = login(load_members())
    new_tries = new_wins = 0
    
    print("----- NEW GAME -----")
    win, score = davincicode()
    if win == 1:
        new_wins += 1
    new_tries += 1
    if score > best_score:
        best_score = score
        
    while ask("Play more?(y/n) : "):
        print("----- NEW GAME -----")
        win, score = davincicode()
        if win == 1:
            new_wins += 1
        new_tries += 1
        if score > best_score:
            best_score = score
    
    wins += new_wins
    tries += new_tries

    members = renew_members(username,tries,wins,best_score,members)
    store_members(members)

    print("-----")
    print("You played",new_tries,"games and won",new_wins,"of them.")
    print("Your winning percentage today is",percentDivide(new_wins,new_tries),"%")
    print("Your best score today is",best_score)
    show_top5(members)
    print("Bye!")

main()
