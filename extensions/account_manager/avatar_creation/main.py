"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import discord

from extensions.account_manager.avatar_creation.views.accessories import accessories_stage
from extensions.account_manager.avatar_creation.views.ensemble import ensemble_stage
from extensions.account_manager.avatar_creation.views.hairs import hairs_stage
from extensions.account_manager.avatar_creation.views.skin import skin_stage
from extensions.account_manager.avatar_creation.views.skirt import skirt_stage
from extensions.account_manager.avatar_creation.avatar_generation import generate_avatar
from extensions.account_manager.misc import timeout_message


async def init_avatar_creation(interaction: discord.Interaction):
    """
    Débuter le processus de création d'avatar

    :param interaction: Interaction
    """
    # Demander la couleur de la peau
    skin, interaction = await skin_stage(interaction)
    if skin == "timeout":
        await timeout_message(interaction)
        return

    # Demander le style vestimentaire
    ensemble, interaction = await ensemble_stage(interaction)
    if ensemble == "timeout":
        await timeout_message(interaction)
        return

    # Demander si le personnage porte une jupe
    if ensemble in ['basic', 'floral', 'sailor', 'sailor_bow', 'skull', 'spaghetti', 'sporty', 'stripe']:
        skirt, interaction = await skirt_stage(interaction)
        if skirt == "timeout":
            await timeout_message(interaction)
            return
    else:
        skirt = None

    # Demander les accessoires
    if ensemble not in ["pumpkin", "witch", "clown", "spooky"]:
        accessories, interaction = await accessories_stage(interaction)
        if accessories == "timeout":
            await timeout_message(interaction)
            return
    else:
        accessories = None

    # Demander les cheveux
    if ensemble not in ["clown"]:
        hairs, interaction = await hairs_stage(interaction)
        if hairs == "timeout":
            await timeout_message(interaction)
            return
    else:
        hairs = None

    # Créer l'avatar
    await generate_avatar(interaction, skin, ensemble, skirt, hairs, accessories)

