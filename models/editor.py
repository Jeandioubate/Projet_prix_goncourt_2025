# -*- coding: utf-8 -*-

"""
Class Editor
"""

from dataclasses import dataclass

@dataclass
class Editor:
    """
    Modèle représentant un éditeur littéraire.

    Attributs:
        e_id (int): Identifiant unique de l'éditeur.
        e_name (str): Nom de l'éditeur.
    """

    e_id: int
    e_name: str

    def __str__(self) -> str:
        """
        Retourne une représentation textuelle de l'éditeur.

        Return:
            str: Le nom de l'éditeur.
        """
        return self.e_name
