USE task1;

CREATE INDEX idx_students_room ON students USING HASH (room);
CREATE INDEX idx_rooms_id ON rooms USING HASH (id);
CREATE INDEX idx_rooms_name ON rooms USING HASH (name);
CREATE INDEX idx_students_birthday ON students(birthday);
CREATE INDEX idx_students_sex ON students USING HASH (sex);
