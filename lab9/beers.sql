PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;


CREATE TABLE Customers (
    ID INT PRIMARY KEY,
    Name  VARCHAR(100),
    Owner_Name VARCHAR(100),
    Address VARCHAR(100),
    Latitude DECIMAL(10, 8),
    Longitude DECIMAL(10, 8),
    Postal_Code VARCHAR(10),
    City VARCHAR(50),
    Canton VARCHAR(10)
);

INSERT INTO Customers VALUES(22, 'Ferme Asile', 'Pascal Gremet', 'Promenade des Pêcheurs 10', 46.2291492, 7.2895976, '1950', 'Sion', 'VS');
INSERT INTO Customers VALUES(23, 'Brasserie du Grand-Pont', 'Roland Garin', 'Rue du Grand-Pont 6', 46.2335004, 7.2780625, '1950', 'Sion', 'VS');
INSERT INTO Customers VALUES(24, 'Burgerlution', 'Louis Monnet', 'Pl. du Midi 35', 46.2320137, 7.3592933, '1950', 'Sion', 'VS');
INSERT INTO Customers VALUES(25, 'Le Sil''O', 'Claude Ansermet', 'Cour de la Gare 25', 46.2291677, 7.3632145, '1950', 'Sion', 'VS');
INSERT INTO Customers VALUES(26, 'Abyssinia', 'Marie Dubois', 'Av. Ritz 13', 46.2353354, 7.3555281, '1950', 'Sion', 'VS');
INSERT INTO Customers VALUES(27, 'Pinte Contheysanne', 'Jean-Pierre Favre', 'Rue de Conthey 10', 46.2334199, 7.3573615, '1950', 'Sion', 'VS');
INSERT INTO Customers VALUES(28, 'Restaurant Brasserie Valaisanne', 'Sophie Morard', 'Rue du Vieux-Moulin 52', 46.2412601, 7.3583237, '1950', 'Sion', 'VS');
INSERT INTO Customers VALUES(29, 'La Sitterie', 'André Bonvin', 'Rte du Rawyl 41', 46.2412601, 7.3583237, '1950', 'Sion', 'VS');


CREATE TABLE Beers (
    ID INTEGER PRIMARY KEY,
    Beer_Name VARCHAR(100),
    Category VARCHAR(100),
    Unit_Price DECIMAL(10, 2)
);
INSERT INTO Beers VALUES(1,'Avalanche','Pale Ale',3);
INSERT INTO Beers VALUES(2,'Vintage IPA','IPA',3.1);
INSERT INTO Beers VALUES(3,'Tropical Stout','Stout',3.2);
INSERT INTO Beers VALUES(4,'Paratonnerre','Amber Ale',3.15);
INSERT INTO Beers VALUES(5,'BLIPA','Pale Ale',2.9);
INSERT INTO Beers VALUES(6,'Strong Ale Barrique','Barrique',3.3);
INSERT INTO Beers VALUES(7,'Belle Saison','Saison',2.9);


CREATE TABLE Deliveries (
    ID INTEGER PRIMARY KEY,
    Customer_ID INT,
    Delivery_Date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (Customer_ID) REFERENCES Customers(ID)
);

CREATE TABLE DeliveryItems (
    ID INTEGER PRIMARY KEY,
    Delivery_ID INT,
    Beer_ID INT,
    Quantity INT,
    FOREIGN KEY (Delivery_ID) REFERENCES Deliveries(ID),
    FOREIGN KEY (Beer_ID) REFERENCES Beers(ID)
);

COMMIT;