USE task1;

CREATE INDEX idx_students_room ON students(room) USING HASH;
CREATE INDEX idx_rooms_id ON rooms(id);
CREATE INDEX idx_rooms_name ON rooms(name) USING HASH;
CREATE INDEX idx_students_birthday ON students(birthday);
CREATE INDEX idx_students_sex ON students(sex) USING HASH;
