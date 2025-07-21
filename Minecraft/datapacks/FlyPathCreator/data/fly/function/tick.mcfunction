execute as @a[tag=fly] run scoreboard players add @s clock 1
execute as @a[tag=fly] if score @s clock matches 150.. anchored eyes facing entity @s eyes run function fly:build
execute as @a[tag=fly] if score @s clock matches 150.. run scoreboard players set @s clock 0