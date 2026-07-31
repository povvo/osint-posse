-- Upgrade databases created before OSINT Posse 0.1.0.
ALTER TABLE progress ADD COLUMN completion_records TEXT DEFAULT '{}';
