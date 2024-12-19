// src/supabase.js
import { createClient } from '@supabase/supabase-js';

// Your Supabase URL and Anon Key (from the Supabase dashboard)
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_KEY;
const SUPABASE_STORAGE_FOLDER = import.meta.env.VITE_SUPABASE_STORAGE_FOLDER;
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

const supabase_storage_url = `${SUPABASE_URL}/storage/v1/object/public/${SUPABASE_STORAGE_FOLDER}`;


export { supabase, supabase_storage_url };
