USE Emotorad;

CREATE TABLE Contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phoneNumber VARCHAR(15),
    email VARCHAR(255),
    linkedId INT,
    linkPrecedence ENUM('primary', 'secondary') NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletedAt TIMESTAMP NULL,
    FOREIGN KEY (linkedId) REFERENCES Contacts(id) ON DELETE SET NULL
);
