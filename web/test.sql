-- Database: `test`

-- Table structure for table `Course`
CREATE TABLE Course (
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT NOT NULL,
  Credit INTEGER NOT NULL,
  Required INTEGER NOT NULL,
  Quota INTEGER NOT NULL,
  Dept TEXT NOT NULL,
  Year INTEGER NOT NULL
);

-- Dumping data for table `Course`
INSERT INTO Course (ID, Name, Credit, Required, Quota, Dept, Year) VALUES
(1, 'Engineering Mathematics', 2, 0, 80, 'IECS', 2),
(2, 'Computer Theroerm', 2, 1, 80, 'IECS', 1),
(3, 'Computer Network', 3, 1, 70, 'IECS', 2),
(4, 'English_advanced', 2, 1, 25, 'LANG', 2),
(5, 'NLP', 3, 0, 80, 'IECS', 3),
(6, 'Data Structure', 3, 1, 80, 'IECS', 2),
(7, 'FYP', 6, 1, 200, 'IECS', 4),
(8, 'Linear Algebra', 3, 1, 100, 'IECS', 1),
(9, 'Calcus(I)', 3, 1, 60, 'IECS', 1),
(10, 'Deep Learning', 3, 0, 72, 'IECS', 4),
(11, 'Software Testing', 3, 0, 70, 'IECS', 3),
(12, 'OOP', 3, 0, 60, 'IECS', 2);

-- Table structure for table `Student`
CREATE TABLE Student (
  ID INTEGER PRIMARY KEY,
  First_Name TEXT NOT NULL,
  Last_Name TEXT NOT NULL,
  Year INTEGER NOT NULL,
  Dept TEXT NOT NULL,
  Password TEXT NOT NULL -- 添加 Password 欄位
);

-- Dumping data for table `Student`
INSERT INTO Student (ID, First_Name, Last_Name, Year, Dept, Password) VALUES
(12345678, 'Peter', 'Chan', 3, 'IECS', 'test1234'); -- 設置一個示範密碼

-- Table structure for table `Subscription`
CREATE TABLE Subscription (
  s_id INTEGER NOT NULL,
  c_id INTEGER NOT NULL,
  type INTEGER,
  PRIMARY KEY (s_id, c_id)
);

-- Dumping data for table `Subscription`
INSERT INTO Subscription (s_id, c_id, type) VALUES
(12345678, 1, 1),
(12345678, 2, 1),
(12345678, 5, 1),
(12345678, 8, 1),
(12345678, 9, 1),
(12345678, 10, 1),
(12345678, 11, 1);

-- Table structure for table `TimeTable`
CREATE TABLE TimeTable (
  ID INTEGER NOT NULL,
  Day INTEGER NOT NULL,
  Section INTEGER NOT NULL,
  PRIMARY KEY (ID, Day, Section)
);

-- Dumping data for table `TimeTable`
INSERT INTO TimeTable (ID, Day, Section) VALUES
(1, 4, 2),
(1, 4, 3),
(1, 4, 4),
(2, 2, 7),  
(2, 2, 8),  
(3, 3, 6),
(3, 4, 9),
(3, 4, 10),
(4, 1, 3),
(4, 1, 4),
(5, 3, 2),
(5, 3, 3),
(5, 3, 4),  
(6, 1, 3),
(6, 1, 4),
(6, 2, 8),  
(6, 3, 6),
(6, 3, 7),
(6, 3, 8),  
(7, 5, 12), 
(8, 2, 9),  
(8, 2, 10), 
(8, 2, 11), 
(9, 5, 6),  
(9, 5, 7),  
(9, 5, 8),  
(10, 4, 7),
(10, 4, 8), 
(10, 4, 9), 
(11, 1, 6),  
(11, 1, 7), 
(11, 1, 8), 
(12, 3, 11),
(12, 3, 12),
(12, 3, 13), 
(12, 3, 14); 

