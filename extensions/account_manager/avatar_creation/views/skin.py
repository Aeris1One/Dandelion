"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import discord
import extensions.account_manager.lib.visuals as visuals


class AvatarCreationSkin(discord.ui.View):
    # L'utilisateur peut choisir la couleur de peau de son avatar
    def __init__(self):
        super().__init__(timeout=60)
        self.interaction = None
        self.skin_color = None
        self.timeout_hit = True

    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder='Choisissez une couleur de peau',
        options=[
            discord.SelectOption(emoji="<:char1:1063121749962674396>", label='1', value='1', default=False),
            discord.SelectOption(emoji="<:char2:1063121751933988895>", label='2', value='2', default=False),
            discord.SelectOption(emoji="<:char3:1063121753301323776>", label='3', value='3', default=False),
            discord.SelectOption(emoji="<:char4:1063121754572202015>", label='4', value='4', default=False),
            discord.SelectOption(emoji="<:char5:1063121756811972618>", label='5', value='5', default=False),
            discord.SelectOption(emoji="<:char6:1063121758112190494>", label='6', value='6', default=False),
            discord.SelectOption(emoji="<:char7:1063121759609573446>", label='7', value='7', default=False),
            discord.SelectOption(emoji="<:char8:1063121762243592192>", label='8', value='8', default=False)
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.skin_color = select.values[0]
        self.interaction = interaction
        self.timeout_hit = False
        self.stop()


async def skin_stage(interaction) -> tuple[str, discord.Interaction]:
    """
    Création d'avatar
    Renvoyer la vue de choix de couleur de peau.
    """
    view = AvatarCreationSkin()
    await interaction.response.edit_message(
        attachments=[visuals.generate_bubble("happy", "Bienvenue dans l'assistant d'avatar !\n\nChoisis la couleur de "
                                                      "peau de ton avatar")],
        view=view
    )
    await view.wait()
    if view.timeout_hit:
        return 'timeout', interaction
    return view.skin_color, view.interaction
