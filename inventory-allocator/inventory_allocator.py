from typing import Dict, List, Any

NAME = 'name'
INVENTORY = 'inventory'

class InventoryAllocator:
    """
    A class used to represent an Inventory Allocator

    Attributes
    ----------
    None

    Methods
    -------
    cheapest_shipment(order, inventory)
        Returns the cheapest shipment available given order and inventory,
        if valid
    """
    
    def cheapest_shipment(self, order: Dict[str, int], inventory: List[Dict[str, Any]]):
        """
        Returns the cheapest shipment available given order and inventory,
        if valid

        Parameters
        ----------
        order : Dict[str, int]
            The order of items which need to be shipped
        inventory: List[Dict[str, Any]]
            The available inventory in specified warehouse for various items
            
        Returns
        -------
        List[Dict[str, Dict[str, int]]]
            The list of cheapest item shipments from eligible warehouses, if valid
        """
        
        if not order or not inventory:
            return []

        inventory_item_map = {}
        warehouses_map = {}
        shipment = []
        
        """
        Populates an inventory item map with each item mapped to warehouse(s) 
        and the quantity of the item at specified warehouse
        """
        for warehouse in inventory:
            for item, supply in warehouse[INVENTORY].items():                
                warehouse_name = warehouse[NAME]
                
                if item in inventory_item_map:
                    inventory_item_map[item][warehouse_name] = supply
                else:
                    inventory_item_map[item] = { warehouse_name: supply }
        
        """
        Add eligible inventory to shipment array
        """
        for item, demand in order.items():
            # Check for positive demand
            if demand < 0 or item not in inventory_item_map:
                return []
            elif demand:
                for warehouse in inventory_item_map[item]:
                    # Warehouse index setup in shipment array
                    if warehouse not in warehouses_map:
                        shipment.append({ warehouse: {} })
                        warehouses_map[warehouse] = len(warehouses_map)
                    
                    index = warehouses_map[warehouse]
                    
                    # Check for non-negative supply
                    if inventory_item_map[item][warehouse] < 0:
                        return []

                    # Add item inventory from warehouse to shipment array
                    if demand <= inventory_item_map[item][warehouse]:
                        shipment[index][warehouse][item] = demand
                        demand = 0
                        break
                    else:
                        shipment[index][warehouse][item] = inventory_item_map[item][warehouse]
                        demand -= inventory_item_map[item][warehouse]

            if demand:
                return []
        
        # Return sorted shipment array (assumed from 3rd given sample test case)
        return sorted(shipment, key = lambda wh_name: list(wh_name.keys())[0])
