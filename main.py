#Les installations
!pip install discord.py
!pip install nest_asyncio 
import nest_asyncio 
nest_asyncio.apply()


#----------------------------------------------------------Les fonctionnalités du bot-------------------------------------------
#***********************************Les fonctionnalités basiques(celles demandées dans les livrables)****************************
# Le bot peut :
#   ⁃   Être lancé via la commande /Jouer à tout moment quand le jeu n'est pas encore lancé 
#   ⁃   Poser une série de questions à l’utilisateur (5)
#   ⁃   Récupérer ses réponses et lui donner des points si la réponse est bonne
#   ⁃   Afficher un indice sur l’énigme courante si l’utilisateur le demande
#   ⁃   Afficher son score total lorsque toutes les énigmes ont été réalisées
#   ⁃   Afficher son score actuel avec la commande "/score"
#   ⁃   Relancer le quizz depuis le début avec la commande "/reset game"
#*********************************** Les fonctionnalités ajoutées ****************************
#Le bot peut :
# - Informer un nouveau utilisateur qui salue les membres du groupe de comment lancer le jeu
# - Envoyer des photos
# - Définir une durée maximale de 150 secondes pour finir les quiz (En quelque sorte, un timer caché à l'utilisateur)
# - Envoyez des boutons éphémères 
# - Permettre d'aller directement sur le web à travers l'espace de jeu
# - Assurer la logique dans le jeu
# - Autoriser certaines actions juste pour ridiculiser l'utilisateur
# - A travers les indices, permettre à l'utilisateur de savoir s'il est chanceux ou pas (Test de chance)
# - etc...

#--------------------------------------------------------------------------------- Le Développement -------------------------------------------------------------------------------------------------

import discord
#De la documentation discord.ui nous importons les classes ou fonctionnalités buttton et view
from discord.ui import Button, View
#importation de la classe des commandes pour tout ce qui concernerne les commandes utilisées dans ce jeu 
from discord.ext import commands
#definition de notre bot
bot = commands.Bot(command_prefix = "/", intents = discord.Intents.all())

#Importation de la bibliothèque asyncio pour l'usage des fonctions coroutines
import asyncio
#Importation de la bibliothèque datetime pour tout ce qui concerne l'heure
import time
#Definition de la fonction on_message grace au décorateur .listen() qui d'après la documentation discord.py permet au bot d'écouter les événements.
#C'est un peu l'équivalent de @client.event du Client mais en mode Bot
@bot.listen()
async def on_message(message):
#Dans la suite, c'est un peu fréquent ce genre d'annalyse, nous savons qu'à la fin du jeu nous enverrons ce message donc nous définissons que lorsqu'il se fera entendu, nous calculerons et enverrons les points.  
#Pour le calcul, nous envoyons un type de petit message à l'utilisateur pour le féliciter de sa victoire, ce qu'il ne peut savoir est que ce message est codé
#C'est l'écoute de ce message qui définit son point et puisqu'à chaque message du channel, le système reprend de zéro, la seule chose qui reste est l'historique 
#là où on va chercher ses messages et incrémenter les points selon le type de message envoyé à l’utilisateur.
#Bien vrai, il n'y a pas de système sans faille jusqu’à ce qu'on lui en trouve; en gros seul les initiés comme celui qui lit ces écritures connait la faille.
#Même si c'est pas possible qu'il sache comment ça marche derrière le système de points, nous avons mis des barrières dans la suite pour qu'il n'entre pas ces types de message.
#Après tout, l'utilisateur n'a pas assez de droits dans le channel comme celui de supprimer les messages d'un administrateur tel le Bot; ce qui maintient toute la logique du jeu.
  if "👏 Nous sommes à la fin de notre jeu 👏" == message.content :
    point = 0
    point1 = 0
    point2 = 0
    async for messages in message.channel.history() :
      if "Miammm" in messages.content or "Youpiiiiiiii" in messages.content or "Mes félicitations" in messages.content:
        if point2 < 20 :
          point1 = point1 + 4
          point2 = point1
        elif point2 > 20 :
          await message.channel.send("Vous avez bidouillé le jeu dans son processus ")
          await message.channel.send("Vous pensez qu'on s'en appercevrait pas😒?")
          await message.channel.send("Veuillez recommencer le jeu avec la commande «/reset game»")

    async for messages in message.channel.history() :
      if "Bravooooooo" in messages.content :
        if point2 < 20 :
          point2 = point2 + 2
        elif point2 > 20 :
          await message.channel.send("Vous avez bidouillé le jeu dans son processus ")
          await message.channel.send("Vous pensez qu'on s'en appercevrait pas😒?")
          await message.channel.send("Veuillez recommencer le jeu avec la commande «/reset game»")

    await message.channel.send("Votre score total est : " + str(point2) + " sur 20")      
    await message.channel.send("Vous pouvez recommencer le jeu avec la commande «/reset game»") 
  if "*Un pirate en a toujours une. Que c'est?*" == message.content:
    channel = message.channel
    def check(m):
      return "👏 Nous sommes à la fin de notre jeu 👏" == m.content and  m.channel == channel
    try:
      msg = await bot.wait_for('message', timeout=150.0, check=check)
    except asyncio.TimeoutError:
      await channel.send("🤧🤧🤧🤧🤧Time over❗️")
      await channel.send("....... Réinitialisation dans 5 secondes")
      await asyncio.sleep(2)
      await channel.send("Veuillez recommencer dans un instant")
      await asyncio.sleep(3)
      await channel.purge(limit= None)
    else:
      await channel.send("😎Cool! Vous avez fini dans les délais")

                #le reste est pareil à la logique précédente 
