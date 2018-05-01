### Best Ball Simulator
This is a simulator which will help you gauge your chance to win your MFL10 leage, based on your roster.  It can also help you explore roster construction concepts and determine under what coniditions various roster constructions are optimal.  In order to simulate a best ball team, you enter five parameters for each player which relate to your projection for that player's upcoming performance.  These are:

**Average Non-Touchdown Points**: This is the average number of points per week that you expect your player to score which are *not* from touchdowns.  If you want to use the player's previous year as your projection for this year, take their last year's total points, subtract 6*(last year's TD's), then divide by 16.

**Standard Deviation**: Specifically, this is the standard deviation of the above number, the non-TD points per week.

**Average TD's**:The average amount of TD's your player will score per week.  For example, for a player who scored 8 TD's last year, 8/16, or .5, is a good projection.  This number does *not* need to be an integer (and, in fact, probably shouldn't be).

**Preseason Bust Rate**:
A percentage value, which indicates your approximated chance that the player will bust before the season even starts.  This parameter approximates things like a torn ACL in the preseason, getting buried on the depth chart, hitting your kid, etc.  For early drafted players, this is usually very low, whereas for lotto tickets you draft late, this parameter should be higher.

**Weekly Bust Rate**:
Encompsses the chance of your player suffering a season ending injuy in any given week, and giving you zero points per week after that (or busts for another, less common reason).  You can project this however you want, but in general, your weekly bust rates should be highest for TE's, and should then follow the order of: TE > RB > WR > QB, based on historical data about each position.

### How it works
Before the season starts, each player is given a bye, and then a sample is drawn from a uniform distribution to determine whether or not the player busts before the start of the season (based on their preseason bust rate).

During the season, each week, the first thing that happens is we draw from a uniform distribution to determine whether the player busts (based on the weekly bust rate).  Next, each player's score is calculated from the parameters given.  If the player is on bye, or has busted, the player's weekly score is 0.  Otherwise, we draw from a normal distribution centered at the Non-TD points value given with the standard devaition that was given.  We then sample from a Poisson distribution with a lambda value of the Avg TD's given, multiplied by 6 (or 4, for quarterbacks), and add that number to the sample from the normal distribution.  This gives us the total weekly score (non TD points + points from TD's) for the player.  After generating a score for each player in this manner, the program selects the optimal lineup based on MFL10 rules, and thus produces the team's score for the week.

Over the course of the season, the program sums the weekly scores, leading to a final season score, usually between 1700-2600, for the team.  It does this a total of 5,000 times, simulating 5,000 seasons, then gives you an average score, and the chance that your score will be over 2400, or over 2500.  Specifically, the 2400 number is significant, as that is the average amount of points needed to win an MFL10.
