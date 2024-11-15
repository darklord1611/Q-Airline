# supabase_client.py
import os
from supabase import create_client, Client
from config import SUPABASE_KEY, SUPABASE_URL


# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