#Attention⚠️, nous sommes le groupe pour lequel, la fonction flatten() posait de problème sur l'une de nos marchines
#Dans la peur que ça ne marche pas de votre côté, nous avons découvert qu'elle a été retirée de la bibliothèque python malgré que ça marche sur l'une de nos marchines
#Nous l'avons catégoriquement changé pour éviter le pire, nous avons utilisé un raisonnement assez mathématique puisque nous n'arrivons pas à récupérer l’historique en liste, défaut de flatten()
  if "Let's Go 🥳" == message.content :
    channel= message.channel
    i = 1
    J = 1
    async for messages in channel.history() :
      if "Let's Go 🥳" in messages.content and i != 1 :
        J += 1
        await channel.send("https://i.imgur.com/8peTjjI.png")
        return await channel.send("T'es minable 😂")
      i+=1
    if J == 1 :
      await channel.send("https://i.imgur.com/oxkSref.png")
      await channel.send("*Un pirate en a toujours une. Que c'est?*")

      button1 = Button(style = discord.ButtonStyle.danger,label ="Indice❗️")
      button2= Button(label = "Le web, c'est par ici!",url="https://google.com")
      async def button1_callback(interaction):
        await interaction.response.send_message(content="/insErer1 indice1", view=None)
      button1.callback=button1_callback
      view=View()
      view.add_item(button1)
      view.add_item(button2)
      await message.channel.send("", view=view)

  if "/insErer1 indice1" == message.content :
    i = 1
    J = 1
    async for messages in message.channel.history() :
      if "/insErer1 indice1" in messages.content  and i != 1 :
        J += 1
        await message.channel.send("https://i.imgur.com/8peTjjI.png")
        return await message.channel.send("Je ne crois pas que ça puisse marcher 🤣🤣🤣🤣😂!")
      i+=1
    if J == 1 :
      button1 = Button(style = discord.ButtonStyle.blurple,label ="Boucle d'oreille")
      button2 = Button(style = discord.ButtonStyle.grey,label ="Baguette")
      button3 = Button(style = discord.ButtonStyle.green,label ="Bateau")
      async def button1_callback(interaction):
        await message.channel.send("Passons à la seconde")
        await interaction.response.edit_message(content="Bravooooooo, continue comme ça 😻", view=None)
      button1.callback = button1_callback
      async def button2_callback(interaction):
        await message.channel.send("Passons à la seconde")
        await interaction.response.edit_message(content="Mauvais choix, vous venez d'échouer l'énigme , du courage 🫶🥲", view=None)
      button2.callback = button2_callback
      async def button3_callback(interaction):
        await message.channel.send("Passons à la seconde")
        await interaction.response.edit_message(content="Mauvais choix, vous venez d'échouer l'énigme , du courage 🫶🥲", view=None)
      button3.callback = button3_callback
      view = View()
      view.add_item(button2)
      view.add_item(button3)
      view.add_item(button1)
      await message.channel.send("", view=view)
 

  if "Passons à la seconde" == message.content :
    if message.author != bot.user :
      return
    await asyncio.sleep(3)
    await message.channel.send("https://i.imgur.com/8ttXLHL.png")
    await message.channel.send("*Les sorcières ne s’en servent pas pour faire le ménage. Que c'est?*")
    button1 = Button(style = discord.ButtonStyle.danger,label ="Indice❗️")
    button2= Button(label = "Le web, c'est par ici!",url="https://google.com")
    async def button1_callback(interaction):
      await interaction.response.send_message(content="/inserer2 indIce2", view=None)
    button1.callback=button1_callback
    view=View()
    view.add_item(button1)
    view.add_item(button2)
    await message.channel.send("", view=view)

  if "/inserer2 indIce2" == message.content :
    i = 1
    J = 1
    async for messages in message.channel.history() :
      if "/inserer2 indIce2" in messages.content  and i != 1 :
        J += 1
        await message.channel.send("https://i.imgur.com/8peTjjI.png")
        return await message.channel.send("Je ne crois pas que ça puisse marcher 🤣🤣🤣🤣😂!")
      i+=1
    if J == 1 :
      button1 = Button(style = discord.ButtonStyle.danger,label ="   ")
      button2 = Button(style = discord.ButtonStyle.grey,label ="   ")
      button3 = Button(style = discord.ButtonStyle.green,label ="   ")
      async def button1_callback(interaction):
        await message.channel.send("Passons à la troisième")
        await interaction.response.edit_message(content="Bravooooooo, bonne suite 😻", view=None)
      button1.callback = button1_callback
      async def button2_callback(interaction):
        await message.channel.send("Passons à la troisième")
        await interaction.response.edit_message(content="Mauvais choix, vous venez d'échouer l'énigme , bonne suite 🫶🥲", view=None)
      button2.callback = button2_callback
      async def button3_callback(interaction):
        await message.channel.send("Passons à la troisième")
        await interaction.response.edit_message(content="Mauvais choix, vous venez d'échouer l'énigme , bonne suite 🫶🥲", view=None)
      button3.callback = button3_callback
      view = View()
      view.add_item(button1)
      view.add_item(button3)
      view.add_item(button2)
      await message.channel.send("Choisissez une couleur et laissez la chance vous suivre 😂", view=view)
 

  if "Passons à la troisième" == message.content :
    if message.author != bot.user :
      return
    await asyncio.sleep(3)
    await message.channel.send("https://i.imgur.com/YGI7s6M.png")
    await message.channel.send("*Je pleure quand on me tourne la tête. Qui suis-je?*")
    button1 = Button(style = discord.ButtonStyle.danger,label ="Indice❗️")
    button2= Button(label = "Le web, c'est par ici!",url="https://google.com")
    async def button1_callback(interaction):
      await interaction.response.send_message(content="/insérer3 INdiCe3", view=None)
    button1.callback=button1_callback
    view=View()
    view.add_item(button1)
    view.add_item(button2)
    await message.channel.send("", view=view)

  if "/insérer3 INdiCe3" == message.content :
    i = 1
    J = 1
    async for messages in message.channel.history() :
      if "/insérer3 INdiCe3" in messages.content  and i != 1 :
        J += 1
        await message.channel.send("https://i.imgur.com/8peTjjI.png")
        return await message.channel.send("Je ne crois pas que ça puisse marcher 🤣🤣🤣🤣😂!")
      i+=1
    if J == 1 :
      button1 = Button(style = discord.ButtonStyle.blurple,label ="Le clou")
      button2 = Button(style = discord.ButtonStyle.green,label ="Le robinet")
      button3 = Button(style = discord.ButtonStyle.grey,label ="Le ventilateur")
      async def button2_callback(interaction):
        await message.channel.send("Passons à l'avant dernière")
        await interaction.response.edit_message(content="Bravooooooo, encore quelques efforts 😻", view=None)
      button2.callback = button2_callback
      async def button1_callback(interaction):
        await message.channel.send("Passons à l'avant dernière")
        await interaction.response.edit_message(content="Mauvais choix, vous venez d'échouer l'énigme , c'est encore possible 🫶🥲", view=None)
      button1.callback = button1_callback
      async def button3_callback(interaction):
        await message.channel.send("Passons à l'avant dernière")
        await interaction.response.edit_message(content="Mauvais choix, vous venez d'échouer l'énigme , c'est encore possible 🫶🥲", view=None)
      button3.callback = button3_callback
      view = View()
      view.add_item(button1)
      view.add_item(button3)
      view.add_item(button2)
      await message.channel.send("La réponse est l'une de ces propositions :", view=view)
 


  if "Passons à l'avant dernière" == message.content :
    if message.author != bot.user :
      return
    await asyncio.sleep(3)
    await message.channel.send("https://i.imgur.com/eJ8mM8A.png")
    await message.channel.send("*Je ne peux pas marcher, j’ai pourtant un dos et quatre pieds. Qui suis-je?*")
    button1 = Button(style = discord.ButtonStyle.danger,label ="Indice❗️")
    button2= Button(label = "Le web, c'est par ici!",url="https://google.com")
    async def button1_callback(interaction):
      await interaction.response.send_message(content="/inserer4 InDicE4", view=None)
    button1.callback=button1_callback
    view=View()
    view.add_item(button1)
    view.add_item(button2)
    await message.channel.send("", view=view)

  if "/inserer4 InDicE4" == message.content :
    i = 1
    J = 1
    async for messages in message.channel.history() :
      if "/inserer4 InDicE4" in messages.content  and i != 1 :
        J += 1
        await message.channel.send("https://i.imgur.com/8peTjjI.png")
        return await message.channel.send("Je ne crois pas que ça puisse marcher 🤣🤣🤣🤣😂!")
      i+=1
    if J == 1 :
      button1 = Button(style = discord.ButtonStyle.danger,label ="La table")
      button2 = Button(style = discord.ButtonStyle.green,label ="Le bossu")
      button3 = Button(style = discord.ButtonStyle.grey,label ="La chaise")
      async def button3_callback(interaction):
        await message.channel.send("... La dernière dans 2 secondes ...")
        await interaction.response.edit_message(content="Bravooooooo, encore quelques efforts 😻", view=None)
      button3.callback = button3_callback
      async def button1_callback(interaction):
        await message.channel.send("... La dernière dans 2 secondes ...")
        await interaction.response.edit_message(content="Mauvaise réponse, vous venez d'échouer l'avant dernière , c'est encore possible 🫶🥲", view=None)
      button1.callback = button1_callback
      async def button2_callback(interaction):
        await message.channel.send("... La dernière dans 2 secondes ...")
        await interaction.response.edit_message(content="Mauvaise réponse, vous venez d'échouer l'avant dernière , c'est encore possible 🫶🥲", view=None)
      button2.callback = button2_callback
      view = View()
      view.add_item(button1)
      view.add_item(button3)
      view.add_item(button2)
      await message.channel.send("La réponse est l'une de ces propositions :", view=view)
 

  if "... La dernière dans 2 secondes ..." == message.content :
    if message.author != bot.user :
      return
    await asyncio.sleep(3)
    await message.channel.send("https://i.imgur.com/IiLy64a.png")
    await message.channel.send("*J’ai toujours bonne mine. Qui suis-je ?*")
    button1 = Button(style = discord.ButtonStyle.danger,label ="Indice❗️")
    button2= Button(label = "Une petite recherche ?",url="https://google.com")
    async def button1_callback(interaction):
      await interaction.response.send_message(content="/inseRer5 InDicE5", view=None)
    button1.callback=button1_callback
    view=View()
    view.add_item(button1)
    view.add_item(button2)
    await message.channel.send("", view=view)

  if "/inseRer5 InDicE5" == message.content :
    i = 1
    J = 1
    async for messages in message.channel.history() :
      if "/inseRer5 InDicE5" in messages.content  and i != 1 :
        J += 1
        await message.channel.send("https://i.imgur.com/8peTjjI.png")
        return await message.channel.send("Je ne crois pas que ça puisse marcher 🤣🤣🤣🤣😂!")
      i+=1
    if J == 1 :
      button4 = Button(style = discord.ButtonStyle.gray,label ="🙄")
      button1 = Button(style = discord.ButtonStyle.danger,label ="🥲")
      button2 = Button(style = discord.ButtonStyle.green,label ="🤣")
      button3 = Button(style = discord.ButtonStyle.blurple,label ="🫣")
      async def button3_callback(interaction):
        await message.channel.send("👏 Nous sommes à la fin de notre jeu 👏")
        await message.channel.send("https://i.imgur.com/e9UPGR4.png")
        await interaction.response.edit_message(content="Bravooooooo😻", view=None)
      button3.callback = button3_callback
      async def button1_callback(interaction):
        await message.channel.send("👏 Nous sommes à la fin de notre jeu 👏")
        await message.channel.send("https://i.imgur.com/e9UPGR4.png")
        await interaction.response.edit_message(content="Rho la_la🤧. Travaille ta chance 😅 ", view=None)
      button1.callback = button1_callback
      async def button2_callback(interaction):
        await message.channel.send("👏 Nous sommes à la fin de notre jeu 👏")
        await message.channel.send("https://i.imgur.com/e9UPGR4.png")
        await interaction.response.edit_message(content="Rho la_la🤧. Travaille ta chance 😅 ", view=None)
      button2.callback = button2_callback
      async def button4_callback(interaction):
        await message.channel.send("👏 Nous sommes à la fin de notre jeu 👏")
        await message.channel.send("https://i.imgur.com/e9UPGR4.png")
        await interaction.response.edit_message(content="Rho la_la🤧. Travaille ta chance 😅 ", view=None)
      button4.callback = button4_callback
      view = View()
      view.add_item(button1)
      view.add_item(button3)
      view.add_item(button2)
      view.add_item(button4)
      await message.channel.send("Une de ces boutons comporte la réponse. Voyons, à qui la chance 😅?:", view=view)
 

  if "boucle d'oreille" in message.content.lower() :
    channel= message.channel
    i = 1
    J = 1
    async for messages in channel.history() :
      if "boucle d'oreille" in messages.content.lower() and i != 1 :
        J += 1
        await channel.send("https://i.imgur.com/la2jC4y.png")
        return await channel.send("Désolé tricheur😒, la route est bloquée😎")
      elif ("Mauvais choix, vous venez d'échouer l'énigme , du courage 🫶🥲" == messages.content or "Bravooooooo, continue comme ça 😻" == messages.content or "/insErer1 indice1" == messages.content) and i != 1 :
        J = J + 1
        return await channel.send("Oups, nous n'encourageons pas la tricherie 🙄")
      i+=1
    if J == 1 :
      emoji = '😻'
      await message.add_reaction(emoji)            
      await channel.send("Youpiiiiiiii 😼 Capitaine 🫡, tu as 4 points")
      await asyncio.sleep(3)
      await channel.send("https://i.imgur.com/8ttXLHL.png")
      await channel.send("*Les sorcières ne s’en servent pas pour faire le ménage. Que c'est?*")
      button1 = Button(style = discord.ButtonStyle.danger,label ="Indice❗️")
      button2= Button(label = "Le Web, c'est par ici !",url="https://google.com")
      async def button1_callback(interaction):
        await interaction.response.send_message(content="/inserer2 indIce2", view=None)
      button1.callback=button1_callback
      view=View()
      view.add_item(button1)
      view.add_item(button2)
      await message.channel.send("", view=view)
  
  if "chaise" in message.content.lower() :
    channel= message.channel
    i = 1
    J = 1
    async for messages in channel.history() :
      if "chaise" in messages.content.lower() and i != 1 :
        J += 1
        await channel.send("https://i.imgur.com/la2jC4y.png")
        return await channel.send("Désolé tricheur😒, la route est bloquée😎")
      elif ("Mauvaise réponse, vous venez d'échouer l'avant dernière , c'est encore possible 🫶🥲" == messages.content or "Bravooooooo, encore quelques efforts 😻" == messages.content or "/inserer4 InDicE4" == messages.content) and i != 1 :
        J = J + 1
        return await channel.send("Oups, nous n'encourageons pas la tricherie 🙄")
      i+=1
    if J == 1 :
      emoji = '🫡'
      await message.add_reaction(emoji)            
      await channel.send("Mes félicitations😍, tu viens d'avoir 4 points de plus")
      await asyncio.sleep(3)
      await channel.send("https://i.imgur.com/IiLy64a.png")
      await channel.send("*J’ai toujours bonne mine. Qui suis-je ?*")
      button1 = Button(style = discord.ButtonStyle.danger,label ="Indice❗️")
      button2= Button(label = "Une petite recherche ?",url="https://google.com")
      async def button1_callback(interaction):
        await interaction.response.send_message(content="/inseRer5 InDicE5", view=None)
      button1.callback=button1_callback
      view=View()
      view.add_item(button1)
      view.add_item(button2)
      await message.channel.send("", view=view)

  if "balais" in message.content.lower() :
    channel= message.channel
    i = 1
    J = 1
    async for messages in channel.history() :
      if "balais" in messages.content.lower() and i != 1 :
        J += 1
        await channel.send("https://i.imgur.com/la2jC4y.png")
        return await channel.send("Désolé tricheur😒, la route est bloquée😎")
      elif ("Mauvais choix, vous venez d'échouer l'énigme , bonne suite 🫶🥲" == messages.content or "Bravooooooo, bonne suite 😻" == messages.content or "/inserer2 indIce2" == messages.content)and i != 1 :
        J = J + 1
        return await channel.send("Oups, nous n'encourageons pas la tricherie 🙄")
      i+=1
    if J == 1 :
      emoji = '🫠'
      await message.add_reaction(emoji)
      await channel.send("https://i.imgur.com/03FiNHP.png")
      await channel.send("Miammm🫠,bon boulot, tu as 4 points de plus")
      await asyncio.sleep(3)
      await channel.send("https://i.imgur.com/YGI7s6M.png")
      await channel.send("*Je pleure quand on me tourne la tête. Qui suis-je?*")
      button1 = Button(style = discord.ButtonStyle.danger,label ="Indice❗️")
      button2= Button(label = "Une petite recherche ?",url="https://google.com")
      async def button1_callback(interaction):
        await interaction.response.send_message(content="/insérer3 INdiCe3", view=None)
      button1.callback=button1_callback
      view=View()
      view.add_item(button1)
      view.add_item(button2)
      await message.channel.send("", view=view)

  if "crayon" in message.content.lower() :
    channel= message.channel
    i = 1
    J = 1
    async for messages in channel.history() :
      if "crayon" in messages.content.lower() and i != 1 :
        J += 1
        await channel.send("https://i.imgur.com/la2jC4y.png")
        return await channel.send("Désolé tricheur😒, la route est bloquée😎")
      elif ("Rho la_la🤧. Travaille ta chance 😅 " == messages.content or "Bravooooooo😻" == messages.content or "/inseRer5 InDicE5" == messages.content) and i != 1 :
        J = J + 1
        return await channel.send("Oups, nous n'encourageons pas la tricherie 🙄")
      i+=1
    if J == 1 :
      emoji = '😻'
      await message.add_reaction(emoji)
      await channel.send("Youpiiiiiiii pour ce succès, tu as 4 points")
      await channel.send("-------------------")
      await channel.send("👏 Nous sommes à la fin de notre jeu 👏")
      await channel.send("https://i.imgur.com/e9UPGR4.png")

  if "robinet" in message.content.lower() :
    channel= message.channel
    i = 1
    J = 1
    async for messages in channel.history() :
      if "robinet" in messages.content.lower() and i != 1 :
        J += 1
        await channel.send("https://i.imgur.com/la2jC4y.png")
        return await channel.send("Désolé tricheur😒, la route est bloquée😎")
      elif ("Mauvais choix, vous venez d'échouer l'énigme , c'est encore possible 🫶🥲" == messages.content or "Bravooooooo, encore quelques efforts 😻" == messages.content or "/insérer3 INdiCe3" == messages.content) and i != 1 :
        J = J + 1
        return await channel.send("Oups, nous n'encourageons pas la tricherie 🙄")
      i+=1
    if J == 1 :
      emoji = '🥳'
      await message.add_reaction(emoji)            
      await channel.send("Mes félicitations😍, tu viens d'avoir 4 points, intéressant 🤔 ")
      await asyncio.sleep(3)
      await channel.send("https://i.imgur.com/eJ8mM8A.png")
      await channel.send("*Je ne peux pas marcher, j’ai pourtant un dos et quatre pieds. Qui suis-je?*")
      button1 = Button(style = discord.ButtonStyle.danger,label ="Indice❗️")
      button2= Button(label = "Une petite recherche ?",url="https://google.com")
      async def button1_callback(interaction):
        await interaction.response.send_message(content="/inserer4 InDicE4", view=None)
      button1.callback=button1_callback
      view=View()
      view.add_item(button1)
      view.add_item(button2)
      await message.channel.send("", view=view)

  #Ce qui suit permet d'informer le nouveau membre de sa prochaine étape losqu'il salut sur le serveur
  if "coucou" in message.content.lower() or "hello"  in message.content.lower() or "bonjour" in message.content.lower() or "hi" in message.content.lower() or "wesh" in message.content.lower() or "salut" in message.content.lower() or "yoo" in message.content.lower():
    channel= message.channel
    i = 1
    J = 1
    async for messages in channel.history() :
      if "Pour accéder à l'espace de jeu, tapez «/Jouer»" in messages.content and i != 1 :
        J += 1
        return await channel.send("Combien de fois tu vas nous saluer 🤷‍♂️ ?")
      i+=1
    if J == 1 :
      emoji = '👋'
      await message.add_reaction(emoji)
      await message.channel.send(f'Ohé, @{message.author}!')
      await message.channel.send("Pour accéder à l'espace de jeu, tapez «/Jouer»")

        #Supression de messages comportants les str incrémenteurs de points non autaurisés à l'utilisateur 
  if "Miammm" in message.content or "Youpiiiiiiii" in message.content or "Mes félicitations" in message.content or "Bravooooooo" in message.content:
    if message.author == bot.user :
      return 
    await message.delete()
