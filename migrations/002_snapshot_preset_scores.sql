-- 002 snapshot preset columns
ALTER TABLE city_snapshots ADD COLUMN balanced_score REAL;
ALTER TABLE city_snapshots ADD COLUMN remote_work_score REAL;
ALTER TABLE city_snapshots ADD COLUMN community_score REAL;
