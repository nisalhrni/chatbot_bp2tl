import os
from pathlib import Path

def setup_env():
    print("=" * 60)
    print("Setup Environment Variables untuk Backend")
    print("=" * 60)

    project_root = Path(__file__).parent.parent
    project_env = project_root / ".env"
    backend_env = Path(__file__).parent / ".env"

    if project_env.exists():
        print(f"Membaca credentials dari {project_env}")

        with open(project_env, 'r') as f:
            lines = f.readlines()

        supabase_url = None
        supabase_key = None

        for line in lines:
            if line.startswith('VITE_SUPABASE_URL='):
                supabase_url = line.split('=', 1)[1].strip()
            elif line.startswith('VITE_SUPABASE_ANON_KEY='):
                supabase_key = line.split('=', 1)[1].strip()

        if supabase_url and supabase_key:
            with open(backend_env, 'w') as f:
                f.write(f"SUPABASE_URL={supabase_url}\n")
                f.write(f"SUPABASE_KEY={supabase_key}\n")
                f.write(f"OLLAMA_BASE_URL=http://localhost:11434\n")

            print("✓ File .env backend berhasil dibuat!")
            print(f"  SUPABASE_URL: {supabase_url[:30]}...")
            print(f"  SUPABASE_KEY: {supabase_key[:30]}...")
            print(f"  OLLAMA_BASE_URL: http://localhost:11434")
        else:
            print("✗ Credentials Supabase tidak ditemukan di .env project")
            print("  Silakan setup manual di backend/.env")
    else:
        print("✗ File .env tidak ditemukan di root project")
        print("  Silakan setup manual di backend/.env")

    print("=" * 60)

if __name__ == "__main__":
    setup_env()
