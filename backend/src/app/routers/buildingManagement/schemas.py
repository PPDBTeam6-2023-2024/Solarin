import datetime

from pydantic import BaseModel
from enum import Enum
from typing import Optional


class TimestampDone(BaseModel):
    day: int
    hours: int
    minutes: int
    seconds: int


class TrainingQueueEntry(BaseModel):
    id: int
    building_id: int
    army_id: int
    train_remaining: int
    troop_type: str
    rank: int
    troop_size: int
    unit_training_time: int
