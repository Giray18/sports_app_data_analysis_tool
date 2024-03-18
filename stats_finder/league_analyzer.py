import numpy as np
import pandas as pd
import random
from collections import defaultdict
import json
import re
import os

class goal_analyzer:

    '''Class to create quick analysis of teams goal/shoot performance'''
    def __init__(self, df, team):
        self.df = df
        # lower and replace methods applied to provide integrity on team name inputs (e.g brighton & or brighton and )
        self.team = team.lower().replace("&","and")

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

    def team_scores(self):
        ''' Returns dataframe of teams and their scores during the season'''
         # Getting game ids from index column
        game_ids = self.df.index.to_list()
        # Saving all team names into a list
        team1_name = list(self.df["team1_name"])
        team2_name = list(self.df["team2_name"])
        team1_name.extend(team2_name)
        team_names = set(team1_name)
        # Getting team match results and team scores in matches
        game_scores = [self.df["event"][game_id][0] for game_id in game_ids]
        # Saving all team and scores in an empty dict
        team_scores_ult = {}
        # Looping through set to sum goals from teams
        for i in team_names:
            # Creating regex pattern for passed team name parameter
            pattern_team = re.compile(rf"{i}\s[0-9]+", re.IGNORECASE)
            # Filtering needed team scores by regex pattern
            team_scores = [re.findall(pattern_team, i) for i in game_scores if len(re.findall(pattern_team, i))>0]
            # Getting team scores and summing them then appending to a dict
            team_scores_ult[i] = sum([int(i[0].split(" ")[-1]) for i in team_scores])
        # Sorting the dict as descending
        team_scores_ult = sorted(team_scores_ult.items(), key=lambda item: item[1], reverse=True)
        # Saving dict to a pandas dataframe
        df = pd.DataFrame(data=team_scores_ult)
        df = df.rename(columns={0: "team_name", 1: "goal_total"})
        return df

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
        home_game_shoots = []
        shots = 0
        try:
            # Getting team match results and team scores in matches
            home_game_shoots = [int(self.df["team1_stat"][game_id]['shots_on_target']) for game_id in game_ids if self.team in self.df['event'][game_id][0].lower()]
            away_game_shoots = [int(self.df["team2_stat"][game_id]['shots_on_target']) for game_id in game_ids if self.team in self.df['event'][game_id][0].lower()]
            home_game_shoots.extend(away_game_shoots)
             # Looping through team scores to sum team scores in games
            for g_shots in home_game_shoots:
                shots += g_shots
        # except block will run if there are faulty inputs on dataset like float values instead integers
        except ValueError:
            shots = "faulty input in dataset"
        return shots

    def shot_accuracy(self):
        ''' Calculating hit rate of teams from shots find target and goals scored'''
        # Calling total_goals method to get team goals
        team_shots_on_goal = self.total_shots()
        # if total shots method is faulty then pass below part
        if isinstance(team_shots_on_goal,str):
            percentage = "can not calculated due to faulty input in dataset"
        else:
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
        ''' Counts total lineups for selected player'''
        game_ids = self.df.index.to_list()
        home_game_starts = [self.df["team1_startings"][game_id] for game_id in game_ids if self.player in self.df['team1_startings'][game_id]]
        home_game_starts = sum([i.count(self.player) for i in home_game_starts])
        away_game_starts = [self.df["team2_startings"][game_id] for game_id in game_ids if self.player in self.df['team2_startings'][game_id]]
        away_game_starts = sum([i.count(self.player) for i in away_game_starts])
        total_line_ups = home_game_starts + away_game_starts
        return total_line_ups

    def top_10_lineupers(self):
        ''' Returns dataframe of top 10 players that has most lineups'''
        game_ids = self.df.index.to_list()
        home_game_starts = [self.df["team1_startings"][game_id] for game_id in game_ids]
        away_game_starts = [self.df["team2_startings"][game_id] for game_id in game_ids]
        home_game_starts.extend(away_game_starts)
        d = defaultdict(int)
        for starts in home_game_starts:
            for i in starts:
                d[i] += 1
        d = sorted(d.items(), key=lambda item: item[1], reverse=True)[:10]
        df = pd.DataFrame(data=d)
        df = df.rename(columns={0: "player_name", 1: "line_ups"})
        return df