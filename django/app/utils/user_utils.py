import requests
from bs4 import BeautifulSoup
import logging


logging.basicConfig(level=logging.INFO)


BASE_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55',
    'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'macOS',
}


# UP4U URLs and headers
UP4U_URLS = {
    'LOGIN_PAGE_URL': 'https://up4u.up.edu.mx/user/auth/login',
    'ORIGIN': 'https://up4u.up.edu.mx',
    'DASHBOARD_URL': 'https://up4u.up.edu.mx/p/inicio?id=1',
    'GRADES_URL': 'https://up4u.up.edu.mx/Calificaciones/index',
    'SCHEDULE_URL': 'https://up4u.up.edu.mx/Horarios/index',
}

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
                logging.error("CSRF token not found in login page.")
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
                logging.info("User authenticated successfully.")
                return True, session.cookies

            logging.error("Failed to log in with provided credentials.")
            return False, None

    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return False, None
