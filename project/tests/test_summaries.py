"""
Tests related to summaries endpoints.

project/tests/test_summaries.py
"""

import json


def test_create_summary(test_app_with_db):
  # Should this be mocked?
  response = test_app_with_db.post(
    '/summaries/',
    data=json.dumps({'url':'https://foo.bar'})
  )

  assert response.status_code == 201
  assert response.json()['url'] == 'https://foo.bar'


def test_create_summaries_invalid_json(test_app):
  response = test_app.post('/summaries/', data=json.dumps({}))
  expected_data = {
    'detail': [
      {
        'loc': ['body', 'url'],
        'msg': 'field required',
        'type': 'value_error.missing'
      }
    ]
  }

  assert response.status_code == 422
  assert response.json() == expected_data


def test_read_summary(test_app_with_db):
  response = test_app_with_db.post(
    '/summaries/',
    data=json.dumps({'url': 'https://foo.bar'})
  )
  summary_id = response.json()['id']

  response = test_app_with_db.get(f'/summaries/{summary_id}/')
  assert response.status_code == 200

  response_dict = response.json()
  assert response_dict.get('id') == summary_id
  assert response_dict.get('url') == 'https://foo.bar'
  assert response_dict.get('summary')
  assert response_dict.get('created_at')


def test_read_summary_incorrect_id(test_app_with_db):
  response = test_app_with_db.get('/summaries/999/')
  assert response.status_code == 404
  assert response.json()['detail'] == 'Summary not found'


def test_read_all_summaries(test_app_with_db):
  response = test_app_with_db.post(
    '/summaries/',
    data=json.dumps({'url': 'https://foo.bar'})
  )
  summary_id = response.json()['id']

  response = test_app_with_db.get('/summaries/')
  assert response.status_code == 200

  response_list = response.json()
  assert len(list(filter(
    lambda d: d.get('id') == summary_id, response_list
  ))) > 0
