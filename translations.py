"""
Translation system for Code with AI competition platform.
Supports English (en) and Swedish (sv) languages.
"""

TRANSLATIONS = {
    'en': {
        'nav': {
            'leaderboard': 'Leaderboard',
            'competition_info': 'Competition Info',
            'level': 'Level',
            'logout': 'Log out',
            'logout_with_user': 'Log out ({})',
        },
        'base': {
            'title': 'Code with AI',
            'subtitle': 'Coding competition',
            'subtitle_with_levels': 'Coding competition with {} progressively harder levels',
            'footer': '© 2024 Code with AI Competition Platform',
        },
        'login': {
            'title': 'Sign up for the competition',
            'username': 'Username',
            'username_placeholder': 'Enter your username',
            'username_hint': 'Only letters and numbers allowed',
            'start_competition': 'Start competition',
            'how_it_works': 'How it works:',
            'step1': 'Enter your username above',
            'step2': 'Solve the 5 levels in order',
            'step3': 'Each level has a problem to solve',
            'step4': 'Enter your answer in the box',
            'step5': 'See your ranking on the leaderboard',
            'error_invalid_username': 'Username must be alphanumeric and not empty',
        },
        'admin': {
            'title': 'Competition Control',
            'competition_active': 'Competition active',
            'competition_inactive': 'Competition inactive',
            'started_at': 'Started: {}',
            'not_started': 'The competition has not started',
            'active_competition': 'Active competition:',
            'select_active_competition': 'Select Active Competition',
            'start_competition': 'Start competition',
            'stop_competition': 'Stop competition',
            'clear_all_data': 'Clear all data',
            'statistics': 'Statistics',
            'users': 'Users',
            'submissions': 'Submissions',
            'completed_levels': 'Completed levels',
            'view_leaderboard': 'View leaderboard',
            'alert_started': 'Competition started!',
            'alert_stopped': 'Competition stopped!',
            'alert_changed': 'Competition changed!',
            'confirm_stop': 'Are you sure you want to stop the competition?',
            'confirm_change': 'Are you sure you want to switch to this competition?',
            'confirm_reset': 'Are you sure you want to delete ALL data? This cannot be undone!',
            'alert_reset': 'All data deleted!',
            'error_start': 'Error starting: {}',
            'error_stop': 'Error stopping: {}',
            'error_change': 'Error changing competition: {}',
            'error_reset': 'Error resetting: {}',
            'error_fetch': 'Error: {}',
        },
        'leaderboard': {
            'title': 'Leaderboard',
            'rank': '#',
            'user': 'User',
            'level': 'Level',
            'total_time': 'Total time',
            'details': 'Details',
            'level_detail': 'Level {}: {}',
            'no_results': 'No results yet',
            'start_solving': 'Start solving the levels to see your ranking here!',
            'read_intro': 'Read competition introduction',
            'auto_update': 'Updates automatically every 5 seconds',
            'last_updated': 'Last updated: {}',
            'error_fetch': 'Could not fetch leaderboard. Check that the server is running.',
            'error_console': 'Error fetching leaderboard:',
        },
        'level': {
            'correct_answer': 'Correct answer! Level {} complete!',
            'next_level': 'You will proceed to level {} in 2 seconds...',
            'next_leaderboard': 'You will proceed to the leaderboard in 2 seconds...',
            'problem_description': 'Problem description:',
            'input_file': 'Input file:',
            'download_input': 'Download the input file to process it with your program:',
            'download': 'Download {}',
            'your_answer': 'Your answer:',
            'submit_answer': 'Submit answer',
            'view_leaderboard': 'View leaderboard',
            'show_solution': 'Show solution program',
            'hide_solution': 'Hide solution program',
            'solution_program': 'Solution program:',
            'show_hint': 'Show hint',
            'hide_hint': 'Hide hint',
            'hint': 'Hint:',
            'error_load_solution': 'Could not load solution',
        },
        'competition_intro': {
            'overview': 'Overview',
            'story': 'Story',
            'level_progression': 'Level progression',
            'learning_objectives': 'Learning objectives',
            'difficulty_curve': 'Difficulty level',
            'context': 'Context',
            'estimated_time': 'Estimated time',
            'no_info': 'No competition information available.',
            'start_competition': 'Start competition',
        },
        'errors': {
            'competition_not_found': 'Competition not found',
            'level_not_found': 'Level not found',
            'no_input_file': 'No input file for this level',
            'invalid_filename': 'Invalid filename',
            'file_not_found': 'File not found',
            'invalid_path': 'Invalid file path',
            'competition_not_active': 'The competition is not active. Wait until the competition starts.',
            'answer_required': 'Answer required',
            'wrong_answer': 'Wrong answer! Try again.',
            'invalid_api_key': 'API key required',
            'invalid_api_key_error': 'Invalid API key',
            'no_active_competition': 'No active competition',
            'competition_started': 'Competition started!',
            'competition_stopped': 'Competition stopped!',
            'competition_set': 'Competition {} is now active',
            'invalid_competition': 'Invalid competition',
            'missing_competition_id': 'Missing competition_id',
            'invalid_level': 'Invalid level',
            'invalid_time': 'Invalid time',
            'competition_inactive': 'The competition is not active',
            'level_not_in_competition': 'The level is not in the competition',
            'all_data_deleted': 'All results deleted',
            'error_reading_solution': 'Error reading solution file: {}',
        },
        'messages': {
            'time_improved': 'Time improved!',
            'no_improvement': 'No improvement',
        },
    },
    'sv': {
        'nav': {
            'leaderboard': 'Leaderboard',
            'competition_info': 'Tävlingsinfo',
            'level': 'Nivå',
            'logout': 'Logga ut',
            'logout_with_user': 'Logga ut ({})',
        },
        'base': {
            'title': 'Code with AI',
            'subtitle': 'Kodningstävling',
            'subtitle_with_levels': 'Kodningstävling med {} progressivt svårare nivåer',
            'footer': '© 2024 Code with AI Competition Platform',
        },
        'login': {
            'title': 'Anmäl dig till tävlingen',
            'username': 'Användarnamn',
            'username_placeholder': 'Ange ditt användarnamn',
            'username_hint': 'Endast bokstäver och siffror tillåtna',
            'start_competition': 'Starta tävling',
            'how_it_works': 'Så här fungerar det:',
            'step1': 'Ange ditt användarnamn ovan',
            'step2': 'Lös de 5 nivåerna i ordning',
            'step3': 'Varje nivå har ett problem att lösa',
            'step4': 'Ange ditt svar i rutan',
            'step5': 'Se din ranking på leaderboard',
            'error_invalid_username': 'Användarnamn måste vara alfanumeriskt och inte tomt',
        },
        'admin': {
            'title': 'Tävlingskontroll',
            'competition_active': 'Tävling aktiv',
            'competition_inactive': 'Tävling inaktiv',
            'started_at': 'Startad: {}',
            'not_started': 'Tävlingen är inte startad',
            'active_competition': 'Aktiv tävling:',
            'select_active_competition': 'Välj Aktiv Tävling',
            'start_competition': '🚀 Starta tävling',
            'stop_competition': '⏹️ Stoppa tävling',
            'clear_all_data': '🗑️ Rensa all data',
            'statistics': 'Statistik',
            'users': 'Användare',
            'submissions': 'Inlämningar',
            'completed_levels': 'Genomförda nivåer',
            'view_leaderboard': '📊 Visa leaderboard',
            'alert_started': 'Tävling startad!',
            'alert_stopped': 'Tävling stoppad!',
            'alert_changed': 'Tävling ändrad!',
            'confirm_stop': 'Är du säker på att du vill stoppa tävlingen?',
            'confirm_change': 'Är du säker på att du vill byta till denna tävling?',
            'confirm_reset': 'Är du säker på att du vill radera ALL data? Detta går inte att ångra!',
            'alert_reset': 'All data raderad!',
            'error_start': 'Fel vid start: {}',
            'error_stop': 'Fel vid stopp: {}',
            'error_change': 'Fel vid byte av tävling: {}',
            'error_reset': 'Fel vid reset: {}',
            'error_fetch': 'Fel: {}',
        },
        'leaderboard': {
            'title': 'Leaderboard',
            'rank': '#',
            'user': 'Användare',
            'level': 'Nivå',
            'total_time': 'Total tid',
            'details': 'Detaljer',
            'level_detail': 'Nivå {}: {}',
            'no_results': 'Inga resultat ännu',
            'start_solving': 'Börja lösa nivåerna för att se din ranking här!',
            'read_intro': '📖 Läs tävlingsintroduktion',
            'auto_update': 'Uppdateras automatiskt var 5:e sekund',
            'last_updated': 'Senast uppdaterad: {}',
            'error_fetch': 'Kunde inte hämta leaderboard. Kontrollera att servern körs.',
            'error_console': 'Fel vid hämtning av leaderboard:',
        },
        'level': {
            'correct_answer': 'Rätt svar! Nivå {} klar!',
            'next_level': 'Du går vidare till nivå {} om 2 sekunder...',
            'next_leaderboard': 'Du går vidare till leaderboard om 2 sekunder...',
            'problem_description': 'Problembeskrivning:',
            'input_file': 'Input-fil:',
            'download_input': 'Ladda ner input-filen för att bearbeta den med ditt program:',
            'download': '📥 Ladda ner {}',
            'your_answer': 'Ditt svar:',
            'submit_answer': 'Skicka svar',
            'view_leaderboard': 'Visa leaderboard',
            'show_solution': '💡 Visa lösningsprogram',
            'hide_solution': '🙈 Dölj lösningsprogram',
            'solution_program': 'Lösningsprogram:',
            'show_hint': '💡 Visa tips',
            'hide_hint': '🙈 Dölj tips',
            'hint': 'Tips:',
            'error_load_solution': 'Kunde inte ladda lösningen',
        },
        'competition_intro': {
            'overview': '📋 Översikt',
            'story': '📖 Berättelse',
            'level_progression': '🎯 Nivåprogression',
            'learning_objectives': '🎓 Lärandemål',
            'difficulty_curve': '⭐ Svårighetsgrad',
            'context': '🌍 Kontext',
            'estimated_time': '⏱️ Beräknad tid',
            'no_info': 'Ingen tävlingsinformation tillgänglig.',
            'start_competition': '🚀 Starta tävlingen',
        },
        'errors': {
            'competition_not_found': 'Tävling finns inte',
            'level_not_found': 'Nivå finns inte',
            'no_input_file': 'Ingen input-fil för denna nivå',
            'invalid_filename': 'Ogiltigt filnamn',
            'file_not_found': 'Fil hittades inte',
            'invalid_path': 'Ogiltig fil-sökväg',
            'competition_not_active': 'Tävlingen är inte aktiv. Vänta tills tävlingen startar.',
            'answer_required': 'Svar krävs',
            'wrong_answer': 'Felaktigt svar! Försök igen.',
            'invalid_api_key': 'API-nyckel krävs',
            'invalid_api_key_error': 'Ogiltig API-nyckel',
            'no_active_competition': 'Ingen aktiv tävling',
            'competition_started': 'Tävling startad!',
            'competition_stopped': 'Tävling stoppad!',
            'competition_set': 'Tävling {} är nu aktiv',
            'invalid_competition': 'Ogiltig tävling',
            'missing_competition_id': 'Saknar competition_id',
            'invalid_level': 'Ogiltig nivå',
            'invalid_time': 'Ogiltig tid',
            'competition_inactive': 'Tävlingen är inte aktiv',
            'level_not_in_competition': 'Nivån finns inte i tävlingen',
            'all_data_deleted': 'Alla resultat raderade',
            'error_reading_solution': 'Fel vid läsning av lösningsfil: {}',
        },
        'messages': {
            'time_improved': 'Tid förbättrad!',
            'no_improvement': 'Ingen förbättring',
        },
    },
}


def get_translations(lang='sv'):
    """
    Get translations for a specific language.
    
    Args:
        lang: Language code ('en' or 'sv')
        
    Returns:
        Dictionary of translations for the specified language
    """
    return TRANSLATIONS.get(lang, TRANSLATIONS['sv'])


def t(lang, category, key, *args):
    """
    Get a translated string.
    
    Args:
        lang: Language code ('en' or 'sv')
        category: Translation category (e.g., 'nav', 'admin', 'errors')
        key: Translation key
        *args: Optional format arguments
        
    Returns:
        Translated string, formatted if args provided
    """
    translations = get_translations(lang)
    category_dict = translations.get(category, {})
    text = category_dict.get(key, key)
    
    if args:
        try:
            return text.format(*args)
        except (KeyError, ValueError, IndexError):
            return text
    
    return text

