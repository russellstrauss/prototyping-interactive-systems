import participant

sessionnum = str(input('Enter session num: '))
trialnum = str(input('Enter trial num: '))
newp = participant.generate_participant(sessionnum,trialnum)
print(newp)