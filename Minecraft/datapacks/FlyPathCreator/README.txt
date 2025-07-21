Datapack construtor de precurso para elytra.

Descrição:
> Quando acionado, rodeia o jogador com blocos de lanterna do mar, "sea_lantern", uma vez a cada 7.5 segundos (150 ticks).

Contexto:
> O jogador voa na direção que pretende construir a pista de voo.
> O datapack constroi automáticamente a pista de voo, para que outros jogadores a percorram com elytra.

Instruções de uso:
PRE-1: O jogador deve ter acesso a comandos (op)
INT-1: O jogador coloca a tag "fly" nele próprio para iniciar a construção do precurso
        -> /tag @s add fly
INT-2: O jogador voa pelo mapa para construir o percurso de voo
INT-3: O jogador remove a tag "fly" dele próprio para terminar a construção do precurso
        -> /tag @s remove fly


O que realmente acontece:
> 3 funções:
    -> load
    -> tick
    -> build
> Em load, é criado um objetivo de scoreboard para funcionar como relógio
> A cada tick, para cada jogador com a tag "fly":
    1- Soma 1 no contador (objetivo da scoreboard do jogador).
    2- Verifica que o contador >= 150, ou seja, se já se passaram 7.5 segundos:
        2.1- Se sim, executa a função "build".
    3- Verifica se o contador >= 150:
        3.1- Se sim, reinicia o contador.
> A função build é responsável por colocar os blocos de sea_lantern na posição correta.