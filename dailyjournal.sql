CREATE TABLE `Entries` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` VARCHAR(50),
    `entry` VARCHAR(140),
    `mood_id` int,
    `date` DATE NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Moods`(`id`)
);
CREATE TABLE `Moods` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label` VARCHAR(25)
);
CREATE TABLE `Tags` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `subject` VARCHAR(50)
);
CREATE TABLE `Entry_Tags` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `entry_id` INTEGER NOT NULL,
    `tag_id` INTEGER NOT NULL,
    FOREIGN KEY(`entry_id`) REFERENCES `Entries`(`id`)
    FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

INSERT INTO `Entries` VALUES (null, 'Javascript', 'I learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.', 1, 'Wed Sep 15 2021 10:10:47');
INSERT INTO `Entries` VALUES (null, 'Python', "Python is named after the Monty Python comedy group from the UK. I'm sad because I thought it was named after the snake", 4, 'Wed Sep 15 2021 10:11:33');
INSERT INTO `Entries` VALUES (null, 'Python', "Why did it take so long for python to have a switch statement? It's much cleaner than if/elif blocks", 3, 'Wed Sep 15 2021 10:13:11');
INSERT INTO `Entries` VALUES (null, 'Javascript', "Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.", 3, 'Wed Sep 15 2021 10:14:05');

INSERT INTO `Moods` VALUES (null, 'Happy');
INSERT INTO `Moods` VALUES (null, 'Sad');
INSERT INTO `Moods` VALUES (null, 'Angry');
INSERT INTO `Moods` VALUES (null, 'Ok');

INSERT INTO `Tags` VALUES (null, 'API');
INSERT INTO `Tags` VALUES (null, 'components');
INSERT INTO `Tags` VALUES (null, 'fetch');

INSERT INTO `Entry_Tags` VALUES (null, 4, 2);
INSERT INTO `Entry_Tags` VALUES (null, 4, 3);
INSERT INTO `Entry_Tags` VALUES (null, 9, 1);
INSERT INTO `Entry_Tags` VALUES (null, 9, 2);


UPDATE 'ENTRY_TAGS'
SET entry_id = 2
WHERE entry_id = 9


SELECT DISTINCT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.label,
            (
            SELECT GROUP_CONCAT(t.id)
            FROM Entry_tags et JOIN tags t ON et.tag_id = t.id
            WHERE et.entry_id = e.id
            ) as entry_tags
        FROM Entries e
        JOIN Moods m
            ON m.id = e.mood_id
        LEFT OUTER JOIN entry_tags et ON e.id = et.entry_id
