# Таблица к домашнему заданию по оптимизации в Django (python lesson 27)

| Type of optimization            | URL | Before SQL req. | After SQL req. |
|---------------------------------|----------|-----------------|----------------|
| cached_property(test 1 user)    | max_discount.html | 7               | 2              |
| WITH(test 1 user)               | max_discount.html| 2               | 1              |
| select_related (test 100 users) | max_discount.html| 10              | 1              |








