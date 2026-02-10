import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_dQxI6bev8yCq@ep-wispy-salad-adnoqxlk-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
engine = create_engine(DATABASE_URL.replace('postgresql://', 'postgresql+psycopg2://'))

try:
    with engine.connect() as conn:
        # Check if tags column exists in task table
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'task' AND column_name = 'tags'
        """))
        rows = result.fetchall()
        print('Tags column info:', rows)
        
        # Also check all columns in the task table
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'task'
            ORDER BY ordinal_position
        """))
        all_rows = result.fetchall()
        print('\nAll columns in task table:')
        for row in all_rows:
            print(f'  {row[0]}: {row[1]} (nullable: {row[2]})')
except Exception as e:
    print(f'Error connecting to database: {e}')
    import traceback
    traceback.print_exc()