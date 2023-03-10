"""
Copyright © ascpial 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
from __future__ import annotations

import importlib
import os

__all__ = [
    'EXTENSION_FOLDER',
    'available_namespaces',
    'get_register_order',
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
        if namespace.startswith(('.', '_')):  # extension invalide ou désactivée
            continue

        path = os.path.join(EXTENSION_FOLDER, namespace)

        if not os.path.isdir(path):
            continue

        namespaces.append(namespace)

    return namespaces


def get_register_order(extensions: list[Extension]) -> list[Extension]:
    """Retourne la liste des extensions en respectant les dépendances.
    
    Une extension sera chargé après ses dépendances.
    Ne retourne pas d'erreur si les dépendances d'une extension ne sont pas
    satisfaites.

    L'ordre des extensions est conservé au sein d'un groupe de dépendances
    identiques ou lorsque des extensions ont des dépendances circulaires.
    """
    sorted_extensions: list[Extension] = []

    for extension in extensions:
        to_satisfy = extension.depends_on.copy()  # liste des namespaces manquants

        target_index = 0
        while len(to_satisfy) > 0 and target_index < len(sorted_extensions):
            if sorted_extensions[target_index].namespace in to_satisfy:
                to_satisfy.remove(sorted_extensions[target_index].namespace)

            target_index += 1

        sorted_extensions.insert(target_index + 1, extension)

    return sorted_extensions


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
        self.api_loaded = False

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

    def load_api(self):
        """Charge l'API de l'extension dans la mémoire.
        
        Retourne `True` si le fichier d'API existe, `False` sinon.
        """

        api_path = self.get_module_path(api=True)

        if not os.path.exists(api_path):
            return False

        self.api = importlib.import_module(self.get_module_import(api=True))
        self.api_loaded = True
        return True

    @extension_loaded_check
    def register(self, client):  # TODO: annotation de type
        """Enregistre l'extension auprès du client passé en argument.
        
        Il faut que l'extension ai été chargée.
        """

        self.module.main(client)

    def get_module_path(self, api: bool = False) -> os.PathLike:
        """Retourne le chemin du fichier d'entrée de l'extension.
        
        Si `api`  est paramétré sur `True`, retourne le chemin du module d'API.
        """
        if not api:
            target = "main.py"
        else:
            target = "api.py"

        return os.path.join(EXTENSION_FOLDER, self.namespace, target)

    def get_module_import(self, api: bool = False) -> str:
        """Retourne la référence de module de l'extension.

        Si `api`  est paramétré sur `True`, retourne le chemin du module d'API.
        
        Exemple : `extensions.account_manager.main`
        """
        if not api:
            target = "main"
        else:
            target = "api"

        return '.'.join([EXTENSION_FOLDER, self.namespace, target])

    @property
    @extension_loaded_check
    def depends_on(self) -> list[str]:
        """Retourne la liste des namespaces des extensions sur laquelle dépend
        cette extension.
        
        Peut être utilisé pour définir l'ordre de chargement des extensions.
        Retourne une liste vide par défaut, indiquant que l'extension se suffit
        à elle même.
        """

        if hasattr(self.module, 'depends_on'):
            return self.module.depends_on
        else:
            return []

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

    @property
    @extension_loaded_check
    def db_objects(self) -> list[os.PathLike]:
        """Retourne les objets de database utilisés par le plugin.
        
        Par défaut, retourne une liste vide.

        Il faut que l'extension ai été chargée.
        """

        if hasattr(self.module, 'db_objects'):
            return self.module.db_objects
        else:
            return []
