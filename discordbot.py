import os, discord, random, asyncio, requests, math, DiscordUtils, time, threading
from discord.ext import commands, tasks
from discord.ui import Select, Button, View

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='z!',help_command=None,intents=intents)

@bot.event
async def on_connect():
  print("bot online")

@bot.command(brief='Shows this menu')
async def help(ctx):
  helpers = ""
  helpers+="help: Shows this menu\n"
  for command in bot.commands:
    if command.name != "help":
      helpers+=f"{command.name} {command.help}: {command.brief}\n"
  embed  = discord.Embed(title="Commands", description=helpers,color=discord.Color.green())
  embed.set_footer(text="Prefix: z!")
  await ctx.send(embed=embed)

global checkersActive
checkersActive = False
@bot.command(brief='Play checkers against friends!', help='<@user>')
async def checkers(ctx, user: discord.User):
  global checkersActive
  checkersActive = True
  global checkersctx
  checkersctx = ctx
  global player1
  global player2
  global key
  global rawR
  global ckey_list
  global cval_list
  player1 = checkersctx.author.id
  player2 = user.id
  global p
  p = 1
  key = {
    "A" : "🇦",
    "B" : "🇧",
    "C" : "🇨",
    "D" : "🇩",
    "E" : "🇪",
    "F" : "🇫",
    "G" : "🇬",
    "H" : "🇭",
    "I" : "🟦",
    "J" : "1️⃣",
    "K" : "2️⃣",
    "L" : "3️⃣",
    "M" : "4️⃣",
    "N" : "5️⃣",
    "O" : "6️⃣",
    "P" : "7️⃣",
    "Q" : "8️⃣",
    "0" : "⬛",
    "1" : "🔴",
    "2" : "🟣",
    "3" : "❤️",
    "4" : "💜",
    "5" : "🟫",
    "↖" : "null",
    "↗" : "null",
    "↘" : "null",
    "↙" : "null"
  }
  cval_list = list(key.values())
  ckey_list = list(key.keys())
  
  rawR =[
  ["A",5,2,5,2,5,2,5,2],
  ["B",2,5,2,5,2,5,2,5],
  ["C",5,2,5,2,5,2,5,2],
  ["D",0,5,0,5,0,5,0,5],
  ["E",5,0,5,0,5,0,5,0],
  ["F",1,5,1,5,1,5,1,5],
  ["G",5,1,5,1,5,1,5,1],
  ["H",1,5,1,5,1,5,1,5],
  ["I","J","K","L","M","N","O","P","Q"]]
  
  global chacksboard
  info = await checkerBoard("ongoing", 1)
  chacksboard = await checkersctx.send(info)
  await game()
async def checkerBoard(state, person):
  newboard=""
  for row in rawR:
    for i in row:
      newi = key[str(i)]
      newboard+=newi
    newboard+="\n"
  firstPlayer = f"Player 1: <@{player1}>"
  secondPlayer = f"Player 2: <@{player2}>"
  turn = f"It is Player {str(p)}'s turn."
  if state == "ongoing":
    info = f"{firstPlayer}\n{secondPlayer}\n{turn}\n{newboard}"
  else:
    info = f"Player {person} wins!\n{newboard}"
  return info
async def addReaction(validMoves):
  global chacksboard
  await chacksboard.clear_reactions()
  moveReactions=""
  for move in validMoves:
    for i in move:
      if i not in moveReactions:
        moveReactions += i
  letters = ""
  numbers = ""
  directions = ""
  for i in moveReactions:
    if i in cval_list:
      letters += i
    elif i.isalpha():
      numbers += i
    elif i in ckey_list:
      directions += i
    numbers = "".join(sorted(numbers))
  moveReactions = f'{letters}{numbers}{directions}'
  for i in moveReactions:
    if i.isalpha()==True:
      await chacksboard.add_reaction(key[i])
    else:
      await chacksboard.add_reaction(i)
  await chacksboard.add_reaction("✅")
