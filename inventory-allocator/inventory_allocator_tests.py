import unittest
from inventory_allocator import InventoryAllocator

class InventoryAllocatorTests(unittest.TestCase):
    # Happy Case, exact inventory match!*
    def test_happy_case(self):
        order = { 'apple': 1}
        inventory = [{'name': 'owd', 
                       'inventory': 
                           {'apple': 1}}]
        result = [{'owd': {'apple': 1}}]
        self.assertEqual(InventoryAllocator().cheapest_shipment(order, 
            inventory), result) 

    # Not enough inventory -> no allocations!
    def test_no_allocations(self):
        order = {'apple': 1}
        inventory = [{'name': 'owd', 
                       'inventory': {'apple': 0}}]
        result = []
        self.assertEqual(InventoryAllocator().cheapest_shipment(order, 
            inventory), result)
    
    # Not enough inventory -> no allocations!
    def test_no_allocations_two(self):
        order = {'apple': 2}
        inventory = [{'name': 'owd', 
                       'inventory': {'apple': 1}}]
        result = []
        self.assertEqual(InventoryAllocator().cheapest_shipment(order, 
            inventory), result)
    
    # Should split an item across warehouses if that is the only way to ship
    # an item:
    def test_perfect_split(self):
        order = {'apple': 10}
        inventory = [{'name': 'owd', 
                       'inventory': 
                           {'apple': 5}},
            {'name': 'dm',
            'inventory': 
                {'apple': 5}}]
        result = [{'dm': 
                       {'apple': 5}}, 
            {'owd': {'apple': 5}}]
        self.assertEqual(InventoryAllocator().cheapest_shipment(order, 
            inventory), result)
    
    # Should split an item across warehouses and use less from the warehouse
    # with higher cost
    def test_valid_split(self):
        order = {'apple': 9}
        inventory = [{'name': 'owd', 
                       'inventory': 
                           {'apple': 5}},
            {'name': 'dm',
            'inventory': 
                {'apple': 5}}]
        result = [{'dm': 
                       {'apple': 4}}, 
            {'owd': {'apple': 5}}]
        self.assertEqual(InventoryAllocator().cheapest_shipment(order, 
            inventory), result)
                         
    # Should not be able to fulfill shipment, even with split
    def test_invalid_split(self):
        order = {'apple': 11}
        inventory = [{'name': 'owd', 
                       'inventory': 
                           {'apple': 5 }},
            {'name': 'dm',
            'inventory': 
                {'apple': 5}}]
        result = []
        self.assertEqual(InventoryAllocator().cheapest_shipment(order,
            inventory), result)
        
    # No order -> no allocation!
    def test_no_order(self):
        order = {'apple': 10}
        inventory = []
        result = [{'dm': 
                       {'apple': 4}}, 
            {'owd': {'apple': 5}}]
        result = []
        self.assertEqual(InventoryAllocator().cheapest_shipment(order,
            inventory), result)
        
    # No inventory -> no allocation!
    def test_no_inventory(self):
        order = {'apple': 1}
        inventory = []
        result = []
        self.assertEqual(InventoryAllocator().cheapest_shipment(order,
            inventory), result)
    
    # No order and inventory -> no allocation!
    def test_no_order_inventory(self):
        order = {}
        inventory = []
        result = []
        self.assertEqual(InventoryAllocator().cheapest_shipment(order,
            inventory), result)
    
    # Negative direct supply will not allocate
    def test_negative_direct_supply(self):
        order = {'apple': 10}
        inventory = [{'name': 'owd', 
                       'inventory': 
                           {'apple': 5}},
            {'name': 'dm',
            'inventory': 
                {'apple': -1}}]
        result = []
        self.assertEqual(InventoryAllocator().cheapest_shipment(order,
            inventory), result)
                         
    # Negative indirect supply will allocate
    def test_negative_indirect_supply(self):
        order = {'apple': 10}
        inventory = [{'name': 'owd', 
                       'inventory': 
                           {'apple': 5, 'banana': -1}},
            {'name': 'dm',
            'inventory': 
                {'apple': 5}}]
        result = [{'dm': 
                       {'apple': 5}}, 
            {'owd': {'apple': 5}}]
        self.assertEqual(InventoryAllocator().cheapest_shipment(order,
            inventory), result)
    
    # Zero direct supply will not allocate
    def test_zero_direct_supply(self):
        order = {'apple': 0}
        inventory = [{'name': 'owd', 
                       'inventory': 
                           {'apple': 5}},
            {'name': 'dm',
            'inventory': 
                {'apple': 5}}]
        result = []
        self.assertEqual(InventoryAllocator().cheapest_shipment(order,
            inventory), result)
        
    # Zero indirect supply will allocate when valid
    def test_zero_indirect_supply(self):
        order = {'apple': 10, 'banana': 0}
        inventory = [{'name': 'owd', 
                       'inventory': 
                           {'apple': 5, 'banana': -1}},
            {'name': 'dm',
            'inventory': 
                {'apple': 5}}]
        result = [{'dm': 
                       {'apple': 5}}, 
            {'owd': {'apple': 5}}]
        self.assertEqual(InventoryAllocator().cheapest_shipment(order,
            inventory), result)

    # Happy case two, inventory match after!
    def test_happy_case_two(self):
        order = {'banana': 1}
        inventory = [{'name': 'owd', 
                       'inventory': 
                           {'apple': 5}},
            {'name': 'dm',
            'inventory': 
                {'apple': 5, 'banana': 2}}]
        result = [{'dm': {'banana': 1}}]
        self.assertEqual(InventoryAllocator().cheapest_shipment(order,
            inventory), result)

    # Multiple orders from different warehouses
    def test_multiple_orders(self):
        order = {'apple': 10}
        inventory = [{'name': 'owd', 
                      'inventory': {'apple': 5}}, 
            {'name': 'dm', 'inventory': {'apple': 5}}]
        result = [{'dm': {'apple': 5}}, 
                  {'owd': {'apple': 5}}]
        self.assertEqual(InventoryAllocator().cheapest_shipment(order,
            inventory), result)
    
    # Multiple orders split from different warehouses
    def test_multiple_orders_split(self):
        order = {'apple': 5, 'banana': 5, 'cherry': 5}
        inventory = [{'name': 'owd', 
                       'inventory': 
                           {'apple': 2, 'cherry': 3}},
            {'name': 'dm',
            'inventory': 
                {'apple': 5, 'banana': 2}},
            {'name': 'jz',
            'inventory': 
                {'banana': 4, 'cherry': 3}}]
        result = [{'dm': 
                       {'apple': 3, 'banana': 2}}, 
            {'jz': {'banana': 3, 'cherry': 2}}, 
            {'owd': {'apple': 2, 'cherry': 3}}]
        self.assertEqual(InventoryAllocator().cheapest_shipment(order,
            inventory), result)

    # Multiple order from different warehouses with an invalid order
    def test_multiple_orders_invalid(self):
        order = {'apple': 5, 'banana': 5, 'cherry': 10}
        inventory = [{'name': 'owd', 
                       'inventory': 
                           {'apple': 2, 'cherry': 3}},
            {'name': 'dm',
            'inventory': 
                {'apple': 5, 'banana': 2}},
            {'name': 'jz',
            'inventory': 
                {'banana': 4, 'cherry': 3}}]
        result = []
        self.assertEqual(InventoryAllocator().cheapest_shipment(order,
            inventory), result)

    # Invalid inventory results in no allocation
    def test_invalid_inventory(self):
        order = {'apple': 1}
        inventory = [{'failure': 'owd', 'failure': {'apple': 5}}]
        result = []
        with self.assertRaises(KeyError):
            InventoryAllocator().cheapest_shipment(order, inventory)

if __name__ == "__main__":
    unittest.main()
