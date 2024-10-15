from utils.constants import *

def navigate_to(root, view_name):
    """Gestionnaire de navigation qui charge les vues en fonction de view_name."""
    if view_name == VIEW_MAIN_MENU:
        from views.main_menu import MainMenu
        MainMenu(root)
    elif view_name == VIEW_STATS:
        from views.stats_view import StatsView
        StatsView(root)
    elif view_name == VIEW_ADD_ENTRY:
        from views.add_entry_view import AddEntryView
        AddEntryView(root)
    elif view_name == VIEW_SESSION:
        from views.session_view import SessionView
        SessionView(root)