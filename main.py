# -*- coding: utf-8 -*-
"""
Main - Point d'entrée de l'application Prix Goncourt 2025
"""

import sys
from typing import List, Dict
from business.goncourt import GoncourtService


class GoncourtApplication:
    """
    Classe principale de l'application console.
    Gère l'affichage des menus et la navigation.
    """

    def __init__(self):
        self.service = GoncourtService()
        self.running = True

    def run(self) -> None:
        """
        Méthode principale qui lance l'application.
        """
        print("\n" + "=" * 60)
        print("PRIX GONCOURT 2025 - APPLICATION DE GESTION")
        print("=" * 60)

        while self.running:
            self.show_main_menu()

    def show_main_menu(self) -> None:
        """
        Affiche le menu principal selon l'utilisateur courant.
        """
        print(f"\n{'=' * 60}")
        print(f"MODE: {self.service.current_user.user_type.upper()}")
        print(f"{'=' * 60}")

        menu_options = self.service.get_current_user_menu()

        for key, (description, _) in menu_options.items():
            print(f"{key}. {description}")

        print("0. Quitter l'application")

        choice = input("\nVotre choix: ").strip()

        if choice == "0":
            self.quit_application()
        elif choice in menu_options:
            method_name = menu_options[choice][1]
            self.execute_menu_action(method_name)
        else:
            print("✗ Choix invalide. Veuillez réessayer.")

    def execute_menu_action(self, method_name: str) -> None:
        """
        Exécute l'action correspondant au choix du menu.

        Args:
            method_name (str): Nom de la méthode à exécuter
        """
        try:
            if method_name == "changer_mode":
                self.change_mode()
            elif method_name == "afficher_premiere_selection":
                self.show_premiere_selection()
            elif method_name == "afficher_deuxieme_selection":
                self.show_deuxieme_selection()
            elif method_name == "afficher_troisieme_selection":
                self.show_troisieme_selection()
            elif method_name == "afficher_toutes_selections":
                self.show_all_selections()
            elif method_name == "afficher_resultats_finale":
                self.show_final_results()
            elif method_name == "creer_deuxieme_selection":
                self.create_deuxieme_selection()
            elif method_name == "creer_troisieme_selection":
                self.create_troisieme_selection()
            elif method_name == "enregistrer_votes_finale":
                self.record_final_votes()
            else:
                print("✗ Action non implémentée.")
        except Exception as e:
            print(f"✗ Erreur lors de l'exécution: {e}")

    # === ACTIONS VISITEUR ===

    def change_mode(self) -> None:
        """
        Change le mode d'utilisateur.
        """
        current_mode = self.service.current_user.user_type
        new_mode = "president" if current_mode == "visitor" else "visitor"

        if new_mode == "president":
            success = self.service.change_user_mode("president")
            if success:
                print("✓ Mode président activé")
        else:
            self.service.change_user_mode("visitor")
            print("✓ Mode visiteur activé")

    def show_premiere_selection(self) -> None:
        """
        Affiche la première sélection.
        """
        selection = self.service.get_premiere_selection()
        self.service.display_selection(selection, show_details=True)

    def show_deuxieme_selection(self) -> None:
        """
        Affiche la deuxième sélection.
        """
        selection = self.service.get_deuxieme_selection()
        if selection:
            self.service.display_selection(selection, show_details=True)
        else:
            print("\nLa deuxième sélection n'a pas encore été établie.")

    def show_troisieme_selection(self) -> None:
        """
        Affiche la troisième sélection.
        """
        selection = self.service.get_troisieme_selection()
        if selection:
            self.service.display_selection(selection, show_details=True)
        else:
            print("\nLa troisième sélection n'a pas encore été établie.")

    def show_all_selections(self) -> None:
        """
        Affiche toutes les sélections existantes.
        """
        selections = self.service.get_all_selections()

        if not selections:
            print("\nAucune sélection disponible.")
            return

        for selection in selections:
            self.service.display_selection(selection, show_details=False)
            print()  # Ligne vide entre les sélections

    def show_final_results(self) -> None:
        """
        Affiche les résultats du dernier tour.
        """
        self.service.display_final_results()

    # === ACTIONS PRÉSIDENT ===

    def create_deuxieme_selection(self) -> None:
        """
        Crée la deuxième sélection (8 livres).
        """
        # Vérifier l'état actuel
        state = self.service.get_current_state()
        if not state["premiere_selection"]:
            print("✗ La première sélection doit exister avant de créer la deuxième.")
            return

        if state["deuxieme_selection"]:
            print("✗ La deuxième sélection existe déjà.")
            replace = input("Voulez-vous la recréer? (o/n): ").lower()
            if replace != 'o':
                return

        # Afficher les livres disponibles (de la première sélection)
        available_books = self.service.get_available_books_for_selection(2)

        if not available_books:
            print("✗ Aucun livre disponible pour la deuxième sélection.")
            return

        print(f"\n{'=' * 60}")
        print("CRÉATION DE LA DEUXIÈME SÉLECTION (8 livres)")
        print(f"{'=' * 60}")
        print("\nLivres disponibles (première sélection):")

        for i, book in enumerate(available_books, 1):
            print(f"{i}. {book.b_title} - {book.author.full_name() if book.author else 'Inconnu'}")

        print("\nEntrez les numéros des 8 livres à sélectionner (séparés par des virgules):")
        selection_input = input("Votre choix: ").strip()

        try:
            # Convertir l'entrée en liste d'indices
            indices = [int(idx.strip()) - 1 for idx in selection_input.split(',')]

            # Valider
            if len(indices) != 8:
                print("✗ Vous devez sélectionner exactement 8 livres.")
                return

            for idx in indices:
                if idx < 0 or idx >= len(available_books):
                    print(f"✗ Indice {idx + 1} invalide.")
                    return

            # Récupérer les IDs des livres sélectionnés
            selected_book_ids = [available_books[idx].b_id for idx in indices]

            # Créer la sélection
            success = self.service.create_deuxieme_selection(selected_book_ids)

            if success:
                print("✓ Deuxième sélection créée avec succès!")
                # Créer automatiquement la sélection finale (tour 4)
                self.service.create_final_selection()
            else:
                print("✗ Échec de la création de la deuxième sélection.")

        except ValueError:
            print("✗ Format invalide. Veuillez entrer des numéros séparés par des virgules.")
        except Exception as e:
            print(f"✗ Erreur: {e}")

    def create_troisieme_selection(self) -> None:
        """
        Crée la troisième sélection (4 livres).
        """
        # Vérifier l'état actuel
        state = self.service.get_current_state()
        if not state["deuxieme_selection"]:
            print("✗ La deuxième sélection doit exister avant de créer la troisième.")
            return

        if state["troisieme_selection"]:
            print("✗ La troisième sélection existe déjà.")
            replace = input("Voulez-vous la recréer? (o/n): ").lower()
            if replace != 'o':
                return

        # Afficher les livres disponibles (de la deuxième sélection)
        available_books = self.service.get_available_books_for_selection(3)

        if not available_books:
            print("✗ Aucun livre disponible pour la troisième sélection.")
            return

        print(f"\n{'=' * 60}")
        print("CRÉATION DE LA TROISIÈME SÉLECTION (4 livres)")
        print(f"{'=' * 60}")
        print("\nLivres disponibles (deuxième sélection):")

        for i, book in enumerate(available_books, 1):
            print(f"{i}. {book.b_title} - {book.author.full_name() if book.author else 'Inconnu'}")

        print("\nEntrez les numéros des 4 livres à sélectionner (séparés par des virgules):")
        selection_input = input("Votre choix: ").strip()

        try:
            # Convertir l'entrée en liste d'indices
            indices = [int(idx.strip()) - 1 for idx in selection_input.split(',')]

            # Valider
            if len(indices) != 4:
                print("✗ Vous devez sélectionner exactement 4 livres.")
                return

            for idx in indices:
                if idx < 0 or idx >= len(available_books):
                    print(f"✗ Indice {idx + 1} invalide.")
                    return

            # Récupérer les IDs des livres sélectionnés
            selected_book_ids = [available_books[idx].b_id for idx in indices]

            # Créer la sélection
            success = self.service.create_troisieme_selection(selected_book_ids)

            if success:
                print("✓ Troisième sélection créée avec succès!")
                # Mettre à jour la sélection finale
                self.service.create_final_selection()
            else:
                print("✗ Échec de la création de la troisième sélection.")

        except ValueError:
            print("✗ Format invalide. Veuillez entrer des numéros séparés par des virgules.")
        except Exception as e:
            print(f"✗ Erreur: {e}")

    def record_final_votes(self) -> None:
        """
        Enregistre les votes du dernier tour.
        """
        # Vérifier l'état actuel
        state = self.service.get_current_state()
        if not state["final_selection"]:
            print("✗ La sélection finale (tour 4) doit exister avant d'enregistrer les votes.")
            return

        # Récupérer la sélection finale
        finale_selection = self.service.selection_dao.find_by_round(4)
        if not finale_selection or len(finale_selection.book) != 4:
            print("✗ La sélection finale doit contenir 4 livres.")
            return

        print(f"\n{'=' * 60}")
        print("ENREGISTREMENT DES VOTES DU DERNIER TOUR")
        print(f"Nombre de membres du jury: 10")
        print(f"{'=' * 60}")

        print("\nFinalistes (4 livres):")
        for i, book in enumerate(finale_selection.book, 1):
            print(f"{i}. {book.b_title} - {book.author.full_name() if book.author else 'Inconnu'}")

        print("\nEntrez le nombre de voix pour chaque livre (la somme doit être 10):")

        votes_data = {}
        total_votes = 0

        for i, book in enumerate(finale_selection.book, 1):
            while True:
                try:
                    votes = int(input(f"Voix pour le livre {i} ({book.b_title}): "))
                    if votes < 0:
                        print("✗ Le nombre de voix ne peut pas être négatif.")
                        continue

                    votes_data[book.b_id] = votes
                    total_votes += votes
                    break
                except ValueError:
                    print("✗ Veuillez entrer un nombre entier.")

        # Vérifier le total
        if total_votes != 10:
            print(f"\n✗ Le total des votes ({total_votes}) doit être exactement 10.")
            return

        # Confirmation
        print(f"\nRécapitulatif des votes:")
        for book in finale_selection.book:
            print(f"  {book.b_title}: {votes_data[book.b_id]} voix")

        confirm = input("\nConfirmer l'enregistrement? (o/n): ").lower()
        if confirm != 'o':
            print("✗ Enregistrement annulé.")
            return

        # Enregistrer les votes
        success = self.service.record_final_votes(votes_data)
        if success:
            print("✓ Votes enregistrés avec succès!")
            print("✓ Le prix Goncourt 2025 a été attribué!")
        else:
            print("✗ Échec de l'enregistrement des votes.")

    def quit_application(self) -> None:
        """
        Quitte proprement l'application.
        """
        print("\nMerci d'avoir utilisé l'application Prix Goncourt 2025.")
        print("Au revoir!")
        self.running = False

    def show_current_state(self) -> None:
        """
        Affiche l'état actuel de l'application.
        """
        state = self.service.get_current_state()

        print(f"\n{'=' * 60}")
        print("ÉTAT ACTUEL DE L'APPLICATION")
        print(f"{'=' * 60}")

        status_icons = {True: "✓", False: "✗"}

        print(f"\nSélections:")
        print(f"  Première sélection (15 livres): {status_icons[state['premiere_selection']]}")
        print(f"  Deuxième sélection (8 livres): {status_icons[state['deuxieme_selection']]}")
        print(f"  Troisième sélection (4 livres): {status_icons[state['troisieme_selection']]}")
        print(f"  Sélection finale (4 finalistes): {status_icons[state['final_selection']]}")

        print(f"\nVotes:")
        print(f"  Votes du dernier tour enregistrés: {status_icons[state['votes_recorded']]}")


# Point d'entrée
if __name__ == "__main__":
    try:
        app = GoncourtApplication()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrompue.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErreur critique: {e}")
        sys.exit(1)