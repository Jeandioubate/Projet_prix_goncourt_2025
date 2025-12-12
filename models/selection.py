# -*- coding: utf-8 -*-

"""
Class Selection
"""

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional
from models.book import Book

@dataclass
class Selection:
    """
    Modèle représentant une sélection de livres.

    Attributs:
        s_id (int): Identifiant unique de la sélection.
        s_name (str): Nom de la sélection.
        s_round (int): Numéro du tour de la sélection.
        s_date (Optional[date]): Date de la sélection.
        book (List[Book]): Liste des livres appartenant à la sélection.
    """

    s_id: int
    s_name: str
    s_round: int
    s_date: Optional[date] = None
    book: List[Book] = field(default_factory=list)

    def __str__(self) -> str:
        """Retourne une représentation textuelle de la sélection"""
        date_str = self.s_date.strftime("%d/%m/%Y") if self.s_date else "Date non définie"
        return f"{self.s_name} (Tour {self.s_round}) - {date_str}"

    def add_book(self, book: Book) -> None:
        """Ajoute un livre à la sélection s'il n'y est pas déjà"""

        if book not in self.book:
            self.book.append(book)

    def remove_book(self, book: Book) -> bool:
        """Retire un livre de la sélection

        Return:
            bool: True si le livre a été retiré, False s'il n'était pas présent.
        """
        if book in self.book:
            self.book.remove(book)
            return True
        return False

    def books_number(self) -> int:
        """Retourne le nombre de livres dans la sélection"""
        return len(self.book)

    def get_round_name(self) -> str:
        """Retourne le nom du tour selon son numéro"""
        noms = {
            1: "PREMIÈRE SÉLECTION",
            2: "DEUXIÈME SÉLECTION",
            3: "TROISIÈME SÉLECTION",
            4: "FINALISTES DU PRIX GONCOURT"
        }
        return noms.get(self.s_round, f"Tour {self.s_round}")