#-------------------------------- ma fonction check pour savoir si oui, le joueur a envie de continuer le jeu ou pas.
  if "/Jouer" == message.content:
    channel = message.channel
    i = 1
    J = 1
    async for messages in channel.history() :
      if "/Jouer" == messages.content and i != 1 :
        J = J+1
        return await channel.send("Combien de fois tu vas le faire 🤷‍♂️?")
      i+=1
    if J == 1 :
      await channel.send("Bienvenue dans cette partie de jeu 🫣.")
      await channel.send("https://i.imgur.com/RMSjXw0.png")      
      await channel.send('Êtes-vous prêt(e) à affronter nos énigmes😍?')
      def check(m):
        return "oui" in m.content.lower() and  m.channel == channel
      try:
        msg = await bot.wait_for('message', timeout=10.0, check=check)
      except asyncio.TimeoutError:
        await channel.send("Apparemment, vous n'êtes pas prêt(e)🤧")
        await channel.send("Essayez la commande «/reset game» pour continuer le jeu")
      else:
        await channel.send(f'Parfait, {msg.author}🥲!')
        await channel.send("Vous avez 2min30sec pour terminer le Quiz, sinon c'est un échec quelque soit votre score🤧")
        await asyncio.sleep(2)
        await channel.send("Pour commencer, il est nécessaire que vous connaissiez la règle du jeu🫠")
        await asyncio.sleep(2)
        await channel.send("https://i.imgur.com/tkg8HDR.png")
        await channel.send("Il est temps de savoir ce que vous savez faire 😉😎")
        await asyncio.sleep(5)
        button = Button(style = discord.ButtonStyle.success,label ="Nos Enigmes")
        async def button_callback(interaction):
          await interaction.response.send_message(content="Let's Go 🥳", view=None)
        button.callback = button_callback
        view = View()
        view.add_item(button)
        await channel.send("", view = view)

