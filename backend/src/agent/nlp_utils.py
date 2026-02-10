"""
Natural Language Processing utilities for extracting task parameters
"""

import re
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional, Tuple


def extract_priority(text: str) -> Optional[str]:
    """
    Extract priority level from natural language text.

    Returns: "high", "medium", "low", or None
    """
    text_lower = text.lower()

    # High priority indicators
    if any(word in text_lower for word in ['urgent', 'asap', 'critical', 'important', 'high priority', 'high']):
        return "high"

    # Low priority indicators
    if any(word in text_lower for word in ['low priority', 'low', 'whenever', 'someday', 'maybe']):
        return "low"

    # Medium is default, but check for explicit mentions
    if any(word in text_lower for word in ['medium priority', 'medium', 'normal']):
        return "medium"

    return None


def extract_tags(text: str) -> List[str]:
    """
    Extract tags/categories from natural language text.

    Looks for patterns like:
    - "with tags work and urgent"
    - "tagged as personal"
    - "category work"
    - "#work #urgent"
    """
    tags = []
    text_lower = text.lower()

    # Pattern 1: "with tags X and Y" or "tagged as X"
    tag_patterns = [
        r'(?:with tags?|tagged as|categories?|labels?)\s+([a-z0-9,\s]+?)(?:\.|$|and)',
        r'(?:with tags?|tagged as)\s+([a-z0-9]+(?:\s+and\s+[a-z0-9]+)*)',
    ]

    for pattern in tag_patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            # Split by 'and' or comma
            tag_list = re.split(r'\s+and\s+|,\s*', match)
            tags.extend([tag.strip() for tag in tag_list if tag.strip()])

    # Pattern 2: Hashtags
    hashtag_pattern = r'#([a-z0-9_]+)'
    hashtags = re.findall(hashtag_pattern, text_lower)
    tags.extend(hashtags)

    # Remove duplicates and limit to 10
    unique_tags = list(dict.fromkeys(tags))[:10]

    return unique_tags if unique_tags else []


def parse_relative_date(text: str) -> Optional[datetime]:
    """
    Parse relative date expressions like "tomorrow", "next week", "in 3 days".

    Returns: datetime object or None
    """
    text_lower = text.lower()
    now = datetime.now(timezone.utc)

    # Today
    if 'today' in text_lower:
        return now.replace(hour=23, minute=59, second=0, microsecond=0)

    # Tomorrow
    if 'tomorrow' in text_lower:
        return (now + timedelta(days=1)).replace(hour=23, minute=59, second=0, microsecond=0)

    # Next week
    if 'next week' in text_lower:
        return now + timedelta(days=7)

    # In X days/hours
    days_match = re.search(r'in (\d+) days?', text_lower)
    if days_match:
        days = int(days_match.group(1))
        return now + timedelta(days=days)

    hours_match = re.search(r'in (\d+) hours?', text_lower)
    if hours_match:
        hours = int(hours_match.group(1))
        return now + timedelta(hours=hours)

    # Day of week (next Monday, Tuesday, etc.)
    days_of_week = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6
    }

    for day_name, day_num in days_of_week.items():
        if day_name in text_lower:
            current_day = now.weekday()
            days_ahead = (day_num - current_day) % 7
            if days_ahead == 0:
                days_ahead = 7  # Next week if same day
            return now + timedelta(days=days_ahead)

    return None


def extract_due_date(text: str) -> Optional[str]:
    """
    Extract due date from natural language text.

    Returns: ISO format datetime string or None
    """
    text_lower = text.lower()

    # Look for "due" keyword
    if 'due' not in text_lower:
        return None

    # Extract the part after "due"
    due_match = re.search(r'due\s+(.+?)(?:\.|,|$)', text_lower)
    if not due_match:
        return None

    due_text = due_match.group(1).strip()

    # Parse the relative date
    due_datetime = parse_relative_date(due_text)

    if due_datetime:
        return due_datetime.isoformat()

    return None


def extract_reminder(text: str, due_date: Optional[str] = None) -> Optional[str]:
    """
    Extract reminder time from natural language text.

    Returns: ISO format datetime string or None
    """
    text_lower = text.lower()

    # Look for "remind" keyword
    if 'remind' not in text_lower:
        return None

    now = datetime.now(timezone.utc)

    # Pattern: "remind me X hours/minutes before"
    before_match = re.search(r'remind(?:\s+me)?\s+(\d+)\s+(hour|minute)s?\s+before', text_lower)
    if before_match and due_date:
        amount = int(before_match.group(1))
        unit = before_match.group(2)

        due_dt = datetime.fromisoformat(due_date.replace('Z', '+00:00'))

        if unit == 'hour':
            remind_dt = due_dt - timedelta(hours=amount)
        else:  # minute
            remind_dt = due_dt - timedelta(minutes=amount)

        return remind_dt.isoformat()

    # Pattern: "remind me tomorrow at 3pm"
    remind_match = re.search(r'remind(?:\s+me)?\s+(.+?)(?:\.|,|$)', text_lower)
    if remind_match:
        remind_text = remind_match.group(1).strip()
        remind_dt = parse_relative_date(remind_text)

        if remind_dt:
            return remind_dt.isoformat()

    return None


def extract_recurrence_pattern(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract recurrence pattern from natural language text.

    Returns: Recurrence pattern dict or None
    """
    text_lower = text.lower()

    # Daily pattern
    if any(word in text_lower for word in ['daily', 'every day', 'each day']):
        return {
            "type": "daily",
            "interval": 1
        }

    # Weekly pattern
    if any(word in text_lower for word in ['weekly', 'every week']):
        # Check for specific days
        days_of_week = []
        day_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

        for day in day_names:
            if day in text_lower:
                days_of_week.append(day)

        pattern = {
            "type": "weekly",
            "interval": 1
        }

        if days_of_week:
            pattern["days_of_week"] = days_of_week

        return pattern

    # Monthly pattern
    if any(word in text_lower for word in ['monthly', 'every month']):
        return {
            "type": "monthly",
            "interval": 1
        }

    # Yearly pattern
    if any(word in text_lower for word in ['yearly', 'every year', 'annually']):
        return {
            "type": "yearly",
            "interval": 1
        }

    return None


def extract_search_query(text: str) -> Optional[str]:
    """
    Extract search query from natural language text.

    Returns: Search query string or None
    """
    text_lower = text.lower()

    # Look for search keywords
    search_patterns = [
        r'(?:search|find|look for)\s+(?:tasks?\s+)?(?:about|for|with|containing)\s+(.+?)(?:\.|$)',
        r'(?:search|find)\s+(.+?)(?:\.|$)',
    ]

    for pattern in search_patterns:
        match = re.search(pattern, text_lower)
        if match:
            return match.group(1).strip()

    return None


def extract_task_parameters(text: str) -> Dict[str, Any]:
    """
    Extract all task parameters from natural language text.

    Returns: Dictionary with extracted parameters
    """
    params = {}

    # Extract priority
    priority = extract_priority(text)
    if priority:
        params['priority'] = priority

    # Extract tags
    tags = extract_tags(text)
    if tags:
        params['tags'] = tags

    # Extract due date
    due_date = extract_due_date(text)
    if due_date:
        params['due_date'] = due_date

    # Extract reminder (needs due_date if available)
    reminder = extract_reminder(text, due_date)
    if reminder:
        params['remind_at'] = reminder

    # Extract recurrence pattern
    recurrence = extract_recurrence_pattern(text)
    if recurrence:
        params['is_recurring'] = True
        params['recurrence_pattern'] = recurrence

    return params
