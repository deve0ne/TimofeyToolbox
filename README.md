#Временная документация

## Основное окно

![Окно](https://drive.google.com/uc?export=view&id=1oxIbhrhKSdP66WTD3WUh3ueDgc5m9aSB)

### Mesh Check
В object mode показывает результаты проверки, в edit mode эти результаты становятся доступными для выбора.
Имейте в виду, что на данный момент проверять можно только один меш одновременно, при нескольких выбранных мешах будет проверен последний из них.

* No SG Faces - находит полигоны, которым не назначена конкретная группа сглаживания
* Loose Verts - находит точки и грани, к которым не привязано ни одного полигона
* Incorrect Geometry - находит грани, к которым привязано > 2 полигонов. Такие грани вызывают ошибки шейдинга.
* Degenerates - находит грани и полигоны, площадь которых > 0.0001 м. На данный момент работа над этой проверкой завершена не до конца, и она может принять за дегенерат нормальный маленький полигон. В будущем будет фикс.
* Manifold - проверка на "закрытую" геометрию. Нужна для физ коллизий.
* Check all - проверяет всё и сразу.

* Show/Hide Bounding Box - включает и выключает отображение BB для проверки выбраных мешей.

### Mesh operations
* Fix UV names - заменяет точки на нижние подчёркивания в названиях всех UV на сцене. Полезно для тех, кто пользуется RizomUV, т.к. он не поддерживает точки
* Box mapping - повторяет box mapping (2x2x2) с центром бокса в начале координат. Идентично 3Ds Max'овскому. Необходимо для правильного маппинга стен, полов и прочих горизонатльных и вертикальных поверхностей. Накладывается модификатором, так что чтобы увидеть изменения на развёртке, необходимо его применить
### Scene Optimization
* Limit Size - ограничивает размер текстур во вьюпорте до заданного разрешения, что значительно снижает потребление видеопамяти. Рекомендую ставить 256 на больших сценах, более чем достаточно для наших целей
* Anisotropic Filtration - отключение по идее чуть ускоряет отрисовку, но во вьюпорте появляются лесенки. По факту влияния на производительность не было замечено, в будущем, скорее всего, будет убрано.

## Прочие функции
### Advanced smoothing groups
Находится во вкладке Dagor, под smoothing группами.                                  
![Advanced SG](https://drive.google.com/uc?export=view&id=1JQC4LbiKQEZ2jnAqflC4jj5Ta4mfIos0)
* Advanced Recalculate SG - выполняет стандартный дагоровский Recalculate (то есть просчитывает группы сглаживания по хардам), после чего находит баги пересечения групп и переназначает их. Обычно немного увеличивает количество занятых smoothing групп. Полностью не протестировано, использовать с осторожностью.                    
![Принцип](https://drive.google.com/uc?export=view&id=1mpfsM43Umt6E86EIBnnLiigoUCRPHsva)
## Correct UV                                                                         
![Advanced SG](https://drive.google.com/uc?export=view&id=1OvQIaw-9iKMMr0-nCsOGnuuwajTf1YcQ)                                              
Дублирует эту галочку для удобства:                                                                      
![Advanced SG](https://drive.google.com/uc?export=view&id=12uXMdkAGoxYfcQWji_j2nPoF2pChfprH)
  
