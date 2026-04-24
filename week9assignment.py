from dataclasses import dataclass,field
@dataclass
class Product:
    name :str
    price :float
    quantity :int
    def value(self) -> float:
        return self.quantity*self.price
@dataclass
class Warehouse:
    name :str
    products:list = field(default_factory=list)
    total_value: float = field(init=False)
    def __post_init__(self):
        self._total()
    def _total(self):
         self.total_value=0
         for product in self.products:
             self.total_value+=product.value()
    def add_product(self, product: Product):
        self.products.append(product)
        self._total()
    def sell(self, product_name: str, qty: int) -> bool:
        for product in self.products:
            if product_name==product.name:
                if product.quantity>=qty:
                    product.quantity-=qty
                    self._total()
                    return True
                else:
                    return False
    def restock(self, product_name: str, qty: int):
        for product in self.products:
            if product_name==product.name:
                product.quantity+=qty
                self._total()
                return
    def report(self) -> str:
        result = f"{self.name} Inventory:\n"
        for product in self.products:
            result+=f" {product.name}: {product.quantity} units @ ${product.price} each\n"
        
        result += f" Total value: ${self.total_value:.2f}"
        return result
p1 = Product("Laptop", 999.99, 10)
p2 = Product("Mouse", 29.99, 50)
p3 = Product("Keyboard", 79.99, 30)

w = Warehouse("TechDepot")
w.add_product(p1)
w.add_product(p2)
w.add_product(p3)

print(f"{w.total_value:.1f}")
print(w.sell("Laptop", 3))
print(w.sell("Laptop", 20))
w.restock("Mouse", 25)
print(w.report())
