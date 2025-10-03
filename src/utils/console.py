import os
import sys
from typing import List


class ConsoleMenu:
    def print_header(self, title: str):
        """Affiche l'en-tête du menu"""
        print("\n" + "="*50)
        print(f"{title:^50}")
        print("="*50 + "\n")

    def print_options(self, options: list):
        """Affiche les options du menu"""
        for option in options:
            print(option)
        print()

    def get_choice(self, prompt: str = "Votre choix: ") -> str:
        """Récupère le choix de l'utilisateur"""
        return input(prompt)

    def get_input(self, prompt: str) -> str:
        """Récupère une entrée utilisateur"""
        return input(prompt)

    def wait_for_user(self):
        """Attend que l'utilisateur appuie sur une touche"""
        input("\nAppuyez sur Entrée pour continuer...")


def clear_screen():
    """Efface l'écran de la console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_progress(current: int, total: int):
    """Affiche une barre de progression (tolère total == 0)"""
    bar_length = 40
    if total <= 0:
        filled_length = bar_length
        percent = 100
    else:
        filled_length = int(bar_length * current // total)
        percent = int(100 * current / total)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f"\rProgression: |{bar}| {current}/{total} ({percent}%)")
    sys.stdout.flush()
    if total > 0 and current >= total:
        print()  # newline when done
    elif total <= 0:
        print()
