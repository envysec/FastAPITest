"""
Tests project/app/main.py:ping

project/tests/test_ping.py
"""

def test_ping(test_app):
  # Given
  # test_app

  # When
  expected_response = {
    'environment': 'dev',
    'ping': 'pong!',
    'testing': True
  }

  response = test_app.get('/ping')

  # Then
  assert response.status_code == 200
  assert response.json() == expected_response
