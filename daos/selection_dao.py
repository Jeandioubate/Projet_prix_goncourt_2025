# -*- coding: utf-8 -*-
"""
SelectionDAO - Data Access Object pour les sélections
"""

from typing import Optional, List
from datetime import date
from daos.dao import Dao
from models.selection import Selection
from models.book import Book
from daos.book_dao import BookDAO


class SelectionDAO(Dao[Selection]):
    """
    DAO pour la gestion des sélections dans la base de données.
    """

    def __init__(self):
        self.book_dao = BookDAO()

    def create(self, obj: Selection) -> int:
        """
        Crée une nouvelle sélection.

        Args:
            obj (Selection): La sélection à créer

        Returns:
            int: L'ID de la sélection créée ou 0 en cas d'erreur
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO selection (s_name, s_round, s_date)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (
                    obj.s_name,
                    obj.s_round,
                    obj.s_date
                ))
                self.connection.commit()
                selection_id = cursor.lastrowid

                # Ajouter les livres à la sélection
                for book in obj.book:
                    self.add_book_to_selection(book.b_id, selection_id)

                return selection_id
        except Exception as e:
            print(f"Erreur lors de la création de la sélection: {e}")
            return 0

    def read(self, pk: int) -> Optional[Selection]:
        """
        Récupère une sélection par son ID.

        Args:
            pk (int): ID de la sélection

        Returns:
            Optional[Selection]: La sélection trouvée ou None
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM selection WHERE s_id = %s"
                cursor.execute(sql, (pk,))
                result = cursor.fetchone()

                if result:
                    selection = self._create_selection_from_result(result)
                    # Charger les livres de la sélection
                    selection.book = self.book_dao.get_books_by_selection(pk)
                    return selection
        except Exception as e:
            print(f"Erreur lors de la lecture de la sélection: {e}")
        return None

    def read_all(self) -> List[Selection]:
        """
        Récupère toutes les sélections.

        Returns:
            List[Selection]: Liste de toutes les sélections
        """
        selections = []
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM selection ORDER BY s_round"
                cursor.execute(sql)
                results = cursor.fetchall()

                for result in results:
                    selection = self._create_selection_from_result(result)
                    # Charger les livres de la sélection
                    selection.book = self.book_dao.get_books_by_selection(selection.s_id)
                    selections.append(selection)
        except Exception as e:
            print(f"Erreur lors de la lecture de toutes les sélections: {e}")
        return selections

    def update(self, obj: Selection) -> bool:
        """
        Met à jour une sélection.

        Args:
            obj (Selection): La sélection avec les nouvelles valeurs

        Returns:
            bool: True si la mise à jour a réussi
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    UPDATE selection SET
                        s_name = %s,
                        s_round = %s,
                        s_date = %s
                    WHERE s_id = %s
                """
                cursor.execute(sql, (
                    obj.s_name,
                    obj.s_round,
                    obj.s_date,
                    obj.s_id
                ))
                self.connection.commit()

                # Mettre à jour les livres de la sélection
                # D'abord, supprimer tous les livres actuels
                self._clear_selection_books(obj.s_id)

                # Puis ajouter les nouveaux livres
                for book in obj.book:
                    self.add_book_to_selection(book.b_id, obj.s_id)

                return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la sélection: {e}")
            return False

    def delete(self, pk: int) -> bool:
        """
        Supprime une sélection.

        Args:
            pk (int): ID de la sélection à supprimer

        Returns:
            bool: True si la suppression a réussi
        """
        try:
            # D'abord supprimer les associations livres-sélection
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM book_selection WHERE s_id = %s"
                cursor.execute(sql, (pk,))

                # Puis supprimer la sélection
                sql = "DELETE FROM selection WHERE s_id = %s"
                cursor.execute(sql, (pk,))

                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la suppression de la sélection: {e}")
            return False

    def find_by_round(self, round_number: int) -> Optional[Selection]:
        """
        Trouve une sélection par son numéro de tour.

        Args:
            round_number (int): Numéro du tour (1, 2, 3, 4)

        Returns:
            Optional[Selection]: La sélection trouvée ou None
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM selection WHERE s_round = %s"
                cursor.execute(sql, (round_number,))
                result = cursor.fetchone()

                if result:
                    selection = self._create_selection_from_result(result)
                    selection.book = self.book_dao.get_books_by_selection(selection.s_id)
                    return selection
        except Exception as e:
            print(f"Erreur lors de la recherche par tour: {e}")
        return None

    def add_book_to_selection(self, book_id: int, selection_id: int) -> bool:
        """
        Ajoute un livre à une sélection.

        Args:
            book_id (int): ID du livre
            selection_id (int): ID de la sélection

        Returns:
            bool: True si l'ajout a réussi
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT IGNORE INTO book_selection (b_id, s_id)
                    VALUES (%s, %s)
                """
                cursor.execute(sql, (book_id, selection_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de l'ajout du livre à la sélection: {e}")
            return False

    def remove_book_from_selection(self, book_id: int, selection_id: int) -> bool:
        """
        Retire un livre d'une sélection.

        Args:
            book_id (int): ID du livre
            selection_id (int): ID de la sélection

        Returns:
            bool: True si le retrait a réussi
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM book_selection WHERE b_id = %s AND s_id = %s"
                cursor.execute(sql, (book_id, selection_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors du retrait du livre de la sélection: {e}")
            return False

    def _clear_selection_books(self, selection_id: int) -> None:
        """
        Supprime tous les livres d'une sélection.

        Args:
            selection_id (int): ID de la sélection
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM book_selection WHERE s_id = %s"
                cursor.execute(sql, (selection_id,))
                self.connection.commit()
        except Exception as e:
            print(f"Erreur lors du nettoyage des livres de la sélection: {e}")

    def _create_selection_from_result(self, result: dict) -> Selection:
        """
        Crée un objet Selection à partir d'un résultat de requête.

        Args:
            result (dict): Résultat de la requête SQL

        Returns:
            Selection: Objet Selection créé
        """
        return Selection(
            s_id=result['s_id'],
            s_name=result['s_name'],
            s_round=result['s_round'],
            s_date=result.get('s_date')
        )