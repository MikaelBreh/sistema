PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "cadastros_products"
(
    id               integer     not null
        primary key autoincrement,
    name             varchar(70) not null,
    product_code     varchar(10),
    product_bar_code varchar(13),
    box_bar_code     varchar(14),
    category         varchar(15) not null,
    unit             varchar(10) not null,
    box_quantity     integer,
    gross_weight     decimal(5, 2),
    net_weight       decimal(5, 2),
    ncm              varchar(14),
    cest             varchar(14)
);
INSERT INTO cadastros_products VALUES(1,'Lava Auto Concentrado 500ml Mil Milhas','5el','7896070312975','17896070312972','fabricados','un',20,0.53000000000000007105,0.5,'34025000','1100700');
INSERT INTO cadastros_products VALUES(2,'Lava Auto com Cera 500ml Mil Milhas','6el','7896070340091','17896070340098','fabricados','un',20,0.55,0.5,'34025000','1100700');
INSERT INTO cadastros_products VALUES(3,'Brilha Pneu Líquido 485ml Mil Milhas','7el','7896070314672','17896070314679','fabricados','un',20,0.56000000000000005329,0.47999999999999998223,'15200020',NULL);
INSERT INTO cadastros_products VALUES(4,'Brilha Pneu Gel 500g Mil Milhas','8el','7896070353831','17896070353838','fabricados','un',20,0.56000000000000005329,0.5,'15200020',NULL);
INSERT INTO cadastros_products VALUES(6,'Aromatizante Gel 60g Misto Mil Milhas','11el','1789607003020','17896070030203','misto','un',60,0.1,0.6,'33074900',NULL);
INSERT INTO cadastros_products VALUES(7,'Aromatizante Gel 60g Carro Novo Mil Milhas','11elc','7896070030206','17896070030203','fabricado','un',60,0.1,0.06,'33074900',NULL);
INSERT INTO cadastros_products VALUES(8,'Aromatizante Gel 60g Morango Mil Milhas','11elm','7896070030206','17896070030203','fabricado','un',60,0.1,0.06,'33074900',NULL);
INSERT INTO cadastros_products VALUES(9,'Aromatizante Gel 60g Talco Mil Milhas','11co','7896070030206','17896070030203','fabricados','un',60,0.1,0.06,'33074900',NULL);
INSERT INTO cadastros_products VALUES(10,'Aromatizante Gel 60g Lavanda Mil Milhas','11la','7896070030206','17896070030203','fabricados','un',60,0.1,0.06,'33074900',NULL);
INSERT INTO cadastros_products VALUES(11,'Aromatizante Gel 60g Citrico Mil Milhas','11ct','7896070030206','17896070030203','fabricados','un',60,0.1,0.06,'33074900',NULL);
INSERT INTO cadastros_products VALUES(12,'Aromatizante Gel 60g Tutti-Frutti Mil Milhas','11elt','7896070030206','17896070030203','fabricados','un',60,0.1,0.06,'33074900',NULL);
INSERT INTO cadastros_products VALUES(13,'Aromatizante Spray 60ml Talco Mil Milhas','26elt','7896070303553','17896070303550','fabricados','un',60,0.070000000000000008881,0.06,'33074900',NULL);
INSERT INTO cadastros_products VALUES(14,'Aromatizante Spray 60ml Carro Novo Mil Milhas','26elc','7896070303591','17896070303598','fabricados','un',60,0.070000000000000008881,0.06,'33074900',NULL);
INSERT INTO cadastros_products VALUES(15,'Aromatizante Spray 60ml Morango Mil Milhas','26elm','7896070603813','17896070603810','fabricados','un',60,0.070000000000000008881,0.06,'33074900',NULL);
INSERT INTO cadastros_products VALUES(16,'Aromatizante Spray 60ml Mil Milhas ','26el','7896070303553','17896070303550','fabricados','un',60,0.070000000000000008881,0.06,'33074900',NULL);
INSERT INTO cadastros_products VALUES(17,'Aromatizante Spray 60ml Carro Novo Mil Milhas','26elc','7898973182112','17898973182119','fabricados','un',60,0.070000000000000008881,0.06,'33074900',NULL);
INSERT INTO cadastros_products VALUES(18,'Aromatizante Spray 60ml Talco Mil Milhas','26elt','7898973182129','17898973182126','fabricados','un',60,0.070000000000000008881,0.06,'33074900',NULL);
INSERT INTO cadastros_products VALUES(19,'Antiembaçante Spray 60ml Mil Milhas','18el','7896070303508','17896070303505','fabricados','un',60,0.070000000000000008881,0.06,'34029039',NULL);
INSERT INTO cadastros_products VALUES(20,'Kit 2X1 Silicone Gel + Cera Lata Mil Milhas','21k','7896070000063','17896070000060','fabricados','un',12,0.45,0.45,'34053000',NULL);
INSERT INTO cadastros_products VALUES(21,'Kit 2X1 Concentrado + Cera Lata Mil Milhas','135','7898945110273','17898945110270','fabricados','un',8,0.85,0.85,'34053000',NULL);
INSERT INTO cadastros_products VALUES(22,'Kit 3X1 com Cera Color Mil Milhas','136','7898945110341','17898945110348','fabricados','un',10,0.85,0.85,'34029039','1100700');
INSERT INTO cadastros_products VALUES(23,'Kit 3X1 com Espuma Pequena Mil Milhas ','137','7898945110266','17898945110263','fabricados','un',5,1.1499999999999999111,1.1499999999999999111,'34029039','1100700');
INSERT INTO cadastros_products VALUES(24,'Kit 3X1 com Limpa Parabrisas Mil Milhas','31k','7893590347630','17893590347637','fabricados','un',5,1.1999999999999999644,1.1999999999999999644,'34029039','1100700');
INSERT INTO cadastros_products VALUES(25,'Kit 3X1 com Espuma Grande Mil Milhas ','14c','7893590347944','17893590347941','fabricados','un',5,1.1499999999999999111,1.1499999999999999111,'34029039','1100700');
INSERT INTO cadastros_products VALUES(26,'Kit 4X1 com Limpa Parabrisas Mil Milhas','13co','7893590347524','17893590347521','fabricados','un',5,1.25,1.25,'34029039','1100700');
INSERT INTO cadastros_products VALUES(27,'Kit 4X1 Especial com Silicone Gel Mil Milhas','44','7896070110342','17896070110349','fabricados','un',5,1.25,1.25,'34029039','1100700');
INSERT INTO cadastros_products VALUES(28,'Kit 4X1 Mil Milhas','13el','7896070493216','17896070493213','fabricados','un',5,1.5,1.5,'34029039','1100700');
INSERT INTO cadastros_products VALUES(29,'Kit 4X1 com Cera Lata Mil Milhas','43','7896070100701','17896070100708','fabricados','un',5,1.3999999999999999111,1.3999999999999999111,'34029039','1100700');
INSERT INTO cadastros_products VALUES(30,'Kit 5X1 Mil Milhas','14el','7896070944510','17896070944517','fabricados','un',5,1.6000000000000000888,1.6000000000000000888,'33074900',NULL);
INSERT INTO cadastros_products VALUES(31,'Kit  8X1 Mil Milhas','15c','7898945119009','17898945119006','fabricados','un',15,0.3,0.3,'63071000',NULL);
INSERT INTO cadastros_products VALUES(32,'Cera Lata 200g Mil Milhas','15el','7896070303522','17896070303529','fabricados','un',24,0.25,0.2,'34053000',NULL);
INSERT INTO cadastros_products VALUES(33,'Cera Color 200g Mil Milhas ','16el','7896070582705','17896070582702','fabricados','un',20,0.23000000000000002664,0.2,'34053000',NULL);
INSERT INTO cadastros_products VALUES(34,'Silicone Líquido 100ml Mil Milhas','1el','7896070312005','17896070312002','fabricados','un',60,0.1,0.1,'39100013',NULL);
INSERT INTO cadastros_products VALUES(35,'Silicone Líquido 200ml Mil Milhas','2ell','7896070312043','17896070312040','fabricados','un',16,0.16000000000000000888,0.2,'39100013',NULL);
INSERT INTO cadastros_products VALUES(36,'Silicone Gel 100g Carro Novo Mil Milhas','2el','7896070350052','17896070350059','fabricados','un',60,0.11000000000000000888,0.1,'39100013','');
INSERT INTO cadastros_products VALUES(37,'Silicone Gel  250g Carro Novo Mil Milhas','4el','7896070340107','17896070340104','fabricados','un',20,0.25,0.25,'39100013',NULL);
INSERT INTO cadastros_products VALUES(38,'Jet Cera Spray 500ml Mil Milhas ','30el','7896070303898','17896070303895','fabricados','un',20,0.55,0.5,'34053000',NULL);
INSERT INTO cadastros_products VALUES(39,'Limpa Parabrisas 100ml Mil Milhas','16c','7898945110099','17898945110096','fabricados','un',60,0.11999999999999999644,0.1,'34029039','1100700');
INSERT INTO cadastros_products VALUES(40,'Renovador de Parachoques 200ml Mil Milhas','27el','7896070136359','17896070136356','fabricados','un',25,0.27000000000000001776,0.2,'15200020',NULL);
INSERT INTO cadastros_products VALUES(41,'Aditivo Radiador Rosa 1 Litro Mil Milhas','3000','7896070904019','17896070904016','fabricados','un',12,1.0600000000000000532,1,'38237090',NULL);
INSERT INTO cadastros_products VALUES(42,'Estopa Automotiva de Limpeza 150g Mil Milhas','26e','7896070303003','17896070303000','fabricados','un',24,NULL,NULL,'52021000',NULL);
INSERT INTO cadastros_products VALUES(43,'Esponja de Limpeza Mil Milhas','27ele','7896070803374','17896070803371','fabricados','un',30,0.02,0.02,'39095029',NULL);
INSERT INTO cadastros_products VALUES(44,'Lava Auto Concentrado 1 Litro Mil Milhas','5e','7896070110403','17896070110400','fabricados','un',12,1.0700000000000000621,1,'34025000','1100700');
INSERT INTO cadastros_products VALUES(45,'Lava Auto com Cera 1 Litro Mil Milhas','6e','7896070110410','17896070110417','fabricados','un',12,1.090000000000000071,1,'34025000','1100700');
INSERT INTO cadastros_products VALUES(46,'Brilha Pneu Pretinho Líquido 1 Litro Mil Milhas','7e','7896070110397','17896070110394','fabricados','un',12,1.15999999999999992,1,'15200020',NULL);
INSERT INTO cadastros_products VALUES(47,'Cera PTFE para Correntes 90ml Mil Milhas ','1BK','7893590347692','17893590347699','fabricados','un',20,0.11999999999999999644,0.9,'34029039','1100700');
INSERT INTO cadastros_products VALUES(48,'Jet Cera Bike Spray 400ml Mil Milhas','4BK','7893590347654','17893590347651','fabricados','un',20,0.46000000000000005329,0.46000000000000005329,'34029039','1100700');
INSERT INTO cadastros_products VALUES(49,'Lava Bike Pronto Para Uso Spray 400ml Mil Milhas ','3BK','7893590347678','17893590347675','fabricados','un',20,0.46000000000000005329,0.46000000000000005329,'34029090','1100700');
INSERT INTO cadastros_products VALUES(50,'Lava Bikes Concentrado 400ml Mil Milhas ','5BK','7893590347685','17893590347682','fabricados','un',20,0.46000000000000005329,0.46000000000000005329,'34029090','1100700');
INSERT INTO cadastros_products VALUES(51,'Desengraxante Bike 400ml Mil Milhas','2BK','7893590347661','17893590347668','fabricados','un',20,0.44000000000000003552,0.4,'34029090','1100700');
INSERT INTO cadastros_products VALUES(52,'Limpa Cozinha Total Spray 910ml Casa Clean','9L','7893590347838','17893590347835','fabricados','un',10,1,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(53,'Limpa Cozinha Limpeza Pesada Spray 910ml Casa Clean','14L','7893590347821','17893590347828','fabricados','un',10,1,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(54,'Limpa Banheiro Total Spray 910ml Casa Clean','10L','7893590347814','17893590347811','fabricado','un',10,1,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(55,'Multiuso Spray 910ml Casa Clean','13L','7893590347760','17893590347767','fabricados','un',10,0.99000000000000003552,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(56,'Limpador Spray 910ml Floral Casa Clean','8L','7893590347784','17893590347781','fabricados','un',10,0.99000000000000003552,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(57,'Limpador Spray 910ml Fresh Casa Clean','6L','7893590347777','17893590347774','fabricados','un',10,0.99000000000000003552,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(58,'Limpador Spray 910ml Lavanda Casa Clean','7L','7893590347791','17893590347798','fabricados','un',10,0.99000000000000003552,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(59,'Limpador Spray 910ml Bambu Casa Clean','5L','7893590347807','17893590347804','fabricados','un',10,0.99000000000000003552,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(60,'Limpa Vidros Spray 910ml Casa Clean','1L','7893590347845','17893590347842','fabricados','un',10,0.99000000000000003552,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(61,'Limpa Vidros Refil 910ml Casa Clean','1LR','7896070000056','17896070000053','fabricados','un',10,0.99000000000000003552,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(62,'Limpador com Álcool Refil 910ml Bambu Casa Clean','5LR','7896070000087','17896070000084','fabricados','un',10,0.99000000000000003552,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(63,'Limpador com Álcool Refil 910ml Fresh Casa Clean','6LR','7896070000094','17896070000091','fabricados','un',10,0.99000000000000003552,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(64,'Limpador com Álcool Refil 910ml Lavanda Casa Clean ','7LR','7896070000100','17896070000107','fabricados','un',10,0.99000000000000003552,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(65,'Limpador com Álcool Refil 910ml Floral Casa Clean','8LR','7896070000131','17896070000138','fabricados','un',10,0.99000000000000003552,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(66,'Limpa Cozinha Total Refil 910ml Casa Clean','9LR','7896070000155','17896070000152','fabricados','un',10,1,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(67,'Limpa Cozinha Limpeza Pesada Refil 910ml Casa Clean','14LR','7896070000148','17896070000145','fabricados','un',10,1,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(68,'Limpa Banheiro Total Refil 910ml Casa Clean','10LR','7893590347517','17893590347514','fabricados','un',10,1,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(69,'Multiuso Refil 910ml Casa Clean','13LR','7896070000070','17896070000077','fabricados','un',10,0.99000000000000003552,0.90999999999999996447,'34025000','1100700');
INSERT INTO cadastros_products VALUES(70,'Kit Banheiro Total Spray + Refil 910ml Casa Clean','901','7893590347593','17893590347590','fabricados','un',5,2,1.8200000000000001065,'34025000','1100700');
INSERT INTO cadastros_products VALUES(71,'Kit Cozinha Total Spray + Refil 910ml Casa Clean','902','7893590347609','17893590347606','fabricados','un',5,2,1.8200000000000001065,'34025000','1100700');
INSERT INTO cadastros_products VALUES(72,'Kit Limpador com Álcool Floral Spray + Refil 910ml Casa Clean','903','7893590347647','17893590347644','fabricados','un',5,2,1.8200000000000001065,'34025000','1100700');
INSERT INTO cadastros_products VALUES(73,'Kit Limpa Vidros Spray + Refil 910ml Casa Clean','904','7893590347616','17893590347613','fabricados','un',5,2,1.8200000000000001065,'34025000','1100700');
INSERT INTO cadastros_products VALUES(74,'Kit Multiuso Spray + Refil 910ml Casa Clean','905','7893590347722','17893590347590','fabricados','un',5,2,1.8200000000000001065,'34025000','1100700');
INSERT INTO cadastros_products VALUES(75,'Kit Limpador com Álcool Lavanda Spray + Refil 910ml Casa Clean','906','7893590347623','17893590347620','fabricados','un',5,2,1.8200000000000001065,'34025000','1100700');
INSERT INTO cadastros_products VALUES(76,'Kit Limpador com Álcool Bambu Spray + Refil 910ml Casa Clean','907','7893590347708','17893590347705','fabricados','un',5,2,1.8200000000000001065,'34025000','1100700');
INSERT INTO cadastros_products VALUES(77,'Kit Limpador com Álcool Fresh Spray + Refil 910ml Casa Clean','908','7893590347715','17893590347712','fabricados','un',5,2,1.8200000000000001065,'34025000','1100700');
INSERT INTO cadastros_products VALUES(78,'Lava Louças Pump 1 Litro Maça Casa Clean','10','7898973182013','17898973182010','fabricados','un',12,1.0700000000000000621,1,'34025000','1100500');
INSERT INTO cadastros_products VALUES(79,'Lava Louças Pump 1 Litro Limão Casa Clean','11','7898973182020','17898973182027','fabricados','un',12,1.0700000000000000621,1,'34025000','1100500');
INSERT INTO cadastros_products VALUES(80,'Lava Louças Pump 1 Litro Coco Casa Clean','12','7898973182037','17898973182034','fabricados','un',12,1.0700000000000000621,1,'34025000','1100500');
INSERT INTO cadastros_products VALUES(81,'Lava Louças Pump 1 Litro Cristal Clean Neutro Casa Clean','13','7898973182044','17898973182041','fabricados','un',12,1.0700000000000000621,1,'34025000','1100500');
INSERT INTO cadastros_products VALUES(82,'Lava Louças Pump 1 Litro Cristal Blue Casa Clean','14','7898973182051','17898973182058','fabricados','un',12,1.0700000000000000621,1,'34025000','1100500');
INSERT INTO cadastros_products VALUES(83,'Lava Louças Refil 1 Litro Maça Casa Clean','20','7898973182105','17898973182102','fabricados','un',12,1.0700000000000000621,1,'34025000','1100500');
INSERT INTO cadastros_products VALUES(84,'Lava Louças Refil 1 Litro Limão Casa Clean','21','7898973182099','17898973182096','fabricados','un',12,1.0700000000000000621,1,'34025000','1100500');
INSERT INTO cadastros_products VALUES(85,'Lava Louças Refil 1 Litro Coco Casa Clean','22','7898973182082','17898973182089','fabricados','un',12,1.0700000000000000621,1,'34025000','1100500');
INSERT INTO cadastros_products VALUES(86,'Lava Louças Refil 1 Litro Cristal Clean Neutro Casa Clean','23','7898973182075','17898973182072','fabricados','un',12,1.0700000000000000621,1,'34025000','1100500');
INSERT INTO cadastros_products VALUES(87,'Lava Louças Refil 1 Litro Cristal Blue Casa Clean','24','7898973182068','17898973182065','fabricado','un',12,1.0700000000000000621,1,'34025000','1100500');
COMMIT;
