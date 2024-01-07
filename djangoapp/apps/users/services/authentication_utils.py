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


def authenticate_up4u(username: str, password: str):
    """
    Authenticate to UP4U using provided credentials and return session cookies if successful.

    :param username: The username of the user.
    :param password: The password of the user.
    :return: Tuple of (bool indicating success, session cookies if successful, None otherwise)
    """
    try:
        with requests.Session() as session:
            # Fetch the login page to get the CSRF token
            response = session.get(
                UP4U_URLS['LOGIN_PAGE_URL'], headers=UP4U_HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_token = soup.find(
                'input', attrs={'name': '_csrf'}).get('value')

            if not csrf_token:
                logger.error("CSRF token not found in login page.")
                return False, None

            # Prepare login data with the CSRF token and provided credentials
            login_data = {
                '_csrf': csrf_token,
                'Login[username]': username,
                'Login[password]': password,
                'Login[rememberMe]': '0'
            }

            # Submit login request
            login_response = session.post(
                UP4U_URLS['LOGIN_PAGE_URL'], headers=UP4U_HEADERS, data=login_data)
            login_response.raise_for_status()

            # Check if login was successful by looking for known failure text
            if "Usuario o contraseña incorrectos." not in login_response.text:
                logger.info("User authenticated successfully.")
                return True, session.cookies

            logger.error("Failed to log in with provided credentials.")
            return False, None

    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return False, None
