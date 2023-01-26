"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import prometheus_client

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


def init_prometheus():
    prometheus_client.start_http_server(8000)