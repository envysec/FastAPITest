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
  assert response.json().get('url') == 'https://foo.bar'


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

  response = test_app.post(
    '/summaries/',
    data=json.dumps({'url': 'invalid://url'})
  )
  assert response.status_code == 422
  message = response.json().get('detail')[0].get('msg')
  assert message == 'URL scheme not permitted'


def test_read_summary(test_app_with_db):
  response = test_app_with_db.post(
    '/summaries/',
    data=json.dumps({'url': 'https://foo.bar'})
  )
  summary_id = response.json().get('id')

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
  assert response.json().get('detail') == 'Summary not found'

  response = test_app_with_db.get('/summaries/0/')
  expected_data = {
    'detail': [
      {
        'loc': ['path', 'id'],
        'msg': 'ensure this value is greater than 0',
        'type': 'value_error.number.not_gt',
        'ctx': {'limit_value': 0}
      }
    ]
  }
  assert response.status_code == 422
  assert response.json() == expected_data


def test_read_all_summaries(test_app_with_db):
  response = test_app_with_db.post(
    '/summaries/',
    data=json.dumps({'url': 'https://foo.bar'})
  )
  summary_id = response.json().get('id')

  response = test_app_with_db.get('/summaries/')
  assert response.status_code == 200

  response_list = response.json()
  assert len(list(filter(
    lambda d: d.get('id') == summary_id, response_list
  ))) > 0


def test_remove_summary(test_app_with_db):
  response = test_app_with_db.post(
    '/summaries/',
    data=json.dumps({'url': 'https://foo.bar'})
  )
  summary_id = response.json().get('id')

  response = test_app_with_db.delete(f'/summaries/{summary_id}/')
  assert response.status_code == 200
  assert response.json() == {'id': summary_id, 'url': 'https://foo.bar'}


def test_remove_summary_incorrect_id(test_app_with_db):
  response = test_app_with_db.delete('/summaries/999/')
  assert response.status_code == 404
  assert response.json().get('detail') == 'Summary not found'

  expected_data = {
    'detail': [
      {
        'loc': ['path', 'id'],
        'msg': 'ensure this value is greater than 0',
        'type': 'value_error.number.not_gt',
        'ctx': {'limit_value': 0}
      }
    ]
  }
  response = test_app_with_db.delete('/summaries/0/')
  assert response.status_code == 422
  assert response.json() == expected_data


def test_update_summary(test_app_with_db):
  response = test_app_with_db.post(
    '/summaries/', data=json.dumps({'url': 'https://foo.bar'})
  )
  summary_id = response.json().get('id')

  response = test_app_with_db.put(
    f'summaries/{summary_id}/',
    data=json.dumps({'url': 'https://foo.bar', 'summary': 'updated!'})
  )
  assert response.status_code == 200

  response_dict = response.json()
  assert response_dict.get('id') == summary_id
  assert response_dict.get('url') == 'https://foo.bar'
  assert response_dict.get('summary') == 'updated!'
  assert response_dict.get('created_at')


def test_update_summary_incorrect_id(test_app_with_db):
  response = test_app_with_db.put(
    '/summaries/999/',
    data=json.dumps({'url': 'https://foo.bar', 'summary': 'updated!'})
  )
  assert response.status_code == 404
  assert response.json().get('detail') == 'Summary not found'

  response = test_app_with_db.put(
    '/summaries/0/',
    data=json.dumps({'url': 'https://foo.bar', 'summary': 'updated!'})
  )
  expected_data = {
    'detail': [
      {
        'loc': ['path', 'id'],
        'msg': 'ensure this value is greater than 0',
        'type': 'value_error.number.not_gt',
        'ctx': {'limit_value': 0}
      }
    ]
  }

  assert response.status_code == 422
  assert response.json() == expected_data


def test_update_summary_invalid_json(test_app_with_db):
  response = test_app_with_db.post(
    '/summaries/', data=json.dumps({'url': 'https://foo.bar'})
  )
  summary_id = response.json().get('id')
  expected_data = {
    'detail': [
      {
        'loc': ['body', 'url'],
        'msg': 'field required',
        'type': 'value_error.missing'
      },
      {
        'loc': ['body', 'summary'],
        'msg': 'field required',
        'type': 'value_error.missing'
      }
    ]
  }

  response = test_app_with_db.put(
    f'/summaries/{summary_id}/',
    data=json.dumps({})
  )

  assert response.status_code == 422
  assert response.json() == expected_data


def test_update_summary_invalid_keys(test_app_with_db):
  response = test_app_with_db.post(
    '/summaries/', data=json.dumps({'url': 'https://foo.bar'})
  )
  summary_id = response.json().get('id')
  expected_data = {
    'detail': [
      {
        'loc': ['body', 'summary'],
        'msg': 'field required',
        'type': 'value_error.missing'
      }
    ]
  }

  response = test_app_with_db.put(
    f'/summaries/{summary_id}/',
    data=json.dumps({'url': 'https://foo.bar'})
  )
  assert response.status_code == 422
  assert response.json() == expected_data

  response = test_app_with_db.put(
    f'/summaries/{summary_id}/',
    data=json.dumps({'url': 'invalud://url', 'summary': 'updated!'})
  )
  assert response.status_code == 422
  message = response.json().get('detail')[0].get('msg')
  assert message == 'URL scheme not permitted'
