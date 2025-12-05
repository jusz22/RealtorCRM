export interface Image {
  id: string;
  listing_id: string;
  original_name: string;
  stored_name: string;
  content_type: string | null;
  size_bytes: number;
  storage_path: string;
  created_at: Date;
}
