from bs4 import BeautifulSoup
from .common_headers import BASE_HEADERS
from ....cutom_logger import logger

import requests


UP4U_URLS = {
    # This is the url to the login page
    'LOGIN_PAGE_URL': 'https://up4u.up.edu.mx/user/auth/login',

    # Origin
    'ORIGIN': 'https://up4u.up.edu.mx',

    # This the url after the user has logged in
    'DASHBOARD_URL': 'https://up4u.up.edu.mx/p/inicio?id=1',

    # This is the url to the grades page
    'GRADES_URL': 'https://up4u.up.edu.mx/Calificaciones/index',

    # This is the url to the schedule page
    'SCHEDULE_URL': 'https://up4u.up.edu.mx/Horarios/index',
}

# Login headers
UP4U_HEADERS = BASE_HEADERS.copy()
UP4U_HEADERS.update({
    'Origin': UP4U_URLS['ORIGIN'],
    'Referer': UP4U_URLS['LOGIN_PAGE_URL'],
})


def authenticate_up4u(username: str, password: str) -> bool:
    """
    Authenticate to UP4U and return session cookies if successful.

    :param username: The username, ex: 0250009 of the user.
    :param password: The password of the user.
    :return: True if the user was authenticated successfully, False otherwise.
    """
    # Create the session
    try:
        with requests.Session() as session:
            pass
    except Exception as e:
        logger.error(f'Error creating session: {e}')
