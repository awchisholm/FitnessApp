CREATE TABLE "User_Table" (
	"UserID"	INTEGER NOT NULL,
	"Username"	TEXT,
	"Password"	TEXT,
	"Forename"	TEXT,
	"Surname"	TEXT,
	"Email"		TEXT,
	"DateOfBirth"	TEXT,
	"GroupID"	INTEGER,
	FOREIGN KEY("GroupID") REFERENCES"Group"("GroupID"),
	PRIMARY KEY("UserID" AUTOINCREMENT)
);

CREATE TABLE "Subscriptions" (
	"SubID"	INTEGER NOT NULL,
	"SubscriptionActive"	TEXT,
	"SubscriptionStart"	TEXT,
	"SubscriptionEnd"	TEXT,
	"UserID"		INTEGER,
	FOREIGN KEY("UserID") REFERENCES"User_Table"("UserID"),
	PRIMARY KEY("SubID" AUTOINCREMENT)
);

CREATE TABLE "Group1" (
	"GroupID"	INTEGER NOT NULL,
	"GroupName"	TEXT,
	"GroupStarted"	TEXT,
	"GroupGoal"	TEXT,
	PRIMARY KEY("GroupID" AUTOINCREMENT)
);

CREATE TABLE "Tracking" (
	"TrackingID"	INTEGER NOT NULL,
	"Weight"	INTEGER,
	"Steps"		INTEGER,
	"DateAdded"	INTEGER,
	"UserID"	INTEGER,
	FOREIGN KEY("UserID") REFERENCES "User_Table"("UserID"),
	PRIMARY KEY("TrackingID" AUTOINCREMENT)
);
