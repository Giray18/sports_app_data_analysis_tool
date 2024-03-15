import numpy as np
import pandas as pd
import random
from collections import defaultdict
import json
import re
import os


# #Calculating Total Team Goals
# class league_analyzer:

#     def __init__(self, df, team):
#         self.df = df
#         self.team = team.lower()

#     def total_goals(self): 
#         ''' Calculating total goals scored by selected team'''
#         # Creating regex pattern for passed team name parameter
#         pattern_team = re.compile(rf"{self.team}\s[0-9]+", re.IGNORECASE)
#         # Getting game ids from index column
#         game_ids = self.df.index.to_list()
#         #Getting team match results and team scores in matches
#         game_scores = [self.df["event"][game_id][0] for game_id in game_ids if self.team in self.df["event"][game_id][0].lower()]
#         # game_scores_lower = [x.lower() for x in game_scores]
#         team_scores = [re.findall(pattern_team, i) for i in game_scores]
#         d = defaultdict(int)
#         # Looping through team scores to sum team scores in games
#         for x in team_scores:
#             for y in x:
#                 d[self.team] += int(y.split(" ")[-1])
#         return d[self.team]

# def class_method_decorator(cls):
#     def new_method(self):
#         print("Class method has been decorated")
#         return cls.total_goals(self)
#     league_analyzer.original_method = league_analyzer.class_method
#     league_analyzer.class_method = new_method
#     return league_analyzer

#Calculating Total Team Goals
# @class_method_decorator

class goal_analyzer:
    '''Class to create quick analysis of teams goal/shoot performance'''
    def __init__(self, df, team):
        self.df = df
        self.team = team.lower()

    def total_goals(self): 
        ''' Calculating total goals scored by selected team through entire dataset'''
        # Creating regex pattern for passed team name parameter
        pattern_team = re.compile(rf"{self.team}\s[0-9]+", re.IGNORECASE)
        # Getting game ids from index column
        game_ids = self.df.index.to_list()
        # Getting team match results and team scores in matches
        game_scores = [self.df["event"][game_id][0] for game_id in game_ids if self.team in self.df["event"][game_id][0].lower()]
        # Filtering needed team scores by regex pattern
        team_scores = [re.findall(pattern_team, i) for i in game_scores]
        d = defaultdict(int)
        # Looping through team scores to sum team scores in games
        for games in team_scores:
            for game in games:
                d[self.team] += int(game.split(" ")[-1])
        return d[self.team]

    def total_goal_perc(self):
        ''' Calculating percent of total goals scored by selected team'''
        # Calling total_goals method to get team goals
        team_goals = self.total_goals()
        # Getting goal amount scored by all teams
        pattern_number = re.compile(r"[0-9]+", re.IGNORECASE)
        game_ids = self.df.index.to_list()
        # Getting team match results and team scores in matches
        game_scores = [self.df["event"][game_id][0] for game_id in game_ids]
        # Filtering needed team scores by regex pattern
        team_scores = [re.findall(pattern_number, i) for i in game_scores]
        # Counting all goals scored in league by loop
        goals = 0
        for games in team_scores:
            for goal_num in games:
                goals += int(goal_num)
        percent = team_goals/goals
        percentage = "{:.2%}".format(percent)
        return percentage

    def total_shots(self): 
        ''' Calculating total shots on goal done by selected team through entire dataset'''
        # Getting game ids from index column
        game_ids = self.df.index.to_list()
        # Getting team match results and team scores in matches
        home_game_shoots = [int(self.df["team1_stat"][game_id]['shots_on_target']) for game_id in game_ids if self.team in self.df['event'][game_id][0].lower()]
        away_game_shoots = [int(self.df["team2_stat"][game_id]['shots_on_target']) for game_id in game_ids if self.team in self.df['event'][game_id][0].lower()]
        home_game_shoots.extend(away_game_shoots)
        shots = 0
        # Looping through team scores to sum team scores in games
        for g_shots in home_game_shoots:
            shots += g_shots
        return shots

    def shot_accuracy(self):
        ''' Calculating hit rate of teams from shots find target and goals scored'''
        # Calling total_goals method to get team goals
        team_shots_on_goal = self.total_shots()
        # Calling total_goals method to get team goals
        team_goals = self.total_goals()
        shot_accuracy = team_goals/team_shots_on_goal
        percentage = "{:.2%}".format(shot_accuracy)
        return percentage

class line_ups(goal_analyzer):
    ''' Class to get line up performance of a player'''
    def __init__(self, df, team,player):
        super().__init__(df, team)
        self.player = player.lower()

    def line_up_count(self):
        game_ids = self.df.index.to_list()
        home_game_starts = [self.df["team1_startings"][game_id] for game_id in game_ids if self.player in self.df['team1_startings'][game_id]]
        home_game_starts = sum([i.count(self.player) for i in home_game_starts])
        away_game_starts = [self.df["team2_startings"][game_id] for game_id in game_ids if self.player in self.df['team2_startings'][game_id]]
        away_game_starts = sum([i.count(self.player) for i in away_game_starts])
        total_line_ups = home_game_starts + away_game_starts
        return total_line_ups





    