async def validMove():
  validMoves=[]
  for row in rawR:
    thisRow = rawR.index(row)
    lastRow = rawR[8]
    for i in range(len(row)):
      trueI = row[i]
      if str(trueI).isalpha() == False:
        if p == 1:
          if trueI == 1 and thisRow == 0:
            continue
          if trueI == 1 or trueI == 3:
            if thisRow > 0:
              aboveRow = rawR[thisRow-1]
              if aboveRow[i - 1] == 0:
                validMove=f'{key[row[0]]}{lastRow[i]}↖'
                validMoves.append(validMove)
              if i < 8:
                if aboveRow[i + 1] == 0:
                  validMove=f'{key[row[0]]}{lastRow[i]}↗'
                  validMoves.append(validMove)
            if thisRow > 1:
              upperRow = rawR[thisRow-2]
              if i > 1:
                if (aboveRow[i - 1] == 2 or aboveRow[i - 1] == 4) and (upperRow[i-2] == 0):
                  validMove=f'{key[row[0]]}{lastRow[i]}↖'
                  validMoves.append(validMove)
              if i < 7:
                if (aboveRow[i + 1] == 2 or aboveRow[i + 1] == 4) and (upperRow[i+2] == 0):
                  validMove=f'{key[row[0]]}{lastRow[i]}↗'
                  validMoves.append(validMove)
          if trueI == 3:
            if thisRow == 8:
              continue
            if thisRow < 8:
              belowRow = rawR[thisRow+1]
              if belowRow[i - 1] == 0:
                validMove=f'{key[row[0]]}{lastRow[i]}↙'
                validMoves.append(validMove)
              if i < 8:
                if belowRow[i + 1] == 0:
                  validMove=f'{key[row[0]]}{lastRow[i]}↘'
                  validMoves.append(validMove)
            if thisRow < 7:
              lowerRow = rawR[thisRow+2]
              if i > 1:
                if (belowRow[i - 1] == 2 or belowRow[i - 1] == 4) and (lowerRow[i-2] == 0):
                  validMove=f'{key[row[0]]}{lastRow[i]}↙'
                  validMoves.append(validMove)
              if i < 7:
                if (belowRow[i + 1] == 2 or belowRow[i + 1] == 4) and (lowerRow[i+2] == 0):
                  validMove=f'{key[row[0]]}{lastRow[i]}↘'
                  validMoves.append(validMove)
        elif p == 2:
          if trueI == 2 and thisRow == 8:
            continue
          if trueI == 2 or trueI == 4:
            if thisRow < 8:
              belowRow = rawR[thisRow+1]
              if belowRow[i - 1] == 0:
                validMove=f'{key[row[0]]}{lastRow[i]}↙'
                validMoves.append(validMove)
              if i < 8:
                if belowRow[i + 1] == 0:
                  validMove=f'{key[row[0]]}{lastRow[i]}↘'
                  validMoves.append(validMove)
            if thisRow < 7:
              lowerRow = rawR[thisRow+2]
              if i > 1:
                if (belowRow[i - 1] == 1 or belowRow[i - 1] == 3) and (lowerRow[i-2] == 0):
                  validMove=f'{key[row[0]]}{lastRow[i]}↙'
                  validMoves.append(validMove)
              if i < 7:
                if (belowRow[i + 1] == 1 or belowRow[i + 1] == 3) and (lowerRow[i+2] == 0):
                  validMove=f'{key[row[0]]}{lastRow[i]}↘'
                  validMoves.append(validMove)
          if trueI == 4:
            if thisRow == 0:
              continue
            if thisRow > 0:
              aboveRow = rawR[thisRow-1]
              if aboveRow[i - 1] == 0:
                validMove=f'{key[row[0]]}{lastRow[i]}↖'
                validMoves.append(validMove)
              if i < 8:
                if aboveRow[i + 1] == 0:
                  validMove=f'{key[row[0]]}{lastRow[i]}↗'
                  validMoves.append(validMove)
            if thisRow > 1:
              upperRow = rawR[thisRow-2]
              if i > 1:
                if (aboveRow[i - 1] == 1 or aboveRow[i - 1] == 3) and (upperRow[i-2] == 0):
                  validMove=f'{key[row[0]]}{lastRow[i]}↖'
                  validMoves.append(validMove)
              if i < 7:
                if (aboveRow[i + 1] == 1 or aboveRow[i + 1] == 3) and (upperRow[i+2] == 0):
                  validMove=f'{key[row[0]]}{lastRow[i]}↗'
                  validMoves.append(validMove)
  return validMoves
async def movePiece(potentialMove):
  global p
  potentialMove = list(potentialMove)
  pRow = potentialMove[0]
  pCol = potentialMove[1]
  pdir = potentialMove[2]
  lastRow = rawR[8]
  vRow = cval_list.index(pRow)
  cCol = lastRow.index(pCol)
  currentRow = rawR[vRow]
  currentPiece = currentRow[cCol]
  if p == 1:
    if vRow > 0:
      aboveRow = rawR[vRow-1]
      if pdir == "↖":
        if aboveRow[cCol-1] == 0:
          if aboveRow[0] == "A":
            aboveRow[cCol-1] = 3
          else:
            aboveRow[cCol-1] = currentPiece
      elif pdir == "↗":
        if aboveRow[cCol+1] == 0:
          if aboveRow[0] == "A":
            aboveRow[cCol+1] = 3
          else:
            aboveRow[cCol+1] = currentPiece
      if vRow > 1:
        upperRow = rawR[vRow - 2]
        if pdir == "↖":
          if aboveRow[cCol-1] == 2 or aboveRow[cCol-1] == 4:
            aboveRow[cCol-1] = 0
            if upperRow[0] == "A":
              upperRow[cCol-2] = 3
            else:
              upperRow[cCol-2] = currentPiece
        elif pdir == "↗":
          if aboveRow[cCol+1] == 2 or aboveRow[cCol+1] == 4:
            aboveRow[cCol+1] = 0
            if upperRow[0] == "A":
              upperRow[cCol+2] = 3
            else:
              upperRow[cCol+2] = currentPiece
    if currentPiece == 3:
      if vRow < 8:
        belowRow = rawR[vRow+1]
        if pdir == "↙":
          if belowRow[cCol-1] == 0:
            belowRow[cCol-1] = currentPiece
        elif pdir == "↘":
          if belowRow[cCol+1] == 0:
            belowRow[cCol+1] = currentPiece
        if vRow < 7:
          lowerRow = rawR[vRow+2]
          if pdir == "↙":
            if belowRow[cCol-1] == 2 or belowRow[cCol-1] == 4:
              belowRow[cCol-1] = 0
              lowerRow[cCol-2] = currentPiece
          elif pdir == "↘":
            if belowRow[cCol+1] == 2 or belowRow[cCol+1] == 4:
              belowRow[cCol+1] = 0
              lowerRow[cCol+2] = currentPiece
  elif p == 2:
    if vRow < 8:
      belowRow = rawR[vRow+1]
      if pdir == "↙":
        if belowRow[cCol-1] == 0:
          if belowRow[0] == "H":
            belowRow[cCol-1] = 4
          else:
            belowRow[cCol-1] = currentPiece
      elif pdir == "↘":
        if belowRow[cCol+1] == 0:
          if belowRow[0] == "H":
            belowRow[cCol+1] = 4
          else:
            belowRow[cCol+1] = currentPiece
      if vRow < 7:
        lowerRow = rawR[vRow+2]
        if pdir == "↙":
          if belowRow[cCol-1] == 1 or belowRow[cCol-1] == 3:
            belowRow[cCol-1] = 0
            if lowerRow[0] == "H":
              lowerRow[cCol-2] = 4
            else:
              lowerRow[cCol-2] = currentPiece
        elif pdir == "↘":
          if belowRow[cCol+1] == 1 or belowRow[cCol+1] == 3:
            belowRow[cCol+1] = 0
            if lowerRow[0] == "H":
              lowerRow[cCol+2] =4
            else:
              lowerRow[cCol+2] = currentPiece
    if currentPiece == 4:
      if vRow > 0:
        aboveRow = rawR[vRow-1]
        if pdir == "↖":
          if aboveRow[cCol-1] == 0:
            aboveRow[cCol-1] = currentPiece
        elif pdir == "↗":
          if aboveRow[cCol+1] == 0:
            aboveRow[cCol+1] = currentPiece
        if vRow > 1:
          upperRow = rawR[vRow-2]
          if pdir == "↖":
            if aboveRow[cCol-1] == 1 or aboveRow[cCol-1] == 3:
              aboveRow[cCol-1] = 0
              upperRow[cCol-2] = currentPiece
          elif pdir == "↗":
            if aboveRow[cCol+1] == 1 or aboveRow[cCol+1] == 3:
              aboveRow[cCol+1] = 0
              upperRow[cCol+2] = currentPiece
  currentRow[cCol] = 0
  if p==1:
    p=2
  elif p==2:
    p=1
  await game()