#-------------------------------------------------------------Pour recommencer le jeu----------------------------------------------------------------
@bot.command()
async def reset(ctx,*,arg) :
  if arg == "game" :
    await ctx.channel.purge(limit= None)
    await ctx.send("Si vous êtes ici, soit vous avez envie de recommencer,soit vous avez échoué soit vous dormiez un instant!")
    await asyncio.sleep(2)
    await ctx.send("https://i.imgur.com/tkg8HDR.png")
    await asyncio.sleep(2)
    button = Button(style = discord.ButtonStyle.green,label ="Nos Enigmes")
    async def button_callback(interaction):
      await interaction.response.send_message(content="Let's Go 🥳", view=None)
    button.callback = button_callback
    view = View()
    view.add_item(button)
    await ctx.send("", view = view)

@bot.command()
async def Jouer(ctx):
  return
#--------------------------------------------------Commande de calcul et d'affichage des points -----------------------------------


@bot.command()
async def score(ctx) :
  if ctx.author == bot.user :
    return      
  point = 0
  point1 = 0
  point2 = 0
  async for messages in ctx.channel.history() :
    if "Miammm" in messages.content or "Youpiiiiiiii" in messages.content or "Mes félicitations" in messages.content:
      if point2 < 20 :
        point1 = point1 + 4
        point2 = point1
      elif point2 > 20 :
        await ctx.send("Vous avez bidouillé le jeu dans son processus ")
        await ctx.send("Vous pensez qu'on s'en appercevrait pas😒?")
        await ctx.send("Veuillez recommencer le jeu avec la commande «/reset game»")

  async for messages in ctx.channel.history() :
    if "Bravooooooo" in messages.content :
      if point2 < 20 :
        point2 = point2 + 2
      elif point2 > 20 :
        await ctx.send("Vous avez bidouillé le jeu dans son processus ")
        await ctx.send("Vous pensez qu'on s'en appercevrait pas😒?")
        await ctx.send("Veuillez recommencer le jeu avec la commande «/reset game»")

  await ctx.send("Votre score actuel est : " + str(point2) + " sur 20")      

bot.run("Votre_Token_ici")
