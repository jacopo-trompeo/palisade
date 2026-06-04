import qtawesome as qta

from palisade.gui.widgets.secondary_button import SecondaryButton


class BrowseButton(SecondaryButton):
    def __init__(self):
        super().__init__("  Browse installed apps")
        self.setIcon(qta.icon("fa6s.folder-open", color="#87878f"))
