from tkinter import *
import numpy
import random

root = Tk();

#default values
DEFAULTS = dict();
#[mean, std, avg td's, preseason bust, weekly bust]
DEFAULTS["QB"] = [10, 4, 1.7, 10, 1.5];
DEFAULTS["RB"] = [10, 6, .5, 30, 3];
DEFAULTS["WR"] = [10, 8, .4, 15, 2.2];
DEFAULTS["TE"] = [6.8, 10, .3, 30, 5];
DEFAULTS["DEF"]= [7, 5, .22, 0, 0];

NUM_SEASONS = 5000;

class PositionGroup:
    def __init__(self, root, frameTitle, posAbrev):
        self.frame = Frame(root);
        self.frame.pack();

        # create header with [Title][+][-]
        self.headerFrame = Frame(self.frame);
        self.headerFrame.grid(row=0, columnspan=5);
        self.frameLabel = Label(self.headerFrame, text=frameTitle)
        self.frameLabel.grid(row=0, column=0);
        self.addButton = Button(self.headerFrame, text="+", command= lambda:(self.addPlayer()));
        self.addButton.grid(row=0, column=1);
        self.subButton = Button(self.headerFrame, text="-", command= lambda:(self.removePlayer()));
        self.subButton.grid(row=0, column=2);

        self.i = 0;
        self.playerRows=list();
        self.posAbrev=posAbrev;
        #print("posabrev:%s"%(posAbrev))
        self.addPlayer();

    def addPlayer(self):
        self.i+=1;
        D = DEFAULTS[self.posAbrev];
        self.playerRows.append(PlayerRow(self.frame, self.posAbrev, self.i, \
        D[0], D[1], D[2], D[3], D[4]));

    def removePlayer(self):
        lastRow = self.playerRows[len(self.playerRows)-1];
        self.playerRows.remove(lastRow);
        lastRow.removePlayer();

    def getPlayers(self):
        playerList = list();
        for playerRow in self.playerRows:
            params = playerRow.parameters;
            d = dict();
            for key in params.keys():
                d[key] = float(params[key].get());
            playerList.append(Player(self.posAbrev, playerRow.index, d["avg"],\
             d["std"], d["avg_td"],\
              d["pre_bust"], d["w_bust"]));
        return playerList;


class PlayerRow:
    def __init__(self, root, pos, index, AVG, STD, AVG_TD, PRE_BUST, W_BUST):
        self.index = index;
        self.frame = Frame(root);
        self.frame.grid(row=index);

        self.rowName = Label(self.frame, text="%s" % (pos));
        self.rowName.grid(rowspan=2, column=0);

        # parameters for each player
        # [key, default value, label text]
        self.parameters=dict();
        PARAMS = [("avg", AVG, "Avg (Non-TD):"),\
        ("std", STD, "Std:"),\
        ("avg_td", AVG_TD, "Avg TD's:"),\
        ("pre_bust", PRE_BUST, "Preseason Bust %:"),\
        ("w_bust", W_BUST, "Weekly Bust %:")];

        # add the 5 parameters onto the display
        i=1;
        for param in PARAMS:
            self.parameters[param[0]] = self.addParameter(self.frame, param[1], param[2], i);
            i+=1;

    def removePlayer(self):
        self.frame.grid_forget();

    # set up the label and text box for a parameter
    def addParameter(self, frame, default_value, labelText, index):
        label = Label(frame, text=labelText);
        label.grid(row=1, column=2*index);
        entry = Entry(frame);
        entry.insert(0, default_value);
        entry.grid(row=1, column=2*index+1);
        return entry;

class Player:
    def __init__(self, pos, index, avg, std, avg_td, pre_bust, w_bust):
        self.name = "pos%d"%(index);
        self.avg = avg;
        self.std = std;
        self.avg_td=avg_td;
        self.pre_bust=pre_bust;
        self.w_bust=w_bust;
        self.busted = False;
        self.pos=pos;
        self.bye = 0;

    def initializePlayer(self, weeks):
        #print("in init");
        if (numpy.random.rand() < self.pre_bust/100.0):
            #print("busted");
            self.busted=True;
        self.bye = random.randint(5, weeks-3);

    def simulateGame(self, week):
        #print("busted:%d"%(self.busted));
        if(self.busted or week == self.bye):
            return 0;
        if(numpy.random.rand() < self.w_bust/100.0):
            self.busted=True;
            return 0;
        non_td_pts = numpy.random.normal(self.avg, self.std);
        tds = numpy.random.poisson(self.avg_td);
        m=6;
        if self.pos == "QB":
            m=4;
        #print(tds);
        #print(m);
        #print(self.pos);
        return round(max(0, non_td_pts+m*tds),2);

    def __str__(self):
        s = "avg: %f std: %f avg_td: %f pre_bust: %f w_bust: %f\n" \
        %(self.avg, self.std, self.avg_td, self.pre_bust, self.w_bust);
        return s;

    def __repr__(self):
        return self.__str__();

