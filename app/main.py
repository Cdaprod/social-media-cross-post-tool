# app/main.py

from . import create_app

app = create_app()

if __name__ == '__main__':
    # Validate required environment variables
    required_vars = [
        'THREADS_APP_ID', 'THREADS_ACCESS_TOKEN', 'THREADS_API_URL',
        'TWITTER_API_KEY', 'TWITTER_ACCESS_TOKEN', 'TWITTER_API_URL',
        'ANTHROPIC_API_KEY'
    ]

    missing_vars = [var for var in required_vars if not app.config.get(var)]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

    app.run(host='0.0.0.0', port=5000)