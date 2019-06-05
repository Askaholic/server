insert into account (id, display_name, password) values
    (50,  'player_service', password('player_service')),
    (100, 'ladder1', password('ladder1')),
    (101, 'ladder2', password('ladder2')),
    (102, 'ladder_ban', password('ladder_ban')),
    (200, 'banme', password('banme'))
;

delete from clan_membership where member_id = 50;
insert into clan_membership (clan_id, member_id) values
    (1, 50);

insert into leaderboard_rating (account_id, mean, deviation, total_games, won_games, leaderboard_id)
    values
    -- Golbal rating
    (50,  1200, 250, 42, 42, 1),
    (100, 1500, 500, 0, 0, 1),
    (101, 1500, 500, 0, 0, 1),
    (102, 1500, 500, 0, 0, 1),
    -- Ladder rating
    (50,  1300, 400, 12, 6, 1),
    (100, 1500, 500, 0, 0, 1),
    (101, 1500, 500, 0, 0, 1),
    (102, 1500, 500, 0, 0, 1)
;

insert into avatar (id, url, description) values
    (1, 'http://content.faforever.com/faf/avatars/qai2.png', 'QAI'),
    (2, 'http://content.faforever.com/faf/avatars/UEF.png', 'UEF')
;

insert into avatar_assignment (account_id, avatar_id, selected) values
    (50, 2, 't');

-- delete from matchmaker_ban where id = 102 and userid = 102;
-- insert into matchmaker_ban (id, userid) values (102, 102);

delete from ban where account_id = 200;

insert into game(id, start_time, victory_condition, featured_mod_id, host_id, map_version_id, name, validity) values
    (41935, NOW(), 'DEMORALIZATION', 2, 1, 1, 'MapRepetition', 'VALID'),
    (41936, NOW() + interval '1 minute', 'DEMORALIZATION', 2, 1, 2, 'MapRepetition', 'VALID'),
    (41937, NOW() + interval '2 minute', 'DEMORALIZATION', 2, 1, 3, 'MapRepetition', 'VALID'),
    (41938, NOW() + interval '3 minute', 'DEMORALIZATION', 2, 1, 4, 'MapRepetition', 'VALID'),
    (41939, NOW() + interval '4 minute', 'DEMORALIZATION', 2, 1, 5, 'MapRepetition', 'VALID'),
    (41940, NOW() + interval '5 minute', 'DEMORALIZATION', 2, 1, 6, 'MapRepetition', 'VALID'),
    (41941, NOW() + interval '6 minute', 'DEMORALIZATION', 2, 1, 7, 'MapRepetition', 'VALID');

insert into game_participant (game_id, participant_id, faction, color, team, start_spot, score, finish_time) values
    (1, 1, 0, 0, 2, 0, 10, NOW()),
    (41935, 1, 0, 0, 2, 0, 10, NOW()),
    (41936, 1, 0, 0, 2, 0, 10, NOW() + interval '1 minute'),
    (41937, 1, 0, 0, 2, 0, 10, NOW() + interval '2 minute'),
    (41938, 1, 0, 0, 2, 0, 10, NOW() + interval '3 minute'),
    (41939, 1, 0, 0, 2, 0, 10, NOW() + interval '4 minute'),
    (41940, 1, 0, 0, 2, 0, 10, NOW() + interval '5 minute'),
    (41941, 1, 0, 0, 2, 0, 10, NOW() + interval '6 minute');

delete from social_relation where from_id = 1 and to_id = 2;
insert into social_relation (from_id, to_id, relation) values
    (2, 1, 'FRIEND');
