from app import app

# Get запросы не тестировал - их проще и быстрее посмотреть в браузере. :) А вот post, put и delete тестами покрыты
def test_director_method_post():
    test_director_json = {'id': 113,
                      'name': 'Alexey Derevyanko'
                      }
    resp = app.test_client().post('/directors/', json=test_director_json)
    assert resp.status_code == 201

def test_director_method_put():
    test_director_json = {'name': 'Ivan Ivanov',}
    resp = app.test_client().put('/directors/113', json=test_director_json)
    assert resp.status_code == 204

def test_director_method_delete():
    resp = app.test_client().delete('/directors/113')
    assert resp.status_code == 204

# def test_order_method_post():
#     test_order_json =  {'id': 1031,
#                        'name': 'Сделать домашку',
#                        'description': 'Сделать домашку по Фласку-Алхимии в курсе Скайпро',
#                        'start_date': '18/12/2022',
#                        'end_date': '19/12/2022',
#                        'address': 'Не дом и не улица',
#                        'price': 0,
#                        'customer_id': 24, 'executor_id': 0}
#     resp = app.test_client().post('/orders', json=test_order_json)
#     assert resp.status_code == 200
#
# def test_order_method_put():
#     test_order_json =  {'id': 0,
#                         'name': 'Встретить тетю на вокзале',
#                         'description': 'Встретить тетю на вокзале с табличкой. Отвезти ее в магазин, помочь погрузить покупки. Привезти тетю домой, занести покупки и чемодан в квартиру',
#                         'start_date': '02/08/2013',
#                         'end_date': '03/08/2057',
#                         'address': '4759 William Haven Apt. 194\nWest Corey, TX 43780',
#                         'price': 55120, # price increased x10 - aunt is a nightmare, nobody wants to deal with her
#                         'customer_id': 3,
#                         'executor_id': 6}
#     resp = app.test_client().put('/orders', json=test_order_json)
#     assert resp.status_code == 200
#
# def test_order_method_delete():
#     resp = app.test_client().delete('/orders/42')
#     assert resp.status_code == 200
#
# def test_offer_method_post():
#     test_offer_json =  {'id': 1030, 'order_id': 2, 'executor_id': 1}
#     resp = app.test_client().post('/offers', json=test_offer_json)
#     assert resp.status_code == 200
#
# def test_offer_method_put():
#     test_offer_json =  {'id': 0,
#                         'order_id': 36,
#                         'executor_id': 2 # was 10
#                         }
#     resp = app.test_client().put('/offers', json=test_offer_json)
#     assert resp.status_code == 200
#
# def test_offer_method_delete():
#     resp = app.test_client().delete('/offers/1')
#     assert resp.status_code == 200