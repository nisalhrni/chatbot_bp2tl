/*
  # Create BP2TL Chatbot Helpdesk Tables

  1. New Tables
    - `faq`
      - `id` (uuid, primary key)
      - `question` (text) - Pertanyaan FAQ
      - `answer` (text) - Jawaban FAQ
      - `embedding` (vector) - Embedding untuk semantic search
      - `created_at` (timestamptz)
    
    - `knowledge`
      - `id` (uuid, primary key)
      - `content` (text) - Konten pengetahuan
      - `source_file` (text) - Nama file sumber
      - `embedding` (vector) - Embedding untuk semantic search
      - `created_at` (timestamptz)
    
    - `chat_history`
      - `id` (uuid, primary key)
      - `session_id` (text) - ID sesi chat
      - `user_message` (text) - Pesan dari user
      - `bot_response` (text) - Response dari bot
      - `created_at` (timestamptz)

  2. Security
    - Enable RLS on all tables
    - Public read access untuk FAQ dan knowledge
    - Public insert access untuk chat_history (untuk keperluan demo)
*/

-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create FAQ table
CREATE TABLE IF NOT EXISTS faq (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  question text NOT NULL,
  answer text NOT NULL,
  embedding vector(768),
  created_at timestamptz DEFAULT now()
);

-- Create knowledge table
CREATE TABLE IF NOT EXISTS knowledge (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  content text NOT NULL,
  source_file text NOT NULL,
  embedding vector(768),
  created_at timestamptz DEFAULT now()
);

-- Create chat_history table
CREATE TABLE IF NOT EXISTS chat_history (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id text NOT NULL,
  user_message text NOT NULL,
  bot_response text NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Enable RLS
ALTER TABLE faq ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

-- Policies for FAQ (public read)
CREATE POLICY "Anyone can read FAQ"
  ON faq FOR SELECT
  USING (true);

-- Policies for knowledge (public read)
CREATE POLICY "Anyone can read knowledge"
  ON knowledge FOR SELECT
  USING (true);

-- Policies for chat_history (public insert and read for demo purposes)
CREATE POLICY "Anyone can insert chat history"
  ON chat_history FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Anyone can read chat history"
  ON chat_history FOR SELECT
  USING (true);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS faq_embedding_idx ON faq USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS knowledge_embedding_idx ON knowledge USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS chat_history_session_idx ON chat_history(session_id);
CREATE INDEX IF NOT EXISTS chat_history_created_at_idx ON chat_history(created_at);