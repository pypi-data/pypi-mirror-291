from typing import Any, Dict, List, Optional

from PS3838.PS3838Bet import Bet
from PS3838.PS3838Retrieve import Retrieve
from PS3838.telegram.telegram_bot import CustomLogger
from PS3838.utils import leagues_correspondency
from PS3838.utils.tools_check import check_credentials, check_list_matches
from PS3838.utils.tools_code import get_team_odds, place_bets, retrieve_matches

#############################
#        Retrieving         #
#############################

def retrieving(
    credentials: Dict[str, str],
    list_matches: List[Dict[str, Any]],
    api_retrieve: Optional[Retrieve] = None,
    logger_active: bool = True,
    logger: Optional[CustomLogger] = None,
    *args, 
    **kwargs
) -> List[List[Dict[str, Any]]]:
    """
    This function retrieves the odds for a given list of matches. Thanks to the credentials, it creates a Retrieve API which is used to connect to PS3838. Then several functions are used to find each match and their corresponding odds.
    
    Parameters:
        credentials (Dict[str, str]): The credentials to connect to the PS3838 API. 
            Example: {"username": "my_username", "password": "my_password"}
        list_matches (List[Dict[str, Any]]): A list of matches to retrieve the odds for.
            Example: [{"league" : 2036, "team1" : "Montpellier", "team2" : "Paris Saint-Germain", "date" : datetime(2024, 8, 17, 17, 0, 0), "result" : 2, "amount" : 5, "odd_min" : 1.05}, ...]
        api_retrieve (Optional[Retrieve]): An optional Retrieve object to use to retrieve the matches. If not provided, it will be created.
        logger_active (bool): A boolean to activate the logger. Default is True.
        logger (Optional[CustomLogger]): An optional CustomLogger object to use to log the information. If not provided, it will be created.
        
    Returns:
        List[List[Dict[str, Any]]]: A list of matches with their corresponding odds.
            Example: [({'id': 1595460299, 'starts': '2024-08-23T18:45:00Z', 'home': 'Paris Saint-Germain', 'away': 'Montpellier HSC', 'rotNum': '3121', 'liveStatus': 2, 'status': 'O', 'parlayRestriction': 2, 'altTeaser': False, 'resultingUnit': 'Regular', 'betAcceptanceType': 0, 'version': 545200449, 'league': 2036, 'result': 1, 'amount': 5, 'odd_min': 1.05, 'line_id': 2650184231}, {'team1_odds': 1.309, 'draw_odds': 6.14, 'team2_odds': 8.47}), ...]
    """
    
    # Create the logger if it doesn't exist. 
    if logger_active and not logger:
        custom_logger = CustomLogger(name="PS3838", log_file="PS3838.log", func="retrieving", credentials=credentials)
        logger = custom_logger.get_logger()
    
    # If the API object is not provided, it means that we didn't call the function betting before, so we need to check and create everything. Otherwise the check has been done.
    if not api_retrieve:
        check_credentials(credentials)
        check_list_matches(list_matches)
        api_retrieve = Retrieve(credentials=credentials)

    # Retrieve the matches
    matches = retrieve_matches(list_matches, api_retrieve, logger)

    # Retrieve the odds for each match
    match_odds = []
    for match in matches:
        try:
            team1_odds, match["line_id"] = get_team_odds(api_retrieve, match, "Team1")
            team2_odds, _ = get_team_odds(api_retrieve, match, "Team2")
            draw_odds, _ = get_team_odds(api_retrieve, match, "Draw")
            
            # Append the match and odds to the list "match_odds"
            match_odds.append((match, 
                {
                    "team1_odds": team1_odds,
                    "draw_odds": draw_odds,
                    "team2_odds": team2_odds,
                }
            ))
            
        except Exception as e:
            if logger:
                logger.error(f"Error retrieving odds for match {match['event_id']}: {e}")
    
    if logger:
        logger.info(f"Retrieved odds for {len(match_odds)} matches" if len(match_odds) > 0 else "No matches found")
    return match_odds


#############################
#         Betting           #
#############################

def betting(
    credentials : Dict[str, str],
    list_matches : List[Dict[str, Any]],
    logger_active: bool = True,
    *args, 
    **kwargs
) -> List[List[Dict[str, Any]]] | None:
    """
    This function places bets on the PS3838 API for a given list of matches. It retrieves the odds for each match and then places the bets under some conditions (bet not already placed, odds above a certain threshold, etc.).
    
    Parameters:
        credentials (Dict[str, str]): The credentials to connect to the PS3838 API.
            Example: {"username": "my_username", "password": "my_password"}
        list_matches (List[Dict[str, Any]]): A list of matches to place the bets for.
            Example: [{"league" : 2036, "team1" : "Montpellier", "team2" : "Paris Saint-Germain", "date" : datetime(2024, 8, 17, 17, 0, 0), "result" : 2, "amount" : 5, "odd_min" : 1.05}, ...]
        logger_active (bool): A boolean to activate the logger. Default is True.

    Returns:
        List[List[Dict[str, Any]]] | None: A list of matches with their corresponding odds if the bets were placed, None otherwise.
            Example: [({'id': 1595460299, 'starts': '2024-08-23T18:45:00Z', 'home': 'Paris Saint-Germain', 'away': 'Montpellier HSC', 'rotNum': '3121', 'liveStatus': 2, 'status': 'O', 'parlayRestriction': 2, 'altTeaser': False, 'resultingUnit': 'Regular', 'betAcceptanceType': 0, 'version': 545200449, 'league': 2036, 'result': 1, 'amount': 5, 'odd_min': 1.05, 'line_id': 2650184231}, {'team1_odds': 1.309, 'draw_odds': 6.14, 'team2_odds': 8.47}), ...]
    """
    
    # Create the logger if it doesn't exist.
    if logger_active:
        custom_logger = CustomLogger(name="PS3838", log_file="PS3838.log", func="betting", credentials=credentials)
        logger = custom_logger.get_logger()
    else:
        logger = None

    # Check if the parameters are provided and valid (Raise a CredentialError if not), and check if the list of matches is valid (Raise a ParameterError if not)
    check_credentials(credentials)
    check_list_matches(list_matches, to_bet=True)

    # Create the API objects
    bet = Bet(credentials=credentials)
    retrieve = Retrieve(credentials=credentials)

    # Check if there is maintenance
    maintenance = bet.check_maintenance()

    if maintenance["status"] == 'ALL_BETTING_ENABLED':
        try:
            # Retrieve the odds with the matches
            match_odds = retrieving(credentials, list_matches, retrieve, logger_active=logger_active, logger=logger)

            # Place the bets
            place_bets(match_odds, bet, logger=logger)

        except Exception as e:
            if logger:
                logger.error(f"Error placing bets: {e}")
    else:
        if logger:
            logger.info("Maintenance in progress, no bets placed. Try another time")

    return match_odds if match_odds else None

def get_dict_leagues_correspondency() -> Dict[int, str]:
    """
    This function returns the correspondency between the league names and IDs for sport API and for PS3838.
    Example: {("Ligue1" : 52) : ("Ligue 1" : 2036)}
    """
    return leagues_correspondency.CORRESPONDENCY_DICT_LEAGUES