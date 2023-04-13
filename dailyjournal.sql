CREATE TABLE `Entries` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` VARCHAR(50),
    `entry` VARCHAR(140),
    `mood_id` int,
    date DATE NOT NULL,
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

