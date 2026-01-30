Date: 2026-01-11
Course:
Tags: 

# Content

`typing.Protocol` 是 Python 中实现**结构化子类型(structural subtyping)**，也叫**鸭子类型(duck typing)**的正式方式。它在 Python 3.8+ 中引入。
Protocol enables **Open/Closed Principle** naturally
## 基本概念

**传统继承（名义子类型）：** 必须显式继承才能被认为是子类 **Protocol（结构化子类型）：** 只要对象有相同的方法/属性，就被认为兼容

---

## 简单示例

**不使用 Protocol（传统方式）：**

```python
from abc import ABC, abstractmethod

class Flyable(ABC):
    @abstractmethod
    def fly(self):
        pass

# 必须显式继承Flyable
class Bird(Flyable):
    def fly(self):
        print("鸟在飞")

class Airplane(Flyable):  # 必须继承
    def fly(self):
        print("飞机在飞")

def make_it_fly(obj: Flyable):
    obj.fly()

bird = Bird()
make_it_fly(bird)  # ✓
```

**使用 Protocol（鸭子类型）：**

```python
from typing import Protocol

class Flyable(Protocol):
    def fly(self) -> None:
        ...

# 不需要继承Flyable！只要有fly方法就行
class Bird:
    def fly(self):
        print("鸟在飞")

class Airplane:
    def fly(self):
        print("飞机在飞")

class Superhero:
    def fly(self):
        print("超级英雄在飞")

def make_it_fly(obj: Flyable):  # 接受任何有fly方法的对象
    obj.fly()

# 所有这些都能工作，即使没有继承Flyable
bird = Bird()
plane = Airplane()
hero = Superhero()

make_it_fly(bird)   # ✓
make_it_fly(plane)  # ✓
make_it_fly(hero)   # ✓
```

---

## 实际应用示例

### 示例 1：数据库连接

```python
from typing import Protocol

class DatabaseConnection(Protocol):
    def connect(self) -> None:
        ...
    
    def execute(self, query: str) -> list:
        ...
    
    def close(self) -> None:
        ...

# 不同的数据库实现，不需要继承DatabaseConnection
class MySQLConnection:
    def connect(self):
        print("连接到MySQL")
    
    def execute(self, query: str) -> list:
        print(f"执行MySQL查询: {query}")
        return [{"id": 1, "name": "张三"}]
    
    def close(self):
        print("关闭MySQL连接")

class PostgreSQLConnection:
    def connect(self):
        print("连接到PostgreSQL")
    
    def execute(self, query: str) -> list:
        print(f"执行PostgreSQL查询: {query}")
        return [{"id": 2, "name": "李四"}]
    
    def close(self):
        print("关闭PostgreSQL连接")

# 甚至可以用于第三方库的类，只要它们有相同的方法
class ThirdPartyDB:
    def connect(self):
        print("连接到第三方数据库")
    
    def execute(self, query: str) -> list:
        return []
    
    def close(self):
        print("关闭连接")

# 使用Protocol作为类型提示
def run_query(db: DatabaseConnection, query: str):
    db.connect()
    results = db.execute(query)
    db.close()
    return results

# 所有这些都可以工作
mysql = MySQLConnection()
run_query(mysql, "SELECT * FROM users")

postgres = PostgreSQLConnection()
run_query(postgres, "SELECT * FROM users")

third_party = ThirdPartyDB()
run_query(third_party, "SELECT * FROM users")
```

### 示例 2：可序列化对象

```python
from typing import Protocol

class Serializable(Protocol):
    def to_dict(self) -> dict:
        ...
    
    def to_json(self) -> str:
        ...

# 不同的类实现相同的接口，不需要继承
import json

class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
    
    def to_dict(self) -> dict:
        return {"name": self.name, "email": self.email}
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
    
    def to_dict(self) -> dict:
        return {"name": self.name, "price": self.price}
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

class Order:
    def __init__(self, order_id: int, total: float):
        self.order_id = order_id
        self.total = total
    
    def to_dict(self) -> dict:
        return {"order_id": self.order_id, "total": self.total}
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

# 通用的保存函数
def save_to_file(obj: Serializable, filename: str):
    with open(filename, 'w') as f:
        f.write(obj.to_json())
    print(f"已保存到 {filename}")

# 所有实现了to_dict和to_json的对象都可以使用
user = User("张三", "zhang@example.com")
save_to_file(user, "user.json")

product = Product("笔记本电脑", 5999.99)
save_to_file(product, "product.json")

order = Order(12345, 5999.99)
save_to_file(order, "order.json")
```

