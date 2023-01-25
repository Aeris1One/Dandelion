"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import discord
import lib.visuals as visuals


class AvatarCreationSkirt(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.skirt = None
        self.interaction = None
        self.timeout_hit = True

    # L'utilisateur peut choisir s'il veut une jupe ou non
    @discord.ui.button(label='Oui', style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.skirt = True
        self.interaction = interaction
        self.timeout_hit = False
        self.stop()

    @discord.ui.button(label='Non', style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.skirt = False
        self.interaction = interaction
        self.timeout_hit = False
        self.stop()


async def skirt_stage(interaction) -> tuple[str, discord.Interaction]:
    """
    Création d'avatar
    Renvoyer la vue de la jupe
    """
    view = AvatarCreationSkirt()
    await interaction.response.edit_message(
        attachments=[visuals.generate_bubble("amused", "Génial !\n\nTon avatar porte-t-il une jupe ?")],
        view=view
    )
    await view.wait()
    if view.timeout_hit:
        return 'timeout', interaction
    return view.skirt, view.interaction