class Season:
    def __init__(self, weeks, posGroupDict):
        self.playerDict = dict();
        for pos in posGroupDict.keys():
            self.playerDict[pos] = posGroupDict[pos].getPlayers();
        self.weeks = weeks;
        self.score = 0;

    def simulateWeek(self, week):
        scores = dict();
        for pos in self.playerDict.keys():
            scores[pos] = list();
            for player in self.playerDict[pos]:
                scores[pos].append(player.simulateGame(week));

        weeklyLineup = dict();
        for pos in scores.keys():
            starters = 1;
            if pos == "RB":
                starters = 2;
            if pos == "WR":
                starters = 3;
            weeklyLineup[pos] = list();
            for i in range(0, starters):
                topScoreLeft = max(scores[pos]);
                weeklyLineup[pos].append(topScoreLeft);
                scores[pos].remove(topScoreLeft);
        weeklyLineup["FLEX"] = list();
        weeklyLineup["FLEX"].append(max([max(scores["RB"]), max(scores["WR"]), max(scores["TE"])]));

        weekScore = 0;
        for pos in weeklyLineup.keys():
            for score in weeklyLineup[pos]:
                weekScore+=score;
        return (weeklyLineup, weekScore);

    def initializeSeason(self):
        for pos in self.playerDict.keys():
            #playerList = d[pos].getPlayers();
            for player in self.playerDict[pos]:
                player.initializePlayer(self.weeks);

    def simulateSeason(self):
        totalScore = 0;
        self.initializeSeason();
        for week in range(1, self.weeks+1):
            (lineup, score) = self.simulateWeek(week);
            #print(lineup);
            #print(score);
            #print("---");
            totalScore+=score;
        self.score = totalScore;
        for pos in self.playerDict:
            for player in self.playerDict[pos]:
                player.busted = False;

positions = [("Quarterbacks", "QB"),\
 ("Running Backs", "RB"),\
 ("Wide Receivers", "WR"),\
 ("Tight Ends", "TE"),\
 ("Defenses", "DEF")];

d = dict();
for pos1 in positions:
    d[pos1[1]] = PositionGroup(root, pos1[0], pos1[1]);

def runSeason():
    s = Season(16, d);
    #print(s.playerDict);
    superScore = 0;
    over2500 = 0;
    over2400 = 0;
    for i in range(0, NUM_SEASONS):
        s.simulateSeason();
        superScore+=s.score;
        if s.score > 2400:
            over2400+=1;
        if s.score > 2500:
            over2500+=1;
    print("Avg Score: %f"%(superScore/NUM_SEASONS));
    print("Over 2400: %.2f"%(over2400/NUM_SEASONS));
    print("Over 2500: %.2f"%(over2500/NUM_SEASONS));

seasons = "Seasons";
if NUM_SEASONS == 1:
    seasons = "Season";
runSeason = Button(root, text="Simulate %d %s"%(NUM_SEASONS, seasons), command=runSeason);
runSeason.pack();

d["QB"].addPlayer();
d["WR"].addPlayer();
d["WR"].addPlayer();
d["WR"].addPlayer();
d["WR"].addPlayer();
d["WR"].addPlayer();
d["WR"].addPlayer();
d["WR"].addPlayer();
d["WR"].addPlayer();
#d["WR"].addPlayer();
#d["RB"].addPlayer();
d["RB"].addPlayer();
d["RB"].addPlayer();
d["RB"].addPlayer();
d["RB"].addPlayer();
d["TE"].addPlayer();
#d["TE"].addPlayer();
d["DEF"].addPlayer();

print(d["QB"].playerRows[0].parameters["avg"].get());


#print("Season Score: %f"%(totalScore));




#print(scores);
playerList = d["WR"].getPlayers();
#for i in range(0, 16):
    #print("WR1: %f"%(playerList[0].simulateWeek()));

root.mainloop();
