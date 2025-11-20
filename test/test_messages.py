from messaging.db.message import Message


def test_create_message(client, session):
    payload = {'payload': {'a': 1}}

    res = client.post('/messages', json=payload)
    assert res.status_code == 201

    data = res.get_json()
    assert 'id' in data
    assert data['status'] == 'pending'

    msg = session.get(Message, data['id'])
    assert msg is not None
    assert msg.payload == {'a': 1}


def test_list_messages(client, session):
    m1 = Message(payload={'x': 1}, status='pending')
    m2 = Message(payload={'y': 2}, status='completed')
    session.add_all([m1, m2])
    session.commit()

    res = client.get('/messages')
    assert res.status_code == 200
    data = res.get_json()

    ids = [d['id'] for d in data]
    assert m1.id in ids
    assert m2.id in ids


def test_get_message(client, session):
    msg = Message(payload={'a': 3}, status='pending')
    session.add(msg)
    session.commit()

    res = client.get(f'/messages/{msg.id}')
    assert res.status_code == 200

    data = res.get_json()
    assert data['id'] == msg.id
    assert data['payload'] == {'a': 3}
    assert data['status'] == 'pending'


def test_stats(client, session):
    session.add_all([
        Message(payload={}, status='pending'),
        Message(payload={}, status='completed'),
        Message(payload={}, status='failed'),
    ])
    session.commit()

    res = client.get('/messages/stats')
    assert res.status_code == 200
    stats = res.get_json()
    assert stats['total'] >= 3
    assert stats['pending'] > 0
    assert stats['completed'] > 0
    assert stats['failed'] > 0
