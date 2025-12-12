# -*- coding: utf-8 -*-

"""
Class Author
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Author:
    """
    Modèle représentant un auteur littéraire.

    Attributs:
        a_id (int): Identifiant unique de l'auteur.
        a_last_name (str): Nom de famille de l'auteur.
        a_first_name (str): Prénom de l'auteur.
        a_bio (Optional[str]): Biographie de l'auteur, si disponible.
    """

    a_id: int
    a_last_name: str
    a_first_name: str
    a_bio: Optional[str] = None

    def __str__(self) -> str:
        """
        Retourne une chaine de caractère (le nom de l'auteur).

        Return:
            str: Nom complet sous la forme "Prénom Nom".
        """
        return f"{self.a_first_name} {self.a_last_name}"

    def full_name(self) -> str:
        """
        Retourne le nom complet de l'auteur.

        Returns:
            str: Nom complet sous la forme "Prénom Nom".
        """
        return f"{self.a_first_name} {self.a_last_name}"

    def has_biography(self) -> bool:
        """
        Vérifie si l'auteur possède une biographie.

        Returns:
            bool: True si une biographie est disponible, sinon False.
        """
        return bool(self.a_bio)


