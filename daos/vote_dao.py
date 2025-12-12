# -*- coding: utf-8 -*-
"""
VoteDAO - Data Access Object pour les votes
"""

from typing import Optional, List
from datetime import date
from daos.dao import Dao
from models.vote import Vote
from models.book import Book
from models.selection import Selection
from daos.book_dao import BookDAO
from daos.selection_dao import SelectionDAO


class VoteDAO(Dao[Vote]):
    """
    DAO pour la gestion des votes dans la base de données.
    """

    def __init__(self):
        self.book_dao = BookDAO()
        self.selection_dao = SelectionDAO()

    def create(self, obj: Vote) -> int:
        """
        Crée un nouveau vote.

        Args:
            obj (Vote): Le vote à créer

        Returns:
            int: L'ID du vote créé ou 0 en cas d'erreur
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO vote (v_number_vote, v_date_vote, b_id, s_id)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    obj.v_number_vote,
                    obj.v_date_vote,
                    obj.book.b_id,
                    obj.selection.s_id
                ))
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Erreur lors de la création du vote: {e}")
            return 0

    def read(self, pk: int) -> Optional[Vote]:
        """
        Récupère un vote par son ID.

        Args:
            pk (int): ID du vote

        Returns:
            Optional[Vote]: Le vote trouvé ou None
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT v.*, b.*, s.*
                    FROM vote v
                    JOIN book b ON v.b_id = b.b_id
                    JOIN selection s ON v.s_id = s.s_id
                    WHERE v.v_id = %s
                """
                cursor.execute(sql, (pk,))
                result = cursor.fetchone()

                if result:
                    return self._create_vote_from_result(result)
        except Exception as e:
            print(f"Erreur lors de la lecture du vote: {e}")
        return None

    def read_all(self) -> List[Vote]:
        """
        Récupère tous les votes.

        Returns:
            List[Vote]: Liste de tous les votes
        """
        votes = []
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT v.*, b.*, s.*
                    FROM vote v
                    JOIN book b ON v.b_id = b.b_id
                    JOIN selection s ON v.s_id = s.s_id
                    ORDER BY v.v_date_vote DESC, v.v_number_vote DESC
                """
                cursor.execute(sql)
                results = cursor.fetchall()

                for result in results:
                    vote = self._create_vote_from_result(result)
                    votes.append(vote)
        except Exception as e:
            print(f"Erreur lors de la lecture de tous les votes: {e}")
        return votes

    def update(self, obj: Vote) -> bool:
        """
        Met à jour un vote existant.

        Args:
            obj (Vote): Le vote avec les nouvelles valeurs

        Returns:
            bool: True si la mise à jour a réussi
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    UPDATE vote SET
                        v_number_vote = %s,
                        v_date_vote = %s,
                        b_id = %s,
                        s_id = %s
                    WHERE v_id = %s
                """
                cursor.execute(sql, (
                    obj.v_number_vote,
                    obj.v_date_vote,
                    obj.book.b_id,
                    obj.selection.s_id,
                    obj.v_id
                ))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la mise à jour du vote: {e}")
            return False

    def delete(self, pk: int) -> bool:
        """
        Supprime un vote.

        Args:
            pk (int): ID du vote à supprimer

        Returns:
            bool: True si la suppression a réussi
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM vote WHERE v_id = %s"
                cursor.execute(sql, (pk,))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la suppression du vote: {e}")
            return False

    def get_votes_by_selection(self, selection_id: int) -> List[Vote]:
        """
        Récupère tous les votes d'une sélection.

        Args:
            selection_id (int): ID de la sélection

        Returns:
            List[Vote]: Liste des votes pour cette sélection
        """
        votes = []
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT v.*, b.*, s.*
                    FROM vote v
                    JOIN book b ON v.b_id = b.b_id
                    JOIN selection s ON v.s_id = s.s_id
                    WHERE v.s_id = %s
                    ORDER BY v.v_number_vote DESC
                """
                cursor.execute(sql, (selection_id,))
                results = cursor.fetchall()

                for result in results:
                    vote = self._create_vote_from_result(result)
                    votes.append(vote)
        except Exception as e:
            print(f"Erreur lors de la récupération des votes par sélection: {e}")
        return votes

    def get_final_results(self) -> List[Vote]:
        """
        Récupère les résultats du dernier tour (4ème sélection).

        Returns:
            List[Vote]: Liste des votes triés par nombre de voix
        """
        votes = []
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT v.*, b.*, s.*
                    FROM vote v
                    JOIN book b ON v.b_id = b.b_id
                    JOIN selection s ON v.s_id = s.s_id
                    WHERE s.s_round = 4
                    ORDER BY v.v_number_vote DESC
                """
                cursor.execute(sql)
                results = cursor.fetchall()

                for result in results:
                    vote = self._create_vote_from_result(result)
                    votes.append(vote)
        except Exception as e:
            print(f"Erreur lors de la récupération des résultats finaux: {e}")
        return votes

    def record_final_votes(self, votes_data: dict, selection_id: int, vote_date: date) -> bool:
        """
        Enregistre les votes du dernier tour.

        Args:
            votes_data (dict): Dictionnaire {book_id: nombre_de_voix}
            selection_id (int): ID de la sélection (doit être le tour 4)
            vote_date (date): Date du vote

        Returns:
            bool: True si l'enregistrement a réussi
        """
        try:
            with self.connection.cursor() as cursor:
                # Supprimer les votes existants pour cette sélection
                sql = "DELETE FROM vote WHERE s_id = %s"
                cursor.execute(sql, (selection_id,))

                # Insérer les nouveaux votes
                sql = """
                    INSERT INTO vote (v_number_vote, v_date_vote, b_id, s_id)
                    VALUES (%s, %s, %s, %s)
                """
                for book_id, vote_count in votes_data.items():
                    cursor.execute(sql, (vote_count, vote_date, book_id, selection_id))

                self.connection.commit()
                return True
        except Exception as e:
            print(f"Erreur lors de l'enregistrement des votes finaux: {e}")
            return False

    def _create_vote_from_result(self, result: dict) -> Vote:
        """
        Crée un objet Vote à partir d'un résultat de requête.

        Args:
            result (dict): Résultat de la requête SQL

        Returns:
            Vote: Objet Vote créé
        """
        # Créer le livre
        book = self.book_dao.read(result['b_id'])

        # Créer la sélection
        selection = Selection(
            s_id=result['s_id'],
            s_name=result['s_name'],
            s_round=result['s_round'],
            s_date=result.get('s_date')
        )

        return Vote(
            v_id=result['v_id'],
            v_number_vote=result['v_number_vote'],
            v_date_vote=result['v_date_vote'],
            book=book,
            selection=selection
        )