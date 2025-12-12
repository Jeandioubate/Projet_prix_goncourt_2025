# -*- coding: utf-8 -*-

"""
Class Book
"""

from dataclasses import dataclass, field
from typing import Optional, List
from decimal import Decimal
from models.author import Author
from models.editor import Editor


@dataclass
class Book:
    """
    Modèle représentant un livre.

    Attributs:
        b_id (int): Identifiant unique du livre.
        isbn (str): Numéro ISBN du livre.
        b_title (str): Titre du livre.
        b_summary (Optional[str]): Résumé du livre.
        b_publication_date (str): Date de parution sous format texte.
        b_number_pages (Optional[int]): Nombre de pages.
        b_editor_price (Optional[Decimal]): Prix éditeur du livre.
        author (Optional[Auteur]): Auteur du livre.
        editor (Optional[Editeur]): Éditeur du livre.
        b_main_characters_list (List[str]): Liste structurée des personnages.
    """

    b_id: int
    isbn: str
    b_title: str
    b_summary: Optional[str] = None
    b_publication_date: str = ""
    b_number_pages: Optional[int] = None
    b_editor_price: Optional[Decimal] = None
    author:  Optional[Author] = None
    editor: Optional[Editor] = None
    b_main_characters_list: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        """
        Retourne une chaine de caractère (titre du livre et de l'auteur).

        Return:
            str: Le titre du livre suivi du nom de l'auteur.
        """
        auteur_nom = (
            f"{self.author.a_first_name} {self.author.a_last_name}"
            if self.author else "Auteur inconnu"
        )
        return f"{self.b_title} par {auteur_nom}"

    def is_complet(self) -> bool:
        """
        Vérifie si le livre contient les informations essentielles.

        Return:
            bool: True si le livre est complet, False sinon.
        """
        return all([
            self.b_summary,
            self.b_number_pages,
            self.b_editor_price,
            self.b_main_characters_list
        ])

    def price_formatted(self) -> str:
        """
        Retourne le prix formaté avec deux décimales.

        Return:
            str: Prix formaté ou indication  non renseigné.
        """
        if self.b_editor_price is not None:
            return f"{self.b_editor_price:.2f}€"
        return "Non renseigné"

