# -*- coding: utf-8 -*-
"""
GoncourtService - Service principal de l'application Goncourt
"""

from typing import List, Optional, Dict
from datetime import date
from models.book import Book
from models.selection import Selection
from models.vote import Vote
from models.user import Visitor, President
from daos.book_dao import BookDAO
from daos.selection_dao import SelectionDAO
from daos.vote_dao import VoteDAO


class GoncourtService:
    """
    Couche principale de l'application (couche métier du Prix Goncourt).
    """

    def __init__(self):
        self.book_dao = BookDAO()
        self.selection_dao = SelectionDAO()
        self.vote_dao = VoteDAO()
        self.current_user = Visitor()

        # Initialiser la première sélection si elle n'existe pas
        self._initialize_first_selection()

    def _initialize_first_selection(self) -> None:
        """
        Initialise la première sélection avec les 15 livres de départ.
        Appelée uniquement au démarrage de l'application.
        """
        premiere_selection = self.selection_dao.find_by_round(1)
        if not premiere_selection:
            # Récupérer tous les livres (les 15 premiers)
            all_books = self.book_dao.read_all()

            # Créer la première sélection
            premiere_selection = Selection(
                s_id=0,
                s_name="PREMIÈRE SÉLECTION",
                s_round=1,
                s_date=date(2025, 9, 3),
                book=all_books
            )

            # Sauvegarder en base
            selection_id = self.selection_dao.create(premiere_selection)
            if selection_id:
                print("✓ Première sélection initialisée avec 15 livres")

    def change_user_mode(self, mode: str) -> bool:
        """
        Change le mode d'utilisateur (visiteur/president).

        Args:
            mode (str): 'visitor' ou 'president'

        Returns:
            bool: True si le changement a réussi
        """
        if mode == 'visitor':
            self.current_user = Visitor()
            return True
        elif mode == 'president':
            # Vérification du mot de passe (simplifiée pour l'exercice)
            password = input("Mot de passe président: ")
            if password == "president2025":  # À remplacer par une vraie authentification
                self.current_user = President()
                return True
            else:
                print("✗ Mot de passe incorrect")
                return False
        return False

    def get_current_user_menu(self) -> Dict[str, tuple]:
        """
        Retourne le menu correspondant à l'utilisateur courant.

        Returns:
            Dict[str, tuple]: Options de menu
        """
        return self.current_user.get_menu_options()

    # === MÉTHODES POUR VISITEUR ===

    def get_premiere_selection(self) -> Optional[Selection]:
        """
        Récupère la première sélection (15 livres).

        Returns:
            Optional[Selection]: La première sélection ou None
        """
        return self.selection_dao.find_by_round(1)

    def get_deuxieme_selection(self) -> Optional[Selection]:
        """
        Récupère la deuxième sélection (8 livres).

        Returns:
            Optional[Selection]: La deuxième sélection ou None
        """
        return self.selection_dao.find_by_round(2)

    def get_troisieme_selection(self) -> Optional[Selection]:
        """
        Récupère la troisième sélection (4 livres).

        Returns:
            Optional[Selection]: La troisième sélection ou None
        """
        return self.selection_dao.find_by_round(3)

    def get_all_selections(self) -> List[Selection]:
        """
        Récupère toutes les sélections existantes.

        Returns:
            List[Selection]: Liste de toutes les sélections
        """
        return self.selection_dao.read_all()

    def get_final_results(self) -> List[Vote]:
        """
        Récupère les résultats du dernier tour.

        Returns:
            List[Vote]: Liste des votes triés par nombre de voix
        """
        return self.vote_dao.get_final_results()

    def display_selection(self, selection: Selection, show_details: bool = True) -> None:
        """
        Affiche une sélection de manière formatée.

        Args:
            selection (Selection): La sélection à afficher
            show_details (bool): Afficher les détails complets des livres
        """
        if not selection:
            print("Aucune sélection disponible.")
            return

        print(f"\n{'=' * 60}")
        print(f"{selection.get_round_name()}")
        print(f"Date: {selection.s_date.strftime('%d/%m/%Y') if selection.s_date else 'Non définie'}")
        print(f"Nombre de livres: {selection.books_number()}")
        print(f"{'=' * 60}")

        if not selection.book:
            print("Aucun livre dans cette sélection.")
            return

        for i, book in enumerate(selection.book, 1):
            print(f"\n{i}. {book.b_title}")
            print(f"   Auteur: {book.author.full_name() if book.author else 'Inconnu'}")
            print(f"   Éditeur: {book.editor.e_name if book.editor else 'Inconnu'}")

            if show_details:
                print(f"   ISBN: {book.isbn}")
                print(f"   Date de parution: {book.b_publication_date}")
                print(f"   Pages: {book.b_number_pages or 'Non renseigné'}")
                print(f"   Prix: {book.price_formatted()}")

                if book.b_summary:
                    # Limiter la longueur du résumé
                    summary = book.b_summary[:150] + "..." if len(book.b_summary) > 150 else book.b_summary
                    print(f"   Résumé: {summary}")

                if book.b_main_characters_list:
                    characters = ", ".join(book.b_main_characters_list)
                    print(f"   Personnages: {characters}")

    def display_final_results(self) -> None:
        """
        Affiche les résultats du dernier tour de scrutin.
        """
        votes = self.get_final_results()

        if not votes:
            print("\nAucun résultat disponible pour le dernier tour.")
            return

        print(f"\n{'=' * 60}")
        print("RÉSULTATS DU DERNIER TOUR DE SCRUTIN")
        print("(Prix Goncourt 2025)")
        print(f"{'=' * 60}")

        total_votes = sum(vote.v_number_vote for vote in votes)

        for i, vote in enumerate(votes, 1):
            percentage = (vote.v_number_vote / total_votes * 100) if total_votes > 0 else 0
            print(f"\n{i}. {vote.book.b_title}")
            print(f"   Auteur: {vote.book.author.full_name() if vote.book.author else 'Inconnu'}")
            print(f"   Votes: {vote.v_number_vote} ({percentage:.1f}%)")

        # Afficher le gagnant
        if votes:
            winner = votes[0]
            print(f"\n{'=' * 60}")
            print(f"🏆 PRIX GONCOURT 2025 ATTRIBUÉ À :")
            print(f"   « {winner.book.b_title} »")
            print(f"   de {winner.book.author.full_name() if winner.book.author else 'Inconnu'}")
            print(f"   avec {winner.v_number_vote} voix")
            print(f"{'=' * 60}")

    # === MÉTHODES POUR PRÉSIDENT ===

    def create_deuxieme_selection(self, book_ids: List[int]) -> bool:
        """
        Crée la deuxième sélection avec 8 livres.

        Args:
            book_ids (List[int]): Liste des IDs des 8 livres à sélectionner

        Returns:
            bool: True si la création a réussi
        """
        if len(book_ids) != 8:
            print("✗ La deuxième sélection doit contenir exactement 8 livres.")
            return False

        # Vérifier que les livres existent
        books = []
        for book_id in book_ids:
            book = self.book_dao.read(book_id)
            if not book:
                print(f"✗ Livre avec ID {book_id} non trouvé.")
                return False
            books.append(book)

        # Vérifier que la première sélection existe
        premiere = self.selection_dao.find_by_round(1)
        if not premiere:
            print("✗ La première sélection doit exister avant de créer la deuxième.")
            return False

        # Vérifier que les livres sont dans la première sélection
        premiere_book_ids = [b.b_id for b in premiere.book]
        for book_id in book_ids:
            if book_id not in premiere_book_ids:
                print(f"✗ Le livre avec ID {book_id} n'est pas dans la première sélection.")
                return False

        # Créer la deuxième sélection
        deuxieme_selection = Selection(
            s_id=0,
            s_name="DEUXIÈME SÉLECTION",
            s_round=2,
            s_date=date(2025, 10, 7),
            book=books
        )

        selection_id = self.selection_dao.create(deuxieme_selection)
        if selection_id:
            print(f"✓ Deuxième sélection créée avec {len(books)} livres")
            return True

        return False

    def create_troisieme_selection(self, book_ids: List[int]) -> bool:
        """
        Crée la troisième sélection avec 4 livres.

        Args:
            book_ids (List[int]): Liste des IDs des 4 livres à sélectionner

        Returns:
            bool: True si la création a réussi
        """
        if len(book_ids) != 4:
            print("✗ La troisième sélection doit contenir exactement 4 livres.")
            return False

        # Vérifier que les livres existent
        books = []
        for book_id in book_ids:
            book = self.book_dao.read(book_id)
            if not book:
                print(f"✗ Livre avec ID {book_id} non trouvé.")
                return False
            books.append(book)

        # Vérifier que la deuxième sélection existe
        deuxieme = self.selection_dao.find_by_round(2)
        if not deuxieme:
            print("✗ La deuxième sélection doit exister avant de créer la troisième.")
            return False

        # Vérifier que les livres sont dans la deuxième sélection
        deuxieme_book_ids = [b.b_id for b in deuxieme.book]
        for book_id in book_ids:
            if book_id not in deuxieme_book_ids:
                print(f"✗ Le livre avec ID {book_id} n'est pas dans la deuxième sélection.")
                return False

        # Créer la troisième sélection
        troisieme_selection = Selection(
            s_id=0,
            s_name="TROISIÈME SÉLECTION",
            s_round=3,
            s_date=date(2025, 10, 28),
            book=books
        )

        selection_id = self.selection_dao.create(troisieme_selection)
        if selection_id:
            print(f"✓ Troisième sélection créée avec {len(books)} livres")
            return True

        return False

    def create_final_selection(self) -> bool:
        """
        Crée la sélection finale (tour 4) avec les 4 finalistes.

        Returns:
            bool: True si la création a réussi
        """
        # Vérifier que la troisième sélection existe
        troisieme = self.selection_dao.find_by_round(3)
        if not troisieme:
            print("✗ La troisième sélection doit exister avant de créer la sélection finale.")
            return False

        if len(troisieme.book) != 4:
            print("✗ La troisième sélection doit contenir 4 livres.")
            return False

        # Créer la sélection finale (identique à la troisième mais tour 4)
        finale_selection = Selection(
            s_id=0,
            s_name="FINALISTES DU PRIX GONCOURT",
            s_round=4,
            s_date=date(2025, 11, 4),  # Date de la remise du prix
            book=troisieme.book
        )

        selection_id = self.selection_dao.create(finale_selection)
        if selection_id:
            print("✓ Sélection finale créée avec les 4 finalistes")
            return True

        return False

    def record_final_votes(self, votes_data: Dict[int, int]) -> bool:
        """
        Enregistre les votes du dernier tour.

        Args:
            votes_data (Dict[int, int]): Dictionnaire {book_id: nombre_de_voix}

        Returns:
            bool: True si l'enregistrement a réussi
        """
        # Vérifier que la sélection finale existe
        finale_selection = self.selection_dao.find_by_round(4)
        if not finale_selection:
            print("✗ La sélection finale doit exister avant d'enregistrer les votes.")
            return False

        # Vérifier que les livres sont dans la sélection finale
        finale_book_ids = [b.b_id for b in finale_selection.book]
        for book_id in votes_data.keys():
            if book_id not in finale_book_ids:
                print(f"✗ Le livre avec ID {book_id} n'est pas dans la sélection finale.")
                return False

        # Vérifier que le nombre total de votes est raisonnable (ex: 10 membres du jury)
        total_votes = sum(votes_data.values())
        if total_votes != 10:  # Le jury Goncourt a 10 membres
            print(f"✗ Le total des votes doit être exactement 10 (nombre de membres du jury).")
            print(f"  Total actuel: {total_votes}")
            return False

        # Enregistrer les votes
        success = self.vote_dao.record_final_votes(
            votes_data,
            finale_selection.s_id,
            date.today()
        )

        if success:
            print("✓ Votes enregistrés avec succès")
            return True

        return False

    def get_available_books_for_selection(self, round_number: int) -> List[Book]:
        """
        Récupère les livres disponibles pour une sélection.

        Args:
            round_number (int): Numéro du tour (1, 2, 3)

        Returns:
            List[Book]: Liste des livres disponibles
        """
        if round_number == 1:
            # Pour la première sélection, tous les livres sont disponibles
            return self.book_dao.read_all()
        elif round_number == 2:
            # Pour la deuxième, les livres de la première sélection
            premiere = self.selection_dao.find_by_round(1)
            return premiere.book if premiere else []
        elif round_number == 3:
            # Pour la troisième, les livres de la deuxième sélection
            deuxieme = self.selection_dao.find_by_round(2)
            return deuxieme.book if deuxieme else []
        else:
            return []

    def get_current_state(self) -> Dict:
        """
        Retourne l'état actuel de l'application.

        Returns:
            Dict: État contenant les sélections existantes
        """
        state = {
            "premiere_selection": self.selection_dao.find_by_round(1) is not None,
            "deuxieme_selection": self.selection_dao.find_by_round(2) is not None,
            "troisieme_selection": self.selection_dao.find_by_round(3) is not None,
            "final_selection": self.selection_dao.find_by_round(4) is not None,
            "votes_recorded": len(self.vote_dao.get_final_results()) > 0
        }
        return state