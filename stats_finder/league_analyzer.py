import numpy as np
import pandas as pd
import random
from collections import defaultdict
import json
import re
import os


#Calculating Total Team Goals
class league_analyzer:

    def __init__(self, df, team):
        self.df = df
        self.team = team.lower()

    def total_goals(self): 
        ''' Calculating total goals scored by selected team'''
        # Creating regex pattern for passed team name parameter
        pattern_team = re.compile(rf"{self.team}\s[0-9]+", re.IGNORECASE)
        # Getting game ids from index column
        game_ids = self.df.index.to_list()
        #Getting team match results and team scores in matches
        game_scores = [self.df["event"][game_id][0] for game_id in game_ids if self.team in self.df["event"][game_id][0].lower()]
        # game_scores_lower = [x.lower() for x in game_scores]
        team_scores = [re.findall(pattern_team, i) for i in game_scores]
        d = defaultdict(int)
        # Looping through team scores to sum team scores in games
        for x in team_scores:
            for y in x:
                d[self.team] += int(y.split(" ")[-1])
        return d[self.team]

