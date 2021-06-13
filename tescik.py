def update_highscore(score):
    with open("highscores.txt","r") as file:
        hl = file.readline().split(";")
        hl = [ int(x) for x in hl ]
        hl = sorted(hl, reverse=True)
        for i in range(len(hl)):
            if score >= hl[i]:
                hl = hl[0:i] + [score] + hl[i:-1]
                return hl

    return hl

def overwrite_highscore(score):
    hlist = update_highscore(score)
    text = ""
    for i in range(len(hlist)-1):
        text += str(i) + ";"
    text += str(hlist[-1])
    with open("highscores.txt","w") as file:
        file.write(text)

hlist = update_highscore(200)
print(hlist)