async def checkersWin():
  global validMoves
  resolved = False
  if validMoves == []:
    resolved = True
  else:
    for row in rawR:
      if (p in row) or (p+2 in row):
        break
    else:
      resolved = True
  if resolved == True:
    if p == 1:
      return "won", 2
    else:
      return "won", 1
  else:
    return "ongoing", 1
@bot.event
async def on_reaction_add(reaction, reactor):
  global potentialMove
  global chacksboard
  global validMoves
  if checkersActive == True:
    if reaction.message.id == chacksboard.id:
      reaction = str(reaction)
      if reaction in cval_list:
        valLoc = cval_list.index(reaction)
      else:
        valLoc = 9
      if (reactor.id == player1 and p == 1) or (reactor.id == player2 and p == 2):
        if reaction == "✅":
          if potentialMove in validMoves:
            await movePiece(potentialMove)
        else:
          if (reaction in ckey_list) or (valLoc < 8):
            potentialMove += reaction
          else:
            potentialMove += ckey_list[valLoc] 
@bot.event
async def on_reaction_remove(reaction, reactor):
  global potentialMove
  global chacksboard
  if checkersActive == True:
    if reaction.message.id == chacksboard.id:
      reaction = str(reaction)
      if reaction in cval_list:
        valLoc = cval_list.index(reaction)
      else:
        valLoc = 9
      if (reactor.id == player1 and p == 1) or (reactor.id == player2 and p == 2):
        if reaction == "✅":
          potentialMove = ""
        else:
          if (reaction in ckey_list) or (valLoc < 8):
            potentialMove = potentialMove.replace(reaction,"")
          else:
            potentialMove = potentialMove.replace(ckey_list[valLoc],"") 
async def game():
  global validMoves
  global chacksboard
  validMoves = await validMove()
  state, person = await checkersWin()
  info = await checkerBoard(state, person)
  chacksboard = await chacksboard.edit(content=info)
  if state == "won":
    return
  await addReaction(validMoves)
  global potentialMove 
  potentialMove = ""
    
global active
active = False
@bot.command(brief='Play minesweeper!', help='')
async def minesweeper(ctx):
  global minesweeperctx
  minesweeperctx = ctx
  global player
  global active
  player = minesweeperctx.author.id
  global mkey
  global mkey_list
  global minefield
  global blankfield
  global board
  active = True
  mkey = {
    "A" : "🇦",
    "B" : "🇧",
    "C" : "🇨",
    "D" : "🇩",
    "E" : "🇪",
    "F" : "🇫",
    "G" : "🇬",
    "H" : "🇭",
    "I" : "🇮",
    "J" : "🇯",
    "K" : "🇰",
    "L" : "🇱",
    "M" : "🇲",
    "X" : "⏹️",
    "0" : "⬜",
    "1" : "1️⃣",
    "2" : "2️⃣",
    "3" : "3️⃣",
    "4" : "4️⃣",
    "5" : "5️⃣",
    "6" : "6️⃣",
    "7" : "7️⃣",
    "8" : "8️⃣",
    "9" : "🚩",
    "10" : "❤️‍🔥",
    "11" : "🟦",
    "g"  : "‎",
  }
  mkey_list = list(mkey.keys())
  for i in range(14):
    mkey_list.pop(26-i)
  
  minefield = [
  ["A",11,11,11,11,11,11,11,11,11,11,11,11,11],
  ["B",11,11,11,11,11,11,11,11,11,11,11,11,11],
  ["C",11,11,11,11,11,11,11,11,11,11,11,11,11],
  ["D",11,11,11,11,11,11,11,11,11,11,11,11,11],
  ["E",11,11,11,11,11,11,11,11,11,11,11,11,11],
  ["F",11,11,11,11,11,11,11,11,11,11,11,11,11],
  ["G",11,11,11,11,11,11,11,11,11,11,11,11,11],
  ["H",11,11,11,11,11,11,11,11,11,11,11,11,11],
  ["I",11,11,11,11,11,11,11,11,11,11,11,11,11],
  ["J",11,11,11,11,11,11,11,11,11,11,11,11,11],
  ["K",11,11,11,11,11,11,11,11,11,11,11,11,11],
  ["L",11,11,11,11,11,11,11,11,11,11,11,11,11],
  ["M",11,11,11,11,11,11,11,11,11,11,11,11,11],
  ["X","A","g","B","g","C","g","D","g","E","g","F","g","G","g","H","g","I","g","J","g","K","g","L","g","M"]
  ]

  blankfield = [
  ["A",0,0,0,0,0,0,0,0,0,0,0,0,0],
  ["B",0,0,0,0,0,0,0,0,0,0,0,0,0],
  ["C",0,0,0,0,0,0,0,0,0,0,0,0,0],
  ["D",0,0,0,0,0,0,0,0,0,0,0,0,0],
  ["E",0,0,0,0,0,0,0,0,0,0,0,0,0],
  ["F",0,0,0,0,0,0,0,0,0,0,0,0,0],
  ["G",0,0,0,0,0,0,0,0,0,0,0,0,0],
  ["H",0,0,0,0,0,0,0,0,0,0,0,0,0],
  ["I",0,0,0,0,0,0,0,0,0,0,0,0,0],
  ["J",0,0,0,0,0,0,0,0,0,0,0,0,0],
  ["K",0,0,0,0,0,0,0,0,0,0,0,0,0],
  ["L",0,0,0,0,0,0,0,0,0,0,0,0,0],
  ["M",0,0,0,0,0,0,0,0,0,0,0,0,0],
  ["X","A","g","B","g","C","g","D","g","E","g","F","g","G","g","H","g","I","g","J","g","K","g","L","g","M"]
  ]

  earlyboard = await field(blankfield, "none")
  board = await minesweeperctx.send(earlyboard)
  
  mines = []
  while len(mines) < 25:
    mine = random.randint(0,169)
    if mine not in mines:
      mines.append(mine)
  
  for mine in mines:
    row = math.floor(mine/13)
    pcol = mine - (13*row)
    col = pcol + 1
    fieldrow = minefield[row]
    fieldrow[col] = 10

  for row in minefield:
      for i in range (len(row)):
        trueI = row[i]
        if str(trueI).isalpha() == False:
          if trueI == 11:
            number = 0
            thisRow = minefield.index(row)
            number = await bombsaround(thisRow, i,"first")
            row[i] = number
async def field(board, state):
  newboard=""
  for row in board:
    for i in row:
      newi = mkey[str(i)]
      newboard+=newi
    newboard+="\n"
  if state == "won":
    resolved = "You won!"
  elif state == "lost":
    resolved = "You lost!"
  else:
    resolved = ""
  newerboard = f'Minesweeper\n{resolved}\n{newboard}'
  return newerboard     
async def bombsaround(row, col, asker):
  if asker == "first":
    number = 0
  if row != 0:
    aboveRow = minefield[row - 1]
    if asker == "second" and aboveRow[col] != 10:
        await dig(mkey_list[row-1], mkey_list[col-1])
    elif aboveRow[col] == 10:
      if asker == "first":
        number += 1
    if col != 1:
      leftCol = (col-1)
      if asker == "second" and aboveRow[leftCol] != 10:
          await dig(mkey_list[row-1], mkey_list[col-2])
      elif aboveRow[leftCol] == 10:
        if asker == "first":
          number += 1
    if col != 13:
      rightCol = (col+1)
      if asker == "second" and aboveRow[rightCol] != 10:
          await dig(mkey_list[row-1], mkey_list[col])
      elif aboveRow[rightCol] == 10:
        if asker == "first":
          number += 1
  if row != 12:
    belowRow = minefield[row + 1]
    if asker == "second" and belowRow[col] != 10:
        await dig(mkey_list[row+1], mkey_list[col-1])
    elif belowRow[col] == 10:
      if asker == "first":
        number += 1
    if col != 1:
      leftCol = (col-1)
      if asker == "second" and belowRow[leftCol] != 10:
          await dig(mkey_list[row+1], mkey_list[col-2])
      elif belowRow[leftCol] == 10:
        if asker == "first":
          number += 1
    if col != 13:
      rightCol = (col+1)
      if asker == "second" and belowRow[rightCol] != 10:
          await dig(mkey_list[row+1], mkey_list[col])
      elif belowRow[rightCol] == 10:
        if asker == "first":
          number += 1
  thisRow = minefield[row]
  if col != 1:
    leftCol = (col-1)
    if asker == "second" and thisRow[leftCol] != 10:
        await dig(mkey_list[row], mkey_list[col-2])
    elif thisRow[leftCol] == 10:
      if asker == "first":
        number += 1
  if col != 13:
    rightCol = (col+1)
    if asker == "second" and thisRow[rightCol] != 10:
        await dig(mkey_list[row], mkey_list[col])
    elif thisRow[rightCol] == 10:
      if asker == "first":
        number += 1
  if asker == "first":
    if number == 0:
      number = 11
    return number      
