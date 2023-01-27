"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""

import discord
import random

import lib.avatars as avatars
import lib.visuals as visuals

from extensions.account_manager.avatar_creation.views.confirm import Confirmation
from extensions.account_manager.misc import timeout_message


async def generate_avatar(interaction: discord.Interaction, skin, ensemble, skirt, hairs, accessories) -> None:
    # Créer l'avatar
    clothes = [ensemble]

    # Lister les ensembles qui ont besoin de pantalon/jupe et de chaussures
    need_pants = ['basic', 'floral', 'sailor', 'sailor_bow', 'skull', 'spaghetti', 'sporty', 'stripe']
    # Si l'ensemble a besoin de pantalon/jupe et de chaussures
    if ensemble in need_pants:
        # Si l'utilisateur veut une jupe
        if bool(skirt):
            clothes.append('skirt')
        else:
            clothes.append('pants')
        clothes.append('shoes')

    # "suit" est un cas à part, il a besoin d'un pantalon spécial
    if 'suit' in clothes:
        clothes.append('pants_suit')
        clothes.append('shoes')

    confirmed = False
    if accessories is None:
        accessories = []
    saved_accessories = accessories
    avatar = None
    while not confirmed:
        if avatars.user_has_avatar(interaction.user.id):
            avatars.delete_avatar(interaction.user.id)
        accessories = saved_accessories

        if 'lipstick' in accessories:
            lipstick = random.choice([True, False])
            accessories.remove('lipstick')
        else:
            lipstick = False

        if 'blush' in accessories:
            blush = random.choice([True, False])
            accessories.remove('blush')
        else:
            blush = False

        if accessories is None:
            accessories = []
            if ensemble == "pumpkin":
                accessories.append(random.choice(["hat_pumpkin_blue", "hat_pumpkin_red"]))
            elif ensemble == "witch":
                if random.randint(0, 1) == 0:
                    accessories = ["hat_witch"]
            elif ensemble == "clown":
                accessories.append(random.choice(["mask_clown_blue", "mask_clown_red"]))
            elif ensemble == "spooky":
                if random.randint(0, 1) == 0:
                    accessories = ["spooky"]

        for accessory in accessories:
            if random.randint(0, len(accessories)) != 0:
                accessories.remove(accessory)

        if "earrings" in accessories:
            accessories.remove("earrings")
            accessories.append(
                random.choices(["earring_emerald_silver", "earring_emerald", "earring_red_silver", "earring_red"])[0])

        if "hats" in accessories:
            accessories.remove("hats")
            accessories.append(random.choices(["hat_cowboy", "hat_lucky"])[0])

        avatar = avatars.create_avatar(
            skin,
            clothes,
            hairs,
            accessories,
            lipstick,
            blush
        )

        view = Confirmation()
        await interaction.response.edit_message(
            attachments=[
                visuals.generate_bubble_with_avatar(
                    "pleased",
                    "Voila ton avatar, il te plaît ?\n\n"
                    "S'il ne te plaît pas, clique sur "
                    "\"Régénérer\"\nsinon, tu peux cliquer "
                    "sur \"Confirmer\"",
                    image=avatar
                )
            ],
            view=view
        )
        await view.wait()
        if view.action is None:
            await timeout_message(interaction)
            avatars.delete_avatar(interaction.user.id)
            return
        confirmed = view.action
        interaction = view.interaction

    # Enregistrer l'avatar
    avatars.save_avatar(interaction.user.id, avatar)

    await interaction.response.edit_message(
        attachments=[
            visuals.generate_bubble_with_avatar(
                "happy",
                "Ton avatar a bien été enregistré !\n\n"
                "Tu peux le gérer en tapant '/avatar' !",
                image=avatar
            )
        ],
        view=None
    )

    # Envoyer un message public avec l'avatar
    await interaction.channel.send(
        files=[
            visuals.generate_bubble_with_avatar(
                "happy", f"{interaction.user.name} vient de créer son avatar !\n\n"
                         "Crée le tien avec '/avatar' !",
                image=avatar
            )
        ],
    )
