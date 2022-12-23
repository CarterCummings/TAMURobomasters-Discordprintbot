import os
import discord
from datetime import date


client = discord.Client()

# FILE STRUCTURE
# entries seporated by newline (\n)
# members seporated by #

def writeQueue(subteam,currQueue):
  f = open(str(subteam)+"printqueue.txt", "w")
  for i in currQueue:
      f.write(i[0] + "#" + i[1] + "#" + i[2] + "#" + i[3] + "#" + i[4] + "\n")
  f.close()

def get_queue(subteam):
  f = open(str(subteam)+"printqueue.txt", "w+")
  fileContent = f.read().split("\n")
  printQueue = []
  if (fileContent == []):
    f.close()
    return printQueue
  for i in fileContent:

      printQueue.append(i.split("#"))

  f.close()
  return printQueue

def add_to_queue(user,dateAdded,printFile = " ",claimedBy = "No one", subteam = " ", quantity = 0):
  newPrint = [printFile, str(user), str(dateAdded), str(claimedBy), quantity]
  f = open(str(subteam)+"printqueue.txt", "a")
  f.write(str(newPrint[0]) + "#" + str(newPrint[1]) + "#" + str(newPrint[2]) + "#" + str(newPrint[3]) + "#" + str(newPrint[4]) + "\n")
  f.close()

def claimPrint(subteam,user,printID):
  currQueue = get_queue(subteam)
  if printID >= len(currQueue):
    #print(len(db[("printQueue"+str(subteam))]))
    return 1
  else:
    currQueue[printID][3] = user
    return 0


def del_from_queue(subteam,printID):
  currQueue = get_queue(subteam)
  if printID >= len(currQueue):
    #print(len(db[("printQueue"+str(subteam))]))
    return 1
  else:
    currQueue.pop(printID)
    writeQueue(currQueue)
    return 0

def nuke_queue(subteam):
  f = open(str(subteam)+"printqueue.txt","w")
  f.write("")
  f.close()


@client.event
async def on_ready():
  print("Starting up {0.user}".format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith("!printbothelp"):
    await message.channel.send("Print requests are shared by any channel in a discord category\n!addprint: attach the file to be printed with the command. Takes in number of copies needed. If none is given default is 1\n!claimprint: give a printID to claim a print to work on\n!printqueue: reads out the current print queue.\n!finishprint: takes in the num ID of the print to be removed from the queue.\n!nukequeue: can only be used by someone with the \"Officers\" tag. Deletes the whole queue.")

  if message.content.startswith("!printqueue"):
    await message.channel.send("Active Print Requests: ")
    messageBuffer = ""
    subteam = message.channel.category
    printQueue = get_queue(subteam)
    #print(printQueue)

    if (len(printQueue) != 0 and printQueue != [[""]] ):
      for i in range((len(printQueue)-1)):
        messageBuffer += ("Created by: " + str(printQueue[i][1]) + " on " + str(printQueue[i][2]) + " ID: " + str(i) + " Claimed by: " + str(printQueue[i][3]) + " Quantity: " + str(printQueue[i][4]) )
        messageBuffer += ("\n")
        messageBuffer += str(printQueue[i][0])
        messageBuffer += ("\n")
      await message.channel.send(messageBuffer)
    else:
      await message.channel.send("Queue is empty")



  if message.content.startswith("!claimprint"):
    try:
      printID = int(message.content.split("!claimprint ",1)[1])

      subteam = str(message.channel.category)
      user = message.author.display_name
      if (claimPrint(subteam,user,printID) == 1):
        await message.channel.send("Invalid Print ID")
      else:
        await message.channel.send("You have claimed Print: "+ str(printID))
    except:
      await message.channel.send("Claim invalid")

  if message.content.startswith("!addprint"):
    try:
      quantity = int(message.content.split("!addprint ",1)[1])
    except:
      quantity = 1
    if (len(message.attachments) == 0):
      await message.channel.send("No file included")

    for i in message.attachments:

      if (str(i.url))[-4:] != ".stl":
        await message.channel.send("Invalid File")
        continue
      printFile = ""
      try:
        printFile = i.url
      except:

        break

      user = message.author.display_name
      dateAdded = date.today()
      subteam = message.channel.category
      claimedBy = "No one"
      add_to_queue(user,dateAdded,printFile,claimedBy,subteam,quantity)
      await message.channel.send("Printed added to queue")

  if message.content.startswith("!finishprint"):
    try:
      printID = int(message.content.split("!finishprint ",1)[1])
      subteam = str(message.channel.category)
      if del_from_queue(printID,subteam) == 1:
        await message.channel.send("Invalid Print ID")
      else:
        await message.channel.send("Print has been finished")
    except:
      await message.channel.send("Invalid Command")

  if message.content.startswith("!removeprint"):
    try:
      printID = int(message.content.split("!removeprint ",1)[1])
      subteam = str(message.channel.category)
      if del_from_queue(printID,subteam) == 1:
        await message.channel.send("Invalid Print ID")
      else:
        await message.channel.send("Print Removed from Queue")
    except:
      await message.channel.send("Invalid Command")

  if message.content.startswith("!nukequeue"):
    Officer = False;
    for i in message.author.roles:
      if str(i) == "Officers":
        Officer = True;
    if Officer:
      nuke_queue(str(message.channel.category))
      await message.channel.send("Queue has been nuked. I hope you can live with yourself.")
    else:
      await message.channel.send("You wish you had the power.")



client.run("_____________________________") # This has been left blank as it is the key to the bot and that would be a problem if it was public 
