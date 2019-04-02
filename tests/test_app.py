import pytest
from app.app import Products


def setup_test_env():
    p = Products()
    p.add_product('Croissant', 'CF', [(3, 5.95), (5, 9.95), (9, 16.99)])
    return p


def test_wrong_code():
    products = setup_test_env()
    
    with pytest.raises(TypeError):
        products.process_order('99 CODE')


def test_correct_calculation():
    products = setup_test_env()
    res = products._calculate_packages(13, [(3, 5.95), (5, 9.95), (9, 16.99)])
    assert res == [(5, 9.95), (5, 9.95), (3, 5.95)]


def test_no_packaging_possible():
    products = setup_test_env()
    
    with pytest.raises(TypeError):
        res = products._calculate_packages(7, [(3, 5.95), (5, 9.95), (9, 16.99)])
