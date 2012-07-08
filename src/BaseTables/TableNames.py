prefix = "pycube2master_"

table_names = {}

table_names['ActivitySpan']         = 'activity_spans'
table_names['CaptureEvent']         = 'capture_events'
table_names['DamageDealtEvent']     = 'damage_dealt_events'
table_names['DeathEvent']           = 'death_events'
table_names['FragEvent']            = 'frag_events'
table_names['Game']                 = 'games'
table_names['GameVersion']          = 'game_versions'
table_names['Gun']                  = 'guns'
table_names['Match']                = 'matches'
table_names['Mode']                 = 'modes'
table_names['PseudoMode']           = 'pseudo_modes'
table_names['PunitiveEffect']       = 'punitive_effects'
table_names['PunitiveEffectType']   = 'punitive_effect_types'
table_names['ServerDomain']         = 'server_domains'
table_names['ServerInstance']       = 'server_instances'
table_names['ServerMod']            = 'server_mods'
table_names['ShotEvent']            = 'shot_events'
table_names['User']                 = 'users'
table_names['UserGroup']            = 'user_groups'
table_names['UserGroupMembership']  = 'user_group_memberships'
table_names['UserName']             = 'user_names'

for key in table_names.keys():
    table_names[key] = prefix + table_names[key]

