# -*- coding: utf-8 -*-
"""
Configuration Profiles - Save and load batch configurations

Authors: Vic Dang
Purpose: Allow multiple badge configuration presets
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from src.database import Database

LOGGER = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
PROFILES_DIR = PROJECT_ROOT / 'config' / 'profiles'


@dataclass
class BadgeProfile:
    """Batch configuration profile"""
    name: str
    description: str = ""
    badge_config: Dict = None
    crawler_config: Dict = None
    created_at: str = None
    updated_at: str = None
    is_default: bool = False

    def __post_init__(self):
        if self.badge_config is None:
            self.badge_config = self._default_badge_config()
        if self.crawler_config is None:
            self.crawler_config = self._default_crawler_config()
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.now().isoformat()

    @staticmethod
    def _default_badge_config() -> Dict:
        """Get default badge configuration"""
        return {
            'width': 1024,
            'height': 768,
            'template': 'default.png',
            'font': 'Arial',
            'text_size': 32,
            'background_color': '#FFFFFF',
        }

    @staticmethod
    def _default_crawler_config() -> Dict:
        """Get default crawler configuration"""
        return {
            'base_url': '',
            'workers': 5,
            'timeout': 30,
            'enabled': False,
            'retry_count': 3,
        }

    def to_dict(self) -> Dict:
        """Convert profile to dictionary"""
        return asdict(self)

    def to_json(self) -> str:
        """Convert profile to JSON"""
        return json.dumps(self.to_dict(), indent=2)

    @staticmethod
    def from_dict(data: Dict) -> 'BadgeProfile':
        """Create profile from dictionary"""
        return BadgeProfile(**data)

    @staticmethod
    def from_json(json_str: str) -> 'BadgeProfile':
        """Create profile from JSON"""
        data = json.loads(json_str)
        return BadgeProfile.from_dict(data)


class ProfileManager:
    """Manages configuration profiles"""

    def __init__(self, db: Database = None):
        """
        Initialize profile manager

        :param db: Database instance
        """
        self.db = db or Database()
        PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        self._create_default_profiles()

    def _create_default_profiles(self):
        """Create default profiles if they don't exist"""
        default_profiles = {
            'standard': BadgeProfile(
                name='standard',
                description='Standard badge configuration',
                badge_config={
                    'width': 1024,
                    'height': 768,
                    'template': 'default.png',
                    'font': 'Arial',
                    'text_size': 32,
                },
                is_default=True
            ),
            'high_quality': BadgeProfile(
                name='high_quality',
                description='High quality badge with larger dimensions',
                badge_config={
                    'width': 2048,
                    'height': 1536,
                    'template': 'premium.png',
                    'font': 'Arial',
                    'text_size': 48,
                }
            ),
            'compact': BadgeProfile(
                name='compact',
                description='Compact badge for quick processing',
                badge_config={
                    'width': 512,
                    'height': 384,
                    'template': 'compact.png',
                    'font': 'Arial',
                    'text_size': 24,
                }
            ),
        }

        for profile_name, profile in default_profiles.items():
            if not self._profile_exists(profile_name):
                self.save_profile(profile)
                LOGGER.info(f"Created default profile: {profile_name}")

    def save_profile(self, profile: BadgeProfile):
        """Save profile to database and file"""
        try:
            profile.updated_at = datetime.now().isoformat()

            # Save to database
            self.db.save_profile(
                profile_name=profile.name,
                config_data=profile.to_json(),
                is_default=profile.is_default
            )

            # Save to file
            profile_file = PROFILES_DIR / f"{profile.name}.json"
            with open(profile_file, 'w', encoding='utf-8') as f:
                f.write(profile.to_json())

            LOGGER.info(f"Saved profile: {profile.name}")

        except Exception as e:
            LOGGER.error(f"Failed to save profile: {e}")
            raise

    def load_profile(self, profile_name: str) -> Optional[BadgeProfile]:
        """Load profile from database or file"""
        try:
            # Try database first
            config_json = self.db.get_profile(profile_name)
            if config_json:
                return BadgeProfile.from_json(config_json)

            # Try file
            profile_file = PROFILES_DIR / f"{profile_name}.json"
            if profile_file.exists():
                with open(profile_file, 'r', encoding='utf-8') as f:
                    return BadgeProfile.from_json(f.read())

            LOGGER.warning(f"Profile not found: {profile_name}")
            return None

        except Exception as e:
            LOGGER.error(f"Failed to load profile: {e}")
            return None

    def list_profiles(self) -> List[str]:
        """List all available profiles"""
        try:
            # Get from database
            db_profiles = self.db.list_profiles()

            # Get from files
            file_profiles = [f.stem for f in PROFILES_DIR.glob("*.json")]

            # Combine and deduplicate
            all_profiles = list(set(db_profiles + file_profiles))
            return sorted(all_profiles)

        except Exception as e:
            LOGGER.error(f"Failed to list profiles: {e}")
            return []

    def delete_profile(self, profile_name: str):
        """Delete profile"""
        try:
            # Delete file
            profile_file = PROFILES_DIR / f"{profile_name}.json"
            if profile_file.exists():
                profile_file.unlink()

            LOGGER.info(f"Deleted profile: {profile_name}")

        except Exception as e:
            LOGGER.error(f"Failed to delete profile: {e}")
            raise

    def duplicate_profile(self, source_name: str, new_name: str):
        """Duplicate existing profile"""
        try:
            source = self.load_profile(source_name)
            if not source:
                raise ValueError(f"Source profile not found: {source_name}")

            # Create new profile based on source
            new_profile = BadgeProfile(
                name=new_name,
                description=f"Copy of {source_name}",
                badge_config=source.badge_config.copy(),
                crawler_config=source.crawler_config.copy()
            )

            self.save_profile(new_profile)
            LOGGER.info(f"Duplicated profile {source_name} → {new_name}")

        except Exception as e:
            LOGGER.error(f"Failed to duplicate profile: {e}")
            raise

    def export_profile(self, profile_name: str, export_path: Path):
        """Export profile to file"""
        try:
            profile = self.load_profile(profile_name)
            if not profile:
                raise ValueError(f"Profile not found: {profile_name}")

            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(profile.to_json())

            LOGGER.info(f"Exported profile: {profile_name} → {export_path}")

        except Exception as e:
            LOGGER.error(f"Failed to export profile: {e}")
            raise

    def import_profile(self, import_path: Path, profile_name: str = None):
        """Import profile from file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                profile = BadgeProfile.from_json(f.read())

            if profile_name:
                profile.name = profile_name

            self.save_profile(profile)
            LOGGER.info(f"Imported profile: {import_path} → {profile.name}")

        except Exception as e:
            LOGGER.error(f"Failed to import profile: {e}")
            raise

    def _profile_exists(self, profile_name: str) -> bool:
        """Check if profile exists"""
        profiles = self.list_profiles()
        return profile_name in profiles

    def create_custom_profile(self, name: str, description: str,
                            badge_config: Dict, crawler_config: Dict) -> BadgeProfile:
        """Create and save custom profile"""
        profile = BadgeProfile(
            name=name,
            description=description,
            badge_config=badge_config,
            crawler_config=crawler_config
        )
        self.save_profile(profile)
        return profile