async def checkWin():
  falseField = []
  for row in minefield:
    newrow=[]
    for i in row:
      if i == 10:
        newrow.append(9)
      else:
        newrow.append(i)
    falseField.append(newrow)
  if blankfield == falseField:
    return "won"
  else:
    return "none"
async def dig(row, col):
  nRow = mkey_list.index(row)
  nCol = mkey_list.index(col) + 1
  thisRow = blankfield[nRow]
  fakeRow = minefield[nRow]
  if thisRow[nCol] == 0:
    thisRow[nCol] = fakeRow[nCol]
    if thisRow[nCol] == 11:
      await bombsaround(nRow, nCol, "second")
    elif thisRow[nCol] == 10:
      state = "lost"
      return state
    state = await checkWin()
    return state
async def flag(row, col):
  nRow = mkey_list.index(row)
  nCol = mkey_list.index(col) + 1
  thisRow = blankfield[nRow]
  if thisRow[nCol] == 0:
    thisRow[nCol] = 9
  elif thisRow[nCol] == 9:
    thisRow[nCol] = 0
  else:
    await minesweeperctx.send("You cannot put a flag there")
  state = await checkWin()
  newboard = await field(blankfield, state)
  await board.edit(content=newboard)
async def trueDig(row, col):
  global active
  nRow = mkey_list.index(row)
  nCol = mkey_list.index(col) + 1
  thisRow = blankfield[nRow]
  if thisRow[nCol] != 0:
    await minesweeperctx.send("You cannot dig there")
  state = await dig(row, col)
  newboard = await field(blankfield, state)
  await board.edit(content=newboard)
  if state == "lost" or state =="won":
    active = False

