"""
Copyright © ascpial 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""

import importlib
import os

__all__ = [
    'EXTENSION_FOLDER',
    'available_namespaces',
    'Extension',
]

EXTENSION_FOLDER = 'extensions'

def extension_loaded_check(func):
    """Vérifie que l'extension est chargée et lève une erreur sinon."""

    def wrapper(self, *args, **kwargs):
        if not self.loaded:
            raise ValueError("L'extension n'a pas été chargée")
        
        return func(self, *args, **kwargs)
    
    return wrapper

def available_namespaces() -> list[str]:
    """Retourne la liste des extensions disponibles dans le dossier par défaut.
    """
    namespaces = []

    for namespace in os.listdir(EXTENSION_FOLDER):
        if namespace.startswith(('.', '_')): # extension invalide ou désactivée
            continue
        
        path = os.path.join(EXTENSION_FOLDER, namespace)

        if not os.path.isdir(path):
            continue

        namespaces.append(namespace)
    
    return namespaces

class Extension:
    """Classe utilisée pour gérer les extensions.
    
    Cette classe permet de détecter automatiquement les fichiers à charger et
    permet de faire des opérations comme des tests sur les extensions.
    """

    def __init__(self, namespace: str):
        """Créer une extension avec le namespace indiqué."""
        self.namespace = namespace

        self.module = None
        self.loaded = False
    
    def load(self):
        """Charge l'extension dans la mémoire.

        Cette fonction n'enregistre pas les fonctionnalités au niveau de la
        base de données ou du bot.
        
        Si le fichier d'entrée n'existe pas, lève une erreur
        `FileNotFoundError`.
        """

        module_path = self.get_module_path()

        if not os.path.exists(module_path):
            raise FileNotFoundError(
                f"Il n'existe aucun fichier à l'emplacement {module_path}"
            )

        self.module = importlib.import_module(self.get_module_import())
        self.loaded = True
    
    @extension_loaded_check
    def register(self, client): # TODO: annotation de type
        """Enregistre l'extension auprès du client passé en argument.
        
        Il faut que l'extension ai été chargée.
        """
        
        self.module.main(client)

    def get_module_path(self) -> os.PathLike:
        """Retourne le chemin du fichier d'entrée de l'extension."""
        return os.path.join(EXTENSION_FOLDER, self.namespace, 'main.py')
    
    def get_module_import(self) -> str:
        """Retourne la référence de module de l'extension.
        
        Exemple : `extensions.account_manager.main`
        """
        return '.'.join([EXTENSION_FOLDER, self.namespace, 'main'])
    

    @property
    @extension_loaded_check
    def data_structure(self) -> list[os.PathLike]:
        """Retourne la structure de fichiers pour le stockage utilisée par
        l'extension.
        
        Par défaut, retourne une liste vide.

        Il faut que l'extension ai été chargée.
        """

        if hasattr(self.module, 'data_structure'):
            return self.module.data_structure
        else:
            return []
    
    @property
    @extension_loaded_check
    def downloadable_data(self) -> list[os.PathLike]:
        """Retourne les fichiers à télécharger demandés par l'extension.
        
        Par défaut, retourne une liste vide.

        Il faut que l'extension ai été chargée.
        """

        if hasattr(self.module, 'downloadable_data'):
            return self.module.downloadable_data
        else:
            return []

