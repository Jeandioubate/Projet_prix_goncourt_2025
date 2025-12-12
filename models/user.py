# -*- coding: utf-8 -*-

"""
Classe abstraite User, mère de President et Visiteur
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Tuple

@dataclass
class User(ABC):
    """
    Classe abstraite représentant un utilisateur.

    Attributs:
        user_type (str): Type de l'utilisateur, permet d'identifier ses permissions.
    """

    user_type: str

    @abstractmethod
    def get_menu_options(self) -> Dict[str, Tuple[str, str]]:
        """
        Retourne les options du menu pour l'utilisateur correspondant.

        Return:
            Dict[str, Tuple[str, str]]:
                Un dictionnaire avec comme clé le numéro de l'option,
                et comme valeur un tuple (description, nom_de_méthode).
        """
        ...


@dataclass
class Visitor(User):
    """
    Représente un utilisateur de type visiteur.
    Dispose uniquement des droits de consultation.
    """

    def __init__(self) -> None:
        super().__init__("visitor")

    def get_menu_options(self) -> Dict[str, Tuple[str, str]]:
        """
        Retourne les options du menu pour un visiteur.

        Return:
            Dict[str, Tuple[str, str]]: Liste des actions consultables.
        """
        return {
            "1": ("Afficher la première sélection", "afficher_premiere_selection"),
            "2": ("Afficher la deuxième sélection", "afficher_deuxieme_selection"),
            "3": ("Afficher la troisième sélection", "afficher_troisieme_selection"),
            "4": ("Afficher toutes les sélections", "afficher_toutes_selections"),
            "5": ("Afficher les résultats du dernier tour", "afficher_resultats_finale"),
            "6": ("Changer de mode (Président)", "changer_mode"),
        }


@dataclass
class President(User):
    """
    Représente un président du jury.
    Dispose de droits de modification sur les sélections et les votes.
    """

    def __init__(self) -> None:
        super().__init__("president")

    def get_menu_options(self) -> Dict[str, Tuple[str, str]]:
        """
        Retourne les options du menu pour un président du jury.

        Return:
            Dict[str, Tuple[str, str]]: Liste des actions disponibles pour gérer les sélections et votes.
        """
        return {
            "1": ("Établir la deuxième sélection (8 livres)", "creer_deuxieme_selection"),
            "2": ("Établir la troisième sélection (4 livres)", "creer_troisieme_selection"),
            "3": ("Enregistrer les votes du dernier tour", "enregistrer_votes_finale"),
            "4": ("Changer de mode (Visiteur)", "changer_mode"),
        }