### 示例 3：支持长度和索引的对象

```python
from typing import Protocol

class Sized(Protocol):
    def __len__(self) -> int:
        ...

class SupportsGetItem(Protocol):
    def __getitem__(self, index: int):
        ...

# 任何实现了__len__和__getitem__的对象都可以使用
def get_first_element(container: Sized & SupportsGetItem):
    if len(container) > 0:
        return container[0]
    return None

# 这些都可以工作
print(get_first_element([1, 2, 3]))        # 1
print(get_first_element("hello"))          # h
print(get_first_element((10, 20, 30)))     # 10

# 自定义类也可以
class MyCollection:
    def __init__(self, items):
        self.items = items
    
    def __len__(self):
        return len(self.items)
    
    def __getitem__(self, index):
        return self.items[index]

my_coll = MyCollection([100, 200, 300])
print(get_first_element(my_coll))  # 100
```

---

## Protocol vs ABC (抽象基类)

|特性|Protocol|ABC|
|---|---|---|
|**继承要求**|不需要显式继承|必须显式继承|
|**类型检查**|结构化（鸭子类型）|名义化（继承关系）|
|**灵活性**|更灵活，适用于第三方库|更严格，明确的契约|
|**适用场景**|与现有代码集成|新项目，明确的继承层次|

```python
from typing import Protocol
from abc import ABC, abstractmethod

# Protocol方式 - 鸭子类型
class DrawableProtocol(Protocol):
    def draw(self) -> None:
        ...

# ABC方式 - 显式继承
class DrawableABC(ABC):
    @abstractmethod
    def draw(self) -> None:
        pass

# Protocol：不需要继承
class Circle:
    def draw(self):
        print("画圆")

# ABC：必须继承
class Square(DrawableABC):
    def draw(self):
        print("画正方形")

def render_protocol(obj: DrawableProtocol):
    obj.draw()

def render_abc(obj: DrawableABC):
    obj.draw()

circle = Circle()
render_protocol(circle)  # ✓ 可以工作

# render_abc(circle)  # ✗ 类型检查错误！Circle没有继承DrawableABC

square = Square()
render_abc(square)  # ✓ 可以工作
render_protocol(square)  # ✓ 也可以工作
```

---

## 何时使用 Protocol？

**使用 Protocol 当：**

- 需要与第三方库或现有代码集成
- 不想强制用户继承你的基类
- 想要更灵活的鸭子类型
- 需要描述对象应该有什么方法，而不关心它是什么类型

**使用 ABC 当：**

- 构建新的类层次结构
- 需要强制实现某些方法
- 想要明确的继承关系
- 需要共享代码实现（通过基类方法）

---

## 高级功能：运行时检查

```python
from typing import Protocol, runtime_checkable

@runtime_checkable  # 允许运行时isinstance检查
class Drawable(Protocol):
    def draw(self) -> None:
        ...

class Circle:
    def draw(self):
        print("画圆")

class Triangle:
    def area(self):
        return 10

circle = Circle()
triangle = Triangle()

# 运行时检查
print(isinstance(circle, Drawable))    # True
print(isinstance(triangle, Drawable))  # False
```

---

## 总结

`Protocol` 是 Python 类型系统的强大功能，它让你能够：

- ✅ 定义接口而不强制继承
- ✅ 与任何实现了相同方法的对象兼容
- ✅ 更好地支持鸭子类型
- ✅ 让类型检查工具（如 mypy）能够验证代码

这对于重构代码特别有用，因为你可以定义清晰的接口，而不需要修改现有的类层次结构！

# Note


# Reference

