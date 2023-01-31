"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import discord
import extensions.account_manager.lib.visuals as visuals


class AvatarCreationHairs(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.hairs = None
        self.interaction = None
        self.timeout_hit = True

    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder='Choisissez une coupe de cheveux',
        options=[
            discord.SelectOption(label='Aucun', value='none', default=False),
            discord.SelectOption(label='Au carré', value='bob', default=False),
            discord.SelectOption(label='Tressés', value='braids', default=False),
            discord.SelectOption(label='Frisés', value='curly', default=False),
            discord.SelectOption(label='Emo', value='emo', default=False),
            discord.SelectOption(label='Très longs', value='extra_long', default=False),
            discord.SelectOption(label='Boucle française', value='french_curl', default=False),
            discord.SelectOption(label='Gentleman', value='gentleman', default=False),
            discord.SelectOption(label='Longs et lisses', value='long_straight', default=False),
            discord.SelectOption(label='Mi-longs', value='midiwave', default=False),
            discord.SelectOption(label='Queue de cheval', value='ponytail', default=False),
            discord.SelectOption(label='Chignon', value='spacebuns', default=False),
            discord.SelectOption(label='Ondulés', value='wavy', default=False),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.hairs = select.values[0]
        self.interaction = interaction
        self.timeout_hit = False
        self.stop()


async def hairs_stage(interaction) -> tuple[any, discord.Interaction]:
    """
    Création d'avatar
    Renvoyer la vue de choix d'accessoires
    """
    view = AvatarCreationHairs()
    await interaction.response.edit_message(
        attachments=[visuals.generate_bubble("cool", "Très joli choix !\n\nEt pour finir, quelle coupe de cheveux ?")],
        view=view
    )
    await view.wait()
    if view.timeout_hit:
        return 'timeout', interaction
    if view.hairs == 'none':
        return None, interaction
    return view.hairs, view.interaction
