# -*- coding: utf-8 -*-

"""
Class Vote
"""

from dataclasses import dataclass
from datetime import date
from models.book import Book
from models.selection import Selection

@dataclass
class Vote:
    """
    Modèle représentant un vote pour un livre dans une sélection.

    Attributs:
        v_id (int): Identifiant unique du vote.
        v_number_vote (int): Nombre de votes obtenus.
        v_date_vote (date): Date du vote.
        book (Book): Livre concerné par le vote.
        selection (Selection): Sélection à laquelle le vote appartient.
    """
    v_id: int
    v_number_vote: int
    v_date_vote: date
    book: Book
    selection: Selection

    def __str__(self) -> str:
        """
        Retourne une représentation textuelle du vote.

        Return:
            str: Titre du livre suivi du nombre de voix.
        """
        return f"{self.book.b_title}: {self.v_number_vote} voix"
