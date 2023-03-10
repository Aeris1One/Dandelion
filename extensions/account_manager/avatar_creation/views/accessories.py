"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import discord

import extensions.account_manager.lib.visuals as visuals


class AvatarCreationAccessories(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.accessories = None
        self.interaction = None
        self.timeout_hit = True

    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder='Sélectionne quelques accessoires',
        min_values=0,
        max_values=7,
        options=[
            discord.SelectOption(emoji="🧔", label='Barbe', value='beard', default=False),
            discord.SelectOption(emoji="💎", label="Boucles d'oreilles", value='earrings', default=False),
            discord.SelectOption(emoji="🎩", label="Chapeaux", value='hats', default=False),
            discord.SelectOption(emoji="👓", label='Lunettes de vue', value='glasses', default=False),
            discord.SelectOption(emoji="🕶️", label='Lunettes de soleil', value='glasses_sun', default=False),
            discord.SelectOption(emoji="💄", label='Rouge à lèvre', value='lipstick', default=False),
            discord.SelectOption(emoji="😊", label='Blush', value='blush', default=False)
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.accessories = select.values
        self.interaction = interaction
        self.timeout_hit = False
        self.stop()

    @discord.ui.button(emoji='😉', label='Les accessoires sont choisis au hasard, ajoutes-en plusieurs !', disabled=True,
                       style=discord.ButtonStyle.grey)
    async def nevergonnarun(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass


async def accessories_stage(interaction) -> tuple[str, discord.Interaction]:
    """
    Création d'avatar
    Renvoyer la vue de choix d'accessoires
    """
    view = AvatarCreationAccessories()
    await interaction.response.edit_message(
        attachments=[visuals.generate_bubble("love", "J'adore !\n\nQuels accessoire on ajoute ?")],
        view=view
    )
    await view.wait()
    if view.timeout_hit:
        return 'timeout', interaction
    return view.accessories, view.interaction
