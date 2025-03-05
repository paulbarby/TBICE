import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any

class Database:
    def __init__(self, db_path: str = "image_converter.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Profiles table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            source_folder TEXT,
            destination_folder TEXT,
            output_format TEXT,
            filename_pattern TEXT,
            is_active INTEGER,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
        ''')
        
        # Image settings table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS image_settings (
            id INTEGER PRIMARY KEY,
            profile_id INTEGER,
            resize_width INTEGER,
            resize_height INTEGER,
            resize_method TEXT DEFAULT 'Dimensions',
            keep_aspect_ratio INTEGER DEFAULT 0,
            crop_left INTEGER,
            crop_top INTEGER,
            crop_right INTEGER,
            crop_bottom INTEGER,
            brightness REAL,
            contrast REAL,
            sharpness REAL,
            saturation REAL,
            quality INTEGER,
            FOREIGN KEY (profile_id) REFERENCES profiles (id) ON DELETE CASCADE
        )
        ''')
        
        # Processed files table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_files (
            id INTEGER PRIMARY KEY,
            profile_id INTEGER,
            source_path TEXT,
            destination_path TEXT,
            processed_at TIMESTAMP,
            FOREIGN KEY (profile_id) REFERENCES profiles (id) ON DELETE CASCADE
        )
        ''')
        
        self.conn.commit()
    
    def save_profile(self, profile_data, settings_data):
        current_time = datetime.now()
        
        # Check if profile exists
        self.cursor.execute("SELECT id FROM profiles WHERE name = ?", (profile_data['name'],))
        result = self.cursor.fetchone()
        
        if result:
            # Update existing profile
            profile_id = result[0]
            self.cursor.execute('''
            UPDATE profiles 
            SET source_folder = ?, destination_folder = ?, output_format = ?,
                filename_pattern = ?, is_active = ?, updated_at = ?
            WHERE id = ?
            ''', (
                profile_data['source_folder'],
                profile_data['destination_folder'],
                profile_data['output_format'],
                profile_data['filename_pattern'],
                profile_data['is_active'],
                current_time,
                profile_id
            ))
            
            # Update image settings
            self.cursor.execute('''
            UPDATE image_settings
            SET resize_width = ?, resize_height = ?, resize_method = ?, keep_aspect_ratio = ?,
                crop_left = ?, crop_top = ?, crop_right = ?, crop_bottom = ?,
                brightness = ?, contrast = ?, sharpness = ?, saturation = ?,
                quality = ?
            WHERE profile_id = ?
            ''', (
                settings_data['resize_width'],
                settings_data['resize_height'],
                settings_data.get('resize_method', 'Dimensions'),
                settings_data.get('keep_aspect_ratio', 0),
                settings_data['crop_left'],
                settings_data['crop_top'],
                settings_data['crop_right'],
                settings_data['crop_bottom'],
                settings_data['brightness'],
                settings_data['contrast'],
                settings_data['sharpness'],
                settings_data['saturation'],
                settings_data['quality'],
                profile_id
            ))
        else:
            # Create new profile
            self.cursor.execute('''
            INSERT INTO profiles (
                name, source_folder, destination_folder, output_format,
                filename_pattern, is_active, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                profile_data['name'],
                profile_data['source_folder'],
                profile_data['destination_folder'],
                profile_data['output_format'],
                profile_data['filename_pattern'],
                profile_data['is_active'],
                current_time,
                current_time
            ))
            
            profile_id = self.cursor.lastrowid
            
            # Create image settings
            self.cursor.execute('''
            INSERT INTO image_settings (
                profile_id, resize_width, resize_height, resize_method, keep_aspect_ratio,
                crop_left, crop_top, crop_right, crop_bottom,
                brightness, contrast, sharpness, saturation, 
                quality
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                profile_id,
                settings_data['resize_width'],
                settings_data['resize_height'],
                settings_data.get('resize_method', 'Dimensions'),
                settings_data.get('keep_aspect_ratio', 0),
                settings_data['crop_left'],
                settings_data['crop_top'],
                settings_data['crop_right'],
                settings_data['crop_bottom'],
                settings_data['brightness'],
                settings_data['contrast'],
                settings_data['sharpness'],
                settings_data['saturation'],
                settings_data['quality']
            ))
        
        self.conn.commit()
        return profile_id
    
    def get_profiles(self):
        self.cursor.execute('''
        SELECT p.id, p.name, p.source_folder, p.destination_folder, 
               p.output_format, p.filename_pattern, p.is_active,
               s.resize_width, s.resize_height, s.resize_method, s.keep_aspect_ratio,
               s.crop_left, s.crop_top, s.crop_right, s.crop_bottom,
               s.brightness, s.contrast, s.sharpness, s.saturation, s.quality
        FROM profiles p
        JOIN image_settings s ON p.id = s.profile_id
        ORDER BY p.name
        ''')
        
        columns = [
            'id', 'name', 'source_folder', 'destination_folder', 
            'output_format', 'filename_pattern', 'is_active',
            'resize_width', 'resize_height', 'resize_method', 'keep_aspect_ratio',
            'crop_left', 'crop_top', 'crop_right', 'crop_bottom',
            'brightness', 'contrast', 'sharpness', 'saturation', 'quality'
        ]
        
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    def get_profile(self, profile_id):
        self.cursor.execute('''
        SELECT p.id, p.name, p.source_folder, p.destination_folder, 
               p.output_format, p.filename_pattern, p.is_active,
               s.resize_width, s.resize_height, s.resize_method, s.keep_aspect_ratio,
               s.crop_left, s.crop_top, s.crop_right, s.crop_bottom,
               s.brightness, s.contrast, s.sharpness, s.saturation, s.quality
        FROM profiles p
        JOIN image_settings s ON p.id = s.profile_id
        WHERE p.id = ?
        ''', (profile_id,))
        
        row = self.cursor.fetchone()
        if not row:
            return None
            
        columns = [
            'id', 'name', 'source_folder', 'destination_folder', 
            'output_format', 'filename_pattern', 'is_active',
            'resize_width', 'resize_height', 'resize_method', 'keep_aspect_ratio',
            'crop_left', 'crop_top', 'crop_right', 'crop_bottom',
            'brightness', 'contrast', 'sharpness', 'saturation', 'quality'
        ]
        
        return dict(zip(columns, row))
    
    def update_profile_status(self, profile_id, is_active):
        self.cursor.execute('''
        UPDATE profiles SET is_active = ?, updated_at = ?
        WHERE id = ?
        ''', (is_active, datetime.now(), profile_id))
        self.conn.commit()
    
    def delete_profile(self, profile_id):
        self.cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
        self.conn.commit()
    
    def log_processed_file(self, profile_id, source_path, destination_path):
        self.cursor.execute('''
        INSERT INTO processed_files (profile_id, source_path, destination_path, processed_at)
        VALUES (?, ?, ?, ?)
        ''', (profile_id, source_path, destination_path, datetime.now()))
        self.conn.commit()
    
    def close(self):
        self.conn.close()