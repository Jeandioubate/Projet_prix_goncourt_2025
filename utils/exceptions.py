# -*- coding: utf-8 -*-
"""
Exceptions personnalisées pour l'application Goncourt
"""

class GoncourtException(Exception):
    """Exception de base pour l'application Goncourt"""
    pass

class SelectionException(GoncourtException):
    """Exception liée aux sélections"""
    pass

class VoteException(GoncourtException):
    """Exception liée aux votes"""
    pass

class AuthenticationException(GoncourtException):
    """Exception d'authentification"""
    pass

class ValidationException(GoncourtException):
    """Exception de validation des données"""
    pass