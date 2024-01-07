
@require_http_methods(["POST"])
@csrf_protect
def up4u_login(request) -> Response:
    """
    Login the user with the provided credentials and return the user's data if successful.
    """
  
    try:
    # Extract credentials from POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required.'}, status=400)
        
        # Authenticate user
        success, cookies = authenticate_up4u(username, password)

        if success:
            # You might want to do something with the cookies here, like storing them for future requests
            return JsonResponse({'success': True, 'message': 'User authenticated successfully.'})

        return JsonResponse({'success': False, 'message': 'Invalid username or password.'}, status=401)
    except Exception as e:
        logger.error(f"Login failed: {e}")
        return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)


