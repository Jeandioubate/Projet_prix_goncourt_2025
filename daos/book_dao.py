# -*- coding: utf-8 -*-
"""
BookDAO - Data Access Object pour les livres
"""

from typing import Optional, List
from decimal import Decimal
from daos.dao import Dao
from models.book import Book
from models.author import Author
from models.editor import Editor


class BookDAO(Dao[Book]):
    """
    DAO pour la gestion des livres dans la base de données.
    """

    def create(self, obj: Book) -> int:
        """
        Insère un nouveau livre dans la base de données.

        Args:
            obj (Book): Le livre à insérer

        Returns:
            int: L'ID du livre inséré ou 0 en cas d'erreur
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO book (
                        isbn, b_title, b_summary, b_main_characters, 
                        b_publication_date, b_number_pages, b_editor_price, 
                        a_id, e_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                # Convertir la liste des personnages en chaîne séparée par des virgules
                characters_str = ", ".join(obj.b_main_characters_list) if obj.b_main_characters_list else None

                cursor.execute(sql, (
                    obj.isbn,
                    obj.b_title,
                    obj.b_summary,
                    characters_str,
                    obj.b_publication_date,
                    obj.b_number_pages,
                    float(obj.b_editor_price) if obj.b_editor_price else None,
                    obj.author.a_id if obj.author else None,
                    obj.editor.e_id if obj.editor else None
                ))
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Erreur lors de la création du livre: {e}")
            return 0

    def read(self, pk: int) -> Optional[Book]:
        """
        Récupère un livre par son ID.

        Args:
            pk (int): ID du livre

        Returns:
            Optional[Book]: Le livre trouvé ou None
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT b.*, a.a_id, a.a_last_name, a.a_first_name, a.a_bio,
                           e.e_id, e.e_name
                    FROM book b
                    LEFT JOIN author a ON b.a_id = a.a_id
                    LEFT JOIN editor e ON b.e_id = e.e_id
                    WHERE b.b_id = %s
                """
                cursor.execute(sql, (pk,))
                result = cursor.fetchone()

                if result:
                    return self._create_book_from_result(result)
        except Exception as e:
            print(f"Erreur lors de la lecture du livre: {e}")
        return None

    def read_all(self) -> List[Book]:
        """
        Récupère tous les livres.

        Returns:
            List[Book]: Liste de tous les livres
        """
        books = []
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT b.*, a.a_id, a.a_last_name, a.a_first_name, a.a_bio,
                           e.e_id, e.e_name
                    FROM book b
                    LEFT JOIN author a ON b.a_id = a.a_id
                    LEFT JOIN editor e ON b.e_id = e.e_id
                    ORDER BY b.b_title
                """
                cursor.execute(sql)
                results = cursor.fetchall()

                for result in results:
                    book = self._create_book_from_result(result)
                    books.append(book)
        except Exception as e:
            print(f"Erreur lors de la lecture de tous les livres: {e}")
        return books

    def update(self, obj: Book) -> bool:
        """
        Met à jour un livre existant.

        Args:
            obj (Book): Le livre avec les nouvelles valeurs

        Returns:
            bool: True si la mise à jour a réussi
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    UPDATE book SET
                        isbn = %s,
                        b_title = %s,
                        b_summary = %s,
                        b_main_characters = %s,
                        b_publication_date = %s,
                        b_number_pages = %s,
                        b_editor_price = %s,
                        a_id = %s,
                        e_id = %s
                    WHERE b_id = %s
                """
                characters_str = ", ".join(obj.b_main_characters_list) if obj.b_main_characters_list else None

                cursor.execute(sql, (
                    obj.isbn,
                    obj.b_title,
                    obj.b_summary,
                    characters_str,
                    obj.b_publication_date,
                    obj.b_number_pages,
                    float(obj.b_editor_price) if obj.b_editor_price else None,
                    obj.author.a_id if obj.author else None,
                    obj.editor.e_id if obj.editor else None,
                    obj.b_id
                ))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la mise à jour du livre: {e}")
            return False

    def delete(self, pk: int) -> bool:
        """
        Supprime un livre.

        Args:
            pk (int): ID du livre à supprimer

        Returns:
            bool: True si la suppression a réussi
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM book WHERE b_id = %s"
                cursor.execute(sql, (pk,))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la suppression du livre: {e}")
            return False

    def get_books_by_selection(self, selection_id: int) -> List[Book]:
        """
        Récupère tous les livres d'une sélection spécifique.

        Args:
            selection_id (int): ID de la sélection

        Return:
            List[Book]: Liste des livres de la sélection
        """
        books = []
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT b.*, a.a_id, a.a_last_name, a.a_first_name, a.a_bio,
                           e.e_id, e.e_name
                    FROM book b
                    JOIN book_selection bs ON b.b_id = bs.b_id
                    LEFT JOIN author a ON b.a_id = a.a_id
                    LEFT JOIN editor e ON b.e_id = e.e_id
                    WHERE bs.s_id = %s
                    ORDER BY a.a_last_name                """
                cursor.execute(sql, (selection_id,))
                results = cursor.fetchall()

                for result in results:
                    book = self._create_book_from_result(result)
                    books.append(book)
        except Exception as e:
            print(f"Erreur lors de la récupération des livres par sélection: {e}")
        return books

    def get_books_by_author(self, author_id: int) -> List[Book]:
        """
        Récupère tous les livres d'un auteur.

        Args:
            author_id (int): ID de l'auteur

        Returns:
            List[Book]: Liste des livres de l'auteur
        """
        books = []
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT b.*, a.a_id, a.a_last_name, a.a_first_name, a.a_bio,
                           e.e_id, e.e_name
                    FROM book b
                    LEFT JOIN author a ON b.a_id = a.a_id
                    LEFT JOIN editor e ON b.e_id = e.e_id
                    WHERE b.a_id = %s
                    ORDER BY a.a_last_name
                """
                cursor.execute(sql, (author_id,))
                results = cursor.fetchall()

                for result in results:
                    book = self._create_book_from_result(result)
                    books.append(book)
        except Exception as e:
            print(f"Erreur lors de la récupération des livres par auteur: {e}")
        return books

    def _create_book_from_result(self, result: dict) -> Book:
        """
        Crée un objet Book à partir d'un résultat de requête.

        Args:
            result (dict): Résultat de la requête SQL

        Returns:
            Book: Objet Book créé
        """
        # Créer l'auteur si disponible
        author = None
        if result.get('a_id'):
            author = Author(
                a_id=result['a_id'],
                a_last_name=result['a_last_name'],
                a_first_name=result['a_first_name'],
                a_bio=result.get('a_bio')
            )

        # Créer l'éditeur si disponible
        editor = None
        if result.get('e_id'):
            editor = Editor(
                e_id=result['e_id'],
                e_name=result['e_name']
            )

        # Convertir la chaîne de personnages en liste
        characters_list = []
        if result.get('b_main_characters'):
            characters_list = [c.strip() for c in result['b_main_characters'].split(',')]

        return Book(
            b_id=result['b_id'],
            isbn=result['isbn'],
            b_title=result['b_title'],
            b_summary=result.get('b_summary'),
            b_publication_date=result.get('b_publication_date', ''),
            b_number_pages=result.get('b_number_pages'),
            b_editor_price=Decimal(str(result['b_editor_price'])) if result.get('b_editor_price') else None,
            author=author,
            editor=editor,
            b_main_characters_list=characters_list
        )