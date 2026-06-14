import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://bilujqezctzjaupfqigo.supabase.co";

const supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJpbHVqcWV6Y3R6amF1cGZxaWdvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk5NDQ0NTgsImV4cCI6MjA5NTUyMDQ1OH0.ezGEM61oZW39DG3wvmiRuzwgkoqUulWXHIRyUSxQTXA";

export const supabase = createClient(
  supabaseUrl,
  supabaseAnonKey
);