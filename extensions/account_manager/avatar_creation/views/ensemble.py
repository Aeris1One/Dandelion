"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import discord

import extensions.account_manager.lib.visuals as visuals


class AvatarCreationEnsemble(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.ensemble = None
        self.interaction = None
        self.timeout_hit = True

    # L'utilisateur peut choisir l'ensemble de vêtements de son avatar
    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder='Choisissez un ensemble de vêtements',
        options=[
            discord.SelectOption(label='Basique', value='basic', default=False),
            discord.SelectOption(label='Clown', value='clown', default=False),
            discord.SelectOption(label='Robe', value='dress', default=False),
            discord.SelectOption(label='Floral', value='floral', default=False),
            discord.SelectOption(label='Salopette', value='overalls', default=False),
            discord.SelectOption(label='Marinière', value='sailor', default=False),
            discord.SelectOption(label='Marinière Alternative', value='sailor_bow', default=False),
            discord.SelectOption(label='Crane', value='skull', default=False),
            discord.SelectOption(label='Spaghetti', value='spaghetti', default=False),
            discord.SelectOption(label='Spooky', value='spooky', default=False),
            discord.SelectOption(label='Sportif', value='sporty', default=False),
            discord.SelectOption(label='Rayé', value='stripe', default=False),
            discord.SelectOption(label='Costard', value='suit', default=False),
            discord.SelectOption(label='Citrouille', value='pumpkin', default=False),
            discord.SelectOption(label='Sorcière', value='witch', default=False)
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.ensemble = select.values[0]
        self.interaction = interaction
        self.timeout_hit = False
        self.stop()


async def ensemble_stage(interaction) -> tuple[str, discord.Interaction]:
    """
    Création d'avatar
    Renvoyer la vue de choix de l'ensemble de vêtements de l'avatar.
    """
    view = AvatarCreationEnsemble()
    await interaction.response.edit_message(
        attachments=[visuals.generate_bubble("flirting", "Super ! C'est noté !\n\nMaintenant, choisis son style "
                                                         "vestimentaire.")],
        view=view
    )
    await view.wait()
    if view.timeout_hit:
        return 'timeout', interaction
    return view.ensemble, view.interaction
