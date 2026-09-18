# Database initialization script

-- Enable pgvector extension for vector search
CREATE EXTENSION IF NOT EXISTS vector;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_timetables_train_no ON timetables(train_no);
CREATE INDEX IF NOT EXISTS idx_timetables_station_code ON timetables(station_code);
CREATE INDEX IF NOT EXISTS idx_train_events_train_no ON train_events(train_no);
CREATE INDEX IF NOT EXISTS idx_train_events_station_code ON train_events(station_code);
CREATE INDEX IF NOT EXISTS idx_train_events_created_at ON train_events(created_at);
CREATE INDEX IF NOT EXISTS idx_recommendations_train_no ON recommendations(train_no);
CREATE INDEX IF NOT EXISTS idx_recommendations_score ON recommendations(score);
CREATE INDEX IF NOT EXISTS idx_sop_chunks_doc_id ON sop_chunks(doc_id);
CREATE INDEX IF NOT EXISTS idx_query_logs_created_at ON query_logs(created_at);
