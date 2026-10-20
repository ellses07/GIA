IF DB_ID('AromaDom') IS NOT NULL DROP DATABASE AromaDom;
CREATE DATABASE AromaDom;
GO
USE AromaDom;
GO

CREATE TABLE MaterialTypes(
    MaterialTypeId INT IDENTITY PRIMARY KEY,
    TypeName       NVARCHAR(150) NOT NULL UNIQUE,
    LossPercent    DECIMAL(7,4)  NOT NULL);

CREATE TABLE ProductTypes(
    ProductTypeId   INT IDENTITY PRIMARY KEY,
    TypeName        NVARCHAR(150) NOT NULL UNIQUE,
    TypeCoefficient DECIMAL(12,6) NOT NULL);

CREATE TABLE Materials(
    MaterialId      INT IDENTITY PRIMARY KEY,
    MaterialName    NVARCHAR(250) NOT NULL UNIQUE,
    MaterialTypeId  INT           NOT NULL REFERENCES MaterialTypes,
    UnitPrice       DECIMAL(18,2) NOT NULL,
    StockQuantity   DECIMAL(18,3) NOT NULL,
    MinimumQuantity DECIMAL(18,3) NOT NULL,
    PackageQuantity DECIMAL(18,3) NOT NULL,
    Unit            NVARCHAR(20)  NOT NULL);

CREATE TABLE Products(
    ProductId           INT IDENTITY PRIMARY KEY,
    Article             NVARCHAR(40)  NOT NULL UNIQUE,
    ProductName         NVARCHAR(250) NOT NULL UNIQUE,
    ProductTypeId       INT           NOT NULL REFERENCES ProductTypes,
    MinimumPartnerPrice DECIMAL(18,2) NOT NULL);

CREATE TABLE ProductMaterials(
    ProductId       INT           NOT NULL REFERENCES Products,
    MaterialId      INT           NOT NULL REFERENCES Materials,
    QuantityPerUnit DECIMAL(18,5) NOT NULL,
    PRIMARY KEY(ProductId, MaterialId));
GO

INSERT MaterialTypes(TypeName, LossPercent) VALUES
(N'Соевый воск',0.12),(N'Пчелиный воск',0.18),(N'Ароматическое масло',0.25),
(N'Краситель',0.08),(N'Фитиль',0.03),(N'Стеклянная тара',0.04),
(N'Керамическая тара',0.06),(N'Декор',0.10),(N'Упаковка',0.05),(N'Этикетка',0.02);

INSERT ProductTypes(TypeName, TypeCoefficient) VALUES
(N'Классическая свеча',1.00),(N'Премиальная свеча',1.15),(N'Подарочный набор',1.30),
(N'Интерьерная свеча',1.20),(N'Мини-свеча',0.80),(N'Сезонная коллекция',1.25);

INSERT Materials(MaterialName, MaterialTypeId, UnitPrice, StockQuantity, MinimumQuantity, PackageQuantity, Unit) VALUES
(N'Соевый воск премиум',        1, 890.00, 120,    40,    20,    N'кг'),
(N'Соевый воск EcoBlend',       1, 760.00,  95,    30,    25,    N'кг'),
(N'Пчелиный воск натуральный',  2,1450.00,  48,    15,    10,    N'кг'),
(N'Масло лаванды',              3,3200.00,  18.5,   6,     1,    N'л'),
(N'Масло ванили',               3,2950.00,  22,     8,     1,    N'л'),
(N'Масло цитрусовое',           3,2870.00,  16.7,   5,     1,    N'л'),
(N'Краситель янтарный',         4, 640.00,   6.2,   2,     0.5,  N'кг'),
(N'Краситель розовый',          4, 615.00,   5.1,   1.5,   0.5,  N'кг'),
(N'Фитиль хлопковый 8 см',      5,   4.50,2500,   800,   500,    N'шт'),
(N'Фитиль хлопковый 12 см',     5,   5.80,1800,   600,   400,    N'шт'),
(N'Стакан прозрачный 200 мл',   6,  28.00, 950,   300,   100,    N'шт'),
(N'Стакан матовый 250 мл',      6,  34.00, 620,   200,    60,    N'шт'),
(N'Чаша керамическая белая',    7,  72.00, 280,    80,    40,    N'шт'),
(N'Сухоцветы лаванды',          8, 520.00,   4.8,   1.5,   0.3,  N'кг'),
(N'Лента сатиновая бежевая',    9,  12.00, 340,   120,    50,    N'м'),
(N'Коробка подарочная малая',   9,  18.00, 420,   150,    50,    N'шт'),
(N'Этикетка фирменная круглая',10,   3.20,1800,   500,   250,    N'шт'),
(N'Наклейка предупреждающая',  10,   2.10,1600,   400,   200,    N'шт');

INSERT Products(Article, ProductName, ProductTypeId, MinimumPartnerPrice) VALUES
(N'AR-001',N'Свеча «Лавандовый вечер»',   1, 980.00),
(N'AR-002',N'Свеча «Ванильный крем»',     1, 950.00),
(N'AR-003',N'Свеча «Цитрусовый сад»',     1, 970.00),
(N'AR-004',N'Свеча «Белый мускус»',       2,1290.00),
(N'AR-005',N'Свеча «Дикая орхидея»',      2,1360.00),
(N'AR-006',N'Свеча «Теплый янтарь»',      4,1490.00),
(N'AR-007',N'Свеча «Сандаловое дерево»',  4,1520.00),
(N'AR-008',N'Мини-свеча «Лаванда»',       5, 420.00),
(N'AR-009',N'Мини-свеча «Ваниль»',        5, 410.00),
(N'AR-010',N'Мини-свеча «Цитрус»',        5, 430.00),
(N'AR-011',N'Набор «Уютный дом»',         3,2190.00),
(N'AR-012',N'Набор «Теплый вечер»',       3,2340.00),
(N'AR-013',N'Свеча «Зимние специи»',      6,1380.00),
(N'AR-014',N'Свеча «Хвойный лес»',        6,1410.00);

INSERT ProductMaterials(ProductId, MaterialId, QuantityPerUnit) VALUES
(1,1,0.18),(1,4,0.009),(1,9,1),(1,11,1),(1,17,1),
(2,1,0.18),(2,5,0.01),(2,9,1),(2,11,1),(2,17,1),
(3,2,0.175),(3,6,0.011),(3,9,1),(3,11,1),(3,17,1),
(4,1,0.22),(4,5,0.006),(4,10,1),(4,12,1),(4,17,1),
(5,1,0.225),(5,4,0.004),(5,10,1),(5,12,1),(5,17,1),
(6,3,0.28),(6,7,0.004),(6,10,1),(6,13,1),(6,17,1),
(7,3,0.285),(7,5,0.003),(7,10,1),(7,13,1),(7,17,1),
(8,2,0.07),(8,4,0.003),(8,9,1),(8,11,1),
(9,2,0.07),(9,5,0.003),(9,9,1),(9,11,1),
(10,2,0.07),(10,6,0.003),(10,9,1),(10,11,1),
(11,1,0.18),(11,4,0.009),(11,9,1),(11,11,1),(11,15,1.2),(11,16,1),(11,17,1),
(12,1,0.225),(12,5,0.01),(12,10,1),(12,12,1),(12,15,1.5),(12,16,1),(12,17,1),
(13,1,0.21),(13,5,0.008),(13,7,0.003),(13,10,1),(13,12,1),(13,18,1),
(14,1,0.215),(14,6,0.004),(14,7,0.002),(14,10,1),(14,12,1),(14,18,1);