"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import logging

import prometheus_client

logger = logging.getLogger("libs.monitoring")

# Définir les métriques
#
# Nombre de commandes exécutées depuis le démarrage du bot
commands_ran = prometheus_client.Counter(
    "dandelion_commands_ran",
    "Nombre de commandes exécutées",
    ["command"]
)

# Nombre d'erreurs depuis le démarrage du bot
errors = prometheus_client.Counter(
    "dandelion_exceptions",
    "Nombre d'erreurs",
    ["exception", "method"]
)

# Temps d'exécution des fonctions
function_execution_time = prometheus_client.Summary(
    "dandelion_function_execution_time",
    "Temps d'exécution des fonctions",
    ["function"]
)

# Nombre de messages reçus depuis le démarrage du bot
messages_received = prometheus_client.Counter(
    "dandelion_messages_received",
    "Nombre de messages vus",
    ["guild"]
)


def init_prometheus():
    """
    Initialise le serveur Prometheus
    """
    prometheus_client.start_http_server(8000)
    logger.info("Prometheus démarré sur le port 8000")
