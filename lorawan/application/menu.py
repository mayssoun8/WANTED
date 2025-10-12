from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import subprocess
import os
from InquirerPy import inquirer

console = Console()

# Définition du chemin vers les fichiers .ino
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Récupère le dossier du script
SNIFFING_INO_PATH = os.path.join(SCRIPT_DIR, "..", "attaques", "attaque_par_rejeu", "replay_arduino", "arduino_sniffer", "arduino_sniffer.ino")
REPLAY_INO_PATH = os.path.join(SCRIPT_DIR, "..", "attaques", "attaque_par_rejeu", "replay_arduino", "arduino_player", "arduino_player.ino")
BASIC_ATTACK_INO_PATH = os.path.join(SCRIPT_DIR, "..", "attaques", "attaque_cles_basiques", "arduino", "attaqueArduino.ino")

# Variables de configuration (avec des valeurs par défaut)
port = "/dev/ttyACM1"  # Port par défaut
baud_rate = "9600"  # Vitesse par défaut

def flash_arduino(ino_path):
    """Flashe un fichier .ino donné sur l'Arduino avec les paramètres configurés"""
    command = ["arduino", "--upload", ino_path, "--port", port]

    console.print(f"[bold yellow]Flashage en cours...[/bold yellow] ({ino_path})")

    try:
        subprocess.run(command, check=True)
        console.print("[bold green]Flashage réussi ![/bold green]")

        ## ABANDON LANCEMENT MINICOM POUR L'INSTANT ##
        """
        # Lancer Minicom avec les paramètres configurés
        console.print("[bold yellow]Lancement de Minicom...[/bold yellow]")
        minicom_command = ["minicom", "-D", port, "-b", baud_rate]  # Utilise le port et la vitesse configurés
        subprocess.Popen(minicom_command)  # Utilisation de Popen pour ne pas bloquer l'exécution
        """

    except subprocess.CalledProcessError:
        console.print("[bold red]Erreur lors du flashage.[/bold red] Vérifie la connexion et le port.")

def configure_arduino():
    """Permet de configurer le port et la vitesse de l'Arduino"""
    global port, baud_rate  # Pour pouvoir modifier les variables globales

    # Demander le port
    new_port = Prompt.ask(f"Entrez le port (actuel : {port})")
    if new_port:
        port = new_port

    # Demander la vitesse
    new_baud_rate = Prompt.ask(f"Entrez la vitesse (actuelle : {baud_rate})", default=baud_rate)
    if new_baud_rate:
        baud_rate = new_baud_rate

    console.print(f"[bold green]Configuration mise à jour :[/bold green] Port = {port}, Vitesse = {baud_rate}")

def configuration_menu():
    """Menu de configuration avec sous-menu pour l'Arduino"""
    while True:
        option = inquirer.select(
            "Que voulez-vous configurer ?",
            choices=[
                "Configurer le port et la vitesse de l'Arduino",
                "Retour",
            ],
        ).execute()

        if option == "Configurer le port et la vitesse de l'Arduino":
            configure_arduino()  # Appel de la fonction de configuration
        elif option == "Retour":
            break

def display_menu():
    """Affiche le menu principal avec un titre stylisé et navigation par flèches"""
    console.print(Panel("Reproduction d'attaques LoRaWAN", style="bold blue"))

    option = inquirer.select(
        "Sélectionnez une option :",
        choices=[
            "Sniffing",
            "Usurpation d'identité sur clés basiques",
            "Jamming",
            "Replay",
            "Scénarios (non implémentés)",
            "Configuration",
            "Quitter",
        ],
    ).execute()

    if option == "Sniffing":
        console.print("Vous avez choisi Sniffing", style="bold green")
        flash_arduino(SNIFFING_INO_PATH)
    elif option == "Usurpation d'identité sur clés basiques":
        console.print("Vous avez choisi Usurpation d'identité sur clés basiques", style="bold green")
        flash_arduino(BASIC_ATTACK_INO_PATH)
    elif option == "Jamming":
        console.print("Vous avez choisi Jamming", style="bold green")
    elif option == "Replay":
        console.print("Vous avez choisi Replay", style="bold green")
        flash_arduino(REPLAY_INO_PATH)
    elif option == "Scénarios (non implémentés)":
        console.print("Scénarios (non implémentés)", style="bold yellow")
    elif option == "Configuration":
        configuration_menu()  # Appel du sous-menu de configuration
    elif option == "Quitter":
        console.print("Au revoir!", style="bold red")
        exit()

def main():
    while True:
        display_menu()

if __name__ == "__main__":
    main()