global unoactive
unoactive = False
@bot.command(brief='Play uno with friends!', help='<@users>')
async def uno(ctx, *users: discord.User):
  global unoactive
  global risk
  global cards
  global hands
  global players
  global p
  global centercard
  global handcount
  global infoMessage
  global reverse
  global center
  global ukey_list
  global uval_list
  global centerwildColor
  global wildPlayer

  view = View()
  playingView = View()
  dealButton = Button(style=discord.ButtonStyle.green, label = "Start!")
  playButton = Button(style=discord.ButtonStyle.green, label = "Play!")
  view.add_item(dealButton)

  unoactive = True
  reverse = False
  p = 0
  handcount = 0
  players=[ctx.author.id]
  risk = [0]
  centerwildColor = ""
  wildPlayer = ""
  if len(users)==0:
    await ctx.send("You can't play uno alone, get friends")
    return
    
  file = open('cards.txt')
  cards = file.readlines()
  for i in cards:
    cards[cards.index(i)] = i.strip("\n")
    
  for user in users:
    id = user.id
    players.append(id)
    risk.append(0)

  hands = []
  for x in players:
    hands.append('')
  
  key = {
    "g" : "green",
    "b" : "blue",
    "y" : "yellow",
    "r" : "red"
  }
  ukey_list = list(key.keys())
  uval_list = list(key.values())

  async def createinfo():
    info="UNO!\n"
    for i in range(len(players)):
      player = players[i]
      info+= f"Player {i+1} ({len(hands[i])} cards): <@{player}>\n"
    info += f"It is Player {p+1}'s turn."
    if reverse == True:
      info += " The turn order is reversed!"
    return info
  info = await createinfo()
  infoMessage = await ctx.send(info)

  centercard = cards[random.randint(0,51)]
  center = await ctx.send(centercard, view=view)

  async def deal(interaction):
    global p
    global handcount
    global center
    author = interaction.user.id
    if (author in players) and (hands[players.index(author)] == ''):
      hand = []
      for i in range(7):
        randomCard = random.randint(0,55)
        hand.append(cards[randomCard])
      playerNumber = players.index(author)
      hands[playerNumber] = hand
      handcount +=1
    else:
      await interaction.response.defer()
    if len(players) == handcount:
      view.remove_item(dealButton)
      view.add_item(playButton)
      await center.edit(content = centercard, view=view)
    else: 
      await interaction.response.defer()

  async def cardChoice(interaction):
    global centercard
    global p
    global active
    global reverse
    global wildPlayer
    global centerwildColor
    playedCard = interaction.data["custom_id"]
    playedList = list(playedCard)
    playedColor = playedList[3]
    playedNumber = playedList[4]
    centerList = list(centercard)
    centerNumber = centerList[3]
    centerColor = centerList[2]
    if centerColor == "w":
      centerColor = centerwildColor
    if playedColor == "w":
      wildPlayer = interaction.user.id
    if (playedColor == centerColor) or (playedNumber == centerNumber) or (centerColor == "w") or (playedColor == "w"):
      del playedList[0]
      playedCard = "".join(playedList)
      hands[p].remove(playedCard)
      centercard = playedCard
      
      if len(hands[p]) == 0:
        await interaction.response.send_message(content=f"Player {p+1} wins!",ephemeral = False, view=None)
        await center.edit(content="Game Over!", view=None)
        active = False
      elif len(hands[p]) == 1:
        risk[p] = 1
      if playedNumber == "r":
        if reverse == True:
          reverse = False
        else:
          reverse = True
      elif playedNumber == "y":
        for i in range(4):
          x = random.randint(0,55)
          if reverse == False:
            hands[(p+1)%len(players)].append(cards[x])
          else:
            hands[(p-1)%len(players)].append(cards[x])
      elif playedNumber == "p":
        for i in range(2):
          x = random.randint(0,55)
          if reverse == False:
            hands[(p+1)%len(players)].append(cards[x])
          else:
            hands[(p-1)%len(players)].append(cards[x])
      if playedNumber == "s" or playedNumber == "p" or playedNumber == "y":
        if reverse == False:
          p+=1
        else:
          p-=1
        p = p%len(players)
      centerwildColor = ""
    else:
      x = random.randint(0,55)
      hands[p].append(cards[x])
    if reverse == False:
      p+=1
    else:
      p-=1
    p = p%len(players)
    info = await createinfo()
    await interaction.response.edit_message(content="Dismiss this message!",view=None)
    await infoMessage.edit(content = info)
    await center.edit(content = centercard, view=view)
    
  async def play(interaction):
    author = interaction.user.id
    global wildPlayer
    if author == players[p]:
      displayHand=""
      alpha=list('abcdefghijklmnopqrstuvwxyz')
      if wildPlayer!="":
        await interaction.response.defer()
        return
      for i in hands[p]:
        displayHand+=i
      playingView.clear_items()
      currentHand = hands[p]
      for i in range(len(currentHand)):
        cardButton = Button(style=discord.ButtonStyle.green, custom_id=f"{alpha[i]}{currentHand[i]}", emoji = currentHand[i])
        playingView.add_item(cardButton)
        cardButton.callback = cardChoice
      await center.edit(content = centercard, view=None)
      await interaction.response.send_message(content = displayHand, ephemeral=True, view = playingView)
    else:
      await interaction.response.defer()
  dealButton.callback = deal
  playButton.callback = play
