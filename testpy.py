
questions={'Is the weather good out there','Is this sufficient ','hey is this useful?'}
quest_dict=dict(enumerate((question for question in questions),start=1))
for i,v in quest_dict.items():
    print(i,v)
