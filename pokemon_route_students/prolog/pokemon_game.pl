:-ensure_loaded("pokemon_list.pl").
:-ensure_loaded("pokemon_info_attacks.pl").
:-ensure_loaded("pokemon_route.pl").

player_starts(0,0).

obtem_elemento(0,[H|_], H).

%funcao para obter obtem_elemento

obtem_elemento(N, [_|T], Elemento) :-
    N > 0,
    N1 is N - 1,
    obtem_elemento(N1, T, Elemento).

% get_pokemon_at(Matriz, X, Y, ParIdLevel)
get_pokemon_at(Matriz, X, Y, (Id, Level)) :-
    % 1. Extrair a Linha 'Y' da 'Matriz'
    obtem_elemento(Y, Matriz, LinhaAtual),

    % 2. Extrair a Coluna 'X' dessa 'LinhaAtual'
    obtem_elemento(X, LinhaAtual, (Id, Level)).

% get_vizinho(X, Y, X1, Y1)
    get_vizinho(X, Y, X, Y1) :- Y1 is Y - 1. % Cima
    get_vizinho(X, Y, X, Y1) :- Y1 is Y + 1. % Baixo
    get_vizinho(X, Y, X1, Y) :- X1 is X - 1. % Esquerda
    get_vizinho(X, Y, X1, Y) :- X1 is X + 1. % Direita

% vizinho_valido(Matriz, X, Y, SalaVizinha)
    vizinho_valido(Matriz, X, Y, [Id, Name, Level, X_Vizinho, Y_Vizinho, Types]) :-
        % 1. Calcular as coordenadas (X_Vizinho, Y_Vizinho) a partir de (X, Y)
        get_vizinho(X, Y, X_Vizinho, Y_Vizinho),

        % 2. Ir à Matriz ver que Pokémon está nessas novas coordenadas (usando a regra do Mini-passo 1)
        get_pokemon_at(Matriz, X_Vizinho, Y_Vizinho, (Id, Level)),

        % 3. Consultar a base de dados para obter o Name e os Types correspondentes a esse Id
        pokemon(Id, Name, Types).

% next_rooms(X, Y, Rooms)
    next_rooms(X, Y, Rooms) :-
        % 1. Vai buscar a matriz do mapa que está guardada no facto route/1
        route(M),

        % 2. Encontra todos os vizinhos válidos e guarda-os na lista Rooms
        findall(SalaVizinha, vizinho_valido(M, X, Y, SalaVizinha), Rooms).