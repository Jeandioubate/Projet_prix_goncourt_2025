# -*- coding: utf-8 -*-

"""
Class abstraite générique Dao[T], dont hérite les classes de DAO de chaque entité
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import ClassVar, Optional, List
import pymysql.cursors

@dataclass
class Dao[T](ABC):
    connection: ClassVar[pymysql.Connection] = \
        pymysql.connect(host='localhost',
                        user='John',
                        password='TestPythonEval',
                        database='john_goncourt',
                        cursorclass=pymysql.cursors.DictCursor)

    @abstractmethod
    def create(self, obj: T) -> int:
        """
        Insère une entité dans la base de données.

        Args:
            obj (T): l'objet à insérer.

        Return:
            int: l'ID auto-incrémenté ou 0 en cas d'erreur.
        """
        ...

    @abstractmethod
    def read(self, pk: int) -> Optional[T]:
        """
        Récupère une entrée via sa clé primaire.

        Args:
            pk (int): valeur de la clé primaire.

        Return:
            Optional[T]: l'objet trouvé ou None.
        """
        ...

    @abstractmethod
    def read_all(self) -> List[T]:
        """
        Récupère toutes les lignes de la table.

        Return:
            List[T]: liste des objets instanciés.
        """
        ...

    @abstractmethod
    def update(self, obj: T) -> bool:
        """
        Met à jour un enregistrement existant.

        Args:
            obj (T): objet contenant les nouvelles valeurs.

        Return:
            bool: True si une ligne a été mise à jour.
        """
        ...

    @abstractmethod
    def delete(self, pk: int) -> bool:
        """
        Supprime un enregistrement via sa clé primaire.

        Args:
            pk (int): ID à supprimer.

        Return:
            bool: True si une ligne a été supprimée.
        """
