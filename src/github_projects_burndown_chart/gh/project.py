from datetime import datetime
from typing import List
from dateutil.parser import isoparse

from config import config


class Project:
    def __init__(self, project_data, name):
        print(project_data)
        self.name = name
        self._cards: List[Card] = self.__parse_cards(project_data)

    def __parse_cards(self, project_data):
        card_data = project_data['items']['nodes']
        cards = [Card(data) for data in card_data]
        return cards

    @property
    def cards(self):
        return [card for card in self._cards]

    @property
    def total_points(self):
        return sum([card.points for card in self._cards])


class Card:
    def __init__(self, card_data):
        card_data = card_data['content'] if card_data['content'] else card_data
        self.created: datetime = self.__parse_createdAt(card_data)
        self.assigned: datetime = self.__parse_assignedAt(card_data)
        self.closed: datetime = self.__parse_closedAt(card_data)
        self.points = self.__parse_points(card_data)

    def __parse_assignedAt(self, card_data) -> datetime:
        assignedAt = None
        assignedDates = card_data.get('timelineItems', {}).get('nodes', [])
        if assignedDates:
            assignedAt = isoparse(assignedDates[0]['createdAt'])
        return assignedAt

    def __parse_createdAt(self, card_data) -> datetime:
        createdAt = None
        if card_data.get('createdAt'):
            createdAt = isoparse(card_data['createdAt'])
        return createdAt

    def __parse_closedAt(self, card_data) -> datetime:
        closedAt = None
        if card_data.get('closedAt'):
            closedAt = isoparse(card_data['closedAt'])
        return closedAt

    def __parse_points(self, card_data) -> int:
        card_points = 0
        points_label = config['settings']['points_label']
        if not points_label:
            card_points = 1
        else:
            card_labels = card_data.get('labels', {"nodes": []})['nodes']
            card_points = sum([int(label['name'][len(points_label):])
                              for label in card_labels
                              if points_label in label['name']])
        return card_points