@bot.event
async def on_message(message):
  global active
  if active == True:
    if message.author.id == player:
      message2 = str(message.content)
      message2 = message2.split(" ")
      tag = list(message2[0])
      if tag[0] == "#":
        if len(message2) == 2:
          location = list(message2[1])
          if message2[0] == "#dig":
            if (location[0].upper() in mkey_list) and (location[1].upper() in mkey_list):
              row = location[0].upper()
              col = location[1].upper()
              await trueDig(row, col)
              await message.delete()
            else:
              await minesweeperctx.send("invalid move")
          elif message2[0] == "#flag":
            if (location[0].upper() in mkey_list) and (location[1].upper() in mkey_list):
              row = location[0].upper()
              col = location[1].upper()
              await flag(row, col)
              await message.delete()
            else:
              await minesweeperctx.send("invalid move")
          else:
            await minesweeperctx.send("Use #dig (location) or #flag (location) to move!")
        else:
            await minesweeperctx.send("Use #dig (location) or #flag (location) to move")
  global unoactive
  global players
  global risk
  global hands
  global cards
  global wildPlayer
  global centerwildColor
  if unoactive == True:
    if message.content.lower() == "uno":
      currentPlayer = players.index(message.author.id)
      if risk[currentPlayer] == 1:
        risk[currentPlayer] = 0
      if risk[currentPlayer] == 0:
        if 1 in risk:
          target=risk.index(1)
          for i in range(4):
            x = random.randint(0,51)
            hands[target].append(cards[x])
          risk[target] = 0
    if (wildPlayer == message.author.id):
      if message.content.lower() in uval_list:
        centerwildColor = ukey_list[uval_list.index(message.content.lower())]
        wildPlayer = ""
  await bot.process_commands(message)
    

@bot.command(brief='Play z9 says!', help='')
async def simon(ctx):
  global simonPlayer
  global playable
  global terminal
  global sampleterminal
  global sequence
  global tempsequence
  sequence = []
  tempsequence = []
  playable = False
  simonPlayer = ctx.author.id
  terminal = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
  ]
  sampleterminal = [
    [1,2,3,4,5],
    [2,1,2,3,4],
    [3,2,1,2,3],
    [4,3,2,1,2],
    [5,4,3,2,1]
  ]
  
  
  key = {
    "0" : "⬜",
    "1" : "🟥",
    "2" : "🟧",
    "3" : "🟨",
    "4" : "🟩",
    "5" : "🟦"
  }

  async def convert():
    displayTerminal=""
    for row in terminal:
      for i in row:
        newi = key[str(i)]
        displayTerminal+=newi
      displayTerminal+="\n"
    return displayTerminal

  simonView=View()
  async def simon():
    await displayHelp.edit(content="z9 is thinking...")
    global playable
    global terminal
    global sampleterminal
    global sequence
    playable = False

    n=random.randint(0,24)
    sequence.append(n)

    for i in sequence:
      x = i%5
      y = int((i-x)/5)
      terminal[y][x] = sampleterminal[y][x]
      newterminal = await convert()
      await displayBoard.edit(content=newterminal, view=simonView)
      time.sleep(1)
      terminal[y][x] = 0
    newterminal = await convert()
    await displayBoard.edit(content=newterminal, view=simonView)
    await displayHelp.edit(content=f"Recall the sequence! ({len(sequence)})")
    playable = True

  async def click(interaction):
    global playable
    global sequence
    global tempsequence
    if (interaction.user.id == simonPlayer) and (playable == True):
      position = alpha.index(interaction.data["custom_id"])
      tempsequence.append(position)
      if len(tempsequence) == len(sequence):
        if tempsequence == sequence:
          tempsequence=[]
          await interaction.response.defer()
          await simon()
        else:
          await interaction.response.send_message(content=f"You Lost! Your score: {len(sequence)}")
          playable = False
      else:
        await interaction.response.defer()
    else:
      await interaction.response.defer()


  alpha=list('abcdefghijklmnopqrstuvwxyz')
  numbers=list('1234521234321234321254321')
  for i in range(25):
    switch = Button(style=discord.ButtonStyle.gray, custom_id=alpha[i], emoji = key[numbers[i]])
    simonView.add_item(switch)
    switch.callback = click

  displayHelp = await ctx.send("z9 is thinking...")
  displayTerminal = await convert()
  displayBoard = await ctx.send(content=displayTerminal, view=simonView)
  await simon()

bot.run(${{secrets.API_KEY}})
