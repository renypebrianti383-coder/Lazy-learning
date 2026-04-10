import numpy as np
import os
var = 1
gamma = 0.98
rho = 2.4
memoryaksi = []
memorystate = []
memoryreward = []
memoryaksi1 = []
memorystate1 = []
memoryreward1 = []
def RBF(A, B, var, rho):
  dist = np.linalg.norm(A - B)
  bobot = np.exp(-dist ** 2 / (2 * rho ** 2))
  return var * bobot
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()
def get_action(board, available_moves, memoryaksi, memorystate, memoryreward, player):
    if not memorystate:
        return np.random.choice(available_moves), 0
    scores = []
    co = []
    for move in available_moves:
          expectedval, confident = predict(board, move, memoryaksi, memorystate, memoryreward, player)
          expectedval *= (1 - (1-confident) * 0.1)
          scores.append(expectedval)
          co.append(confident)
    best = available_moves[np.argmax(scores)] if np.random.uniform() < co[np.argmax(co)] else np.random.choice(available_moves)
    return best, co[np.argmax(co)]
def predict(board, move, memoryaksi, memorystate, memoryreward, player):
  sim = board.copy()
  sim[move] = 1 if player == 1 else -1
  relevantdata = [valu for valu, aksi in zip(memorystate, memoryaksi) if aksi == move]
  relevant_rewards = [r for r, a in zip(memoryreward, memoryaksi) if a == move]
  if len(relevant_rewards) == 0 or len(relevantdata) == 0:
        return 0, 0
  weight = []
  for i in range(len(relevantdata)):
    weight.append(RBF(relevantdata[i], np.array(sim), var, rho))
  P = softmax(weight)
  return np.dot(P, relevant_rewards), (np.max(weight) / var)
def learn(state, action, reward, memoryaksi, memorystate, memoryreward):
  memorystate.append(state)
  memoryaksi.append(action)
  memoryreward.append(reward)
  return
def display(board, debug1 = None, debug2 = None, stat=None, stat1=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n      TIC-TAC-TOE AI")
    print("    -----------------")
    sym = {1: 'O', -1: 'X', 0: ' '}
    for i in range(3):
        print(f"      {sym[board[i][0]]} | {sym[board[i][1]]} | {sym[board[i][2]]}")
        if i < 2:
            print("      ---------")
    print("\n")
    print(debug1)
    print(debug2)
    print(stat)
    print(stat1)
board = [[0, 0, 0] for i in range(3)]
discountedreward = []
discountedreward1 = []
moves = []
moves1 = []
disre = []
disre1 = []
step = 0
matc = 0
con = 0
con1 = 0
def validate(board):
    condition0 = False
    condition1 = False
    total = 0
    prevhor = 0
    for i in range(3):
        for j in range(3):
           total += board[i][j]
        if total == 3:
            condition0 = True
        if total == -3:
            condition1 = True
        total = 0
    for i in range(3):
        for j in range(3):
            total += board[j][i]
        if total == 3:
            condition0 = True
        if total == -3:
            condition1 = True
        total = 0
    for i in range(3):
        total += board[i][i]
    if total == 3:
        condition0 = True
    elif total == -3:
        condition1 = True
    total = 0
    for i in reversed(range(3)):
        total += board[i][2 - i]
    if total == 3:
        condition0 = True
    elif total == -3:
        condition1 = True
    total = 0
    return condition0, condition1
confi = 0
step1 = 0
win1 = 0
win = 0
seri = 0
turn = np.random.choice([-1, 1])
while True:
  try:
    if (matc) % 100 == 0 and (matc) > 0:
        board = [[0, 0, 0] for i in range(3)]
        turn1 = np.random.choice([-1, 1])
        game = False
        while not game:
            try:
                condition0, condition1 = validate(board)
                seri = True
                for i in range(len(board)):
                    for j in range(len(board[i])):
                        if board[i][j] == 0:
                            seri = False
                if seri and not condition1 and not condition0:
                    display(board, debug1=con)
                    for i in reversed(range(step)):
                        disre.append((gamma ** i) * 0)
                    for i in reversed(range(step1)):
                        disre1.append((gamma ** i) * 0)
                    for i in range(step):
                        learn(discountedreward[i], moves[i], disre[i], memoryaksi, memorystate, memoryreward)
                    for i in range(step1):
                        learn(discountedreward1[i], moves1[i], disre1[i], memoryaksi1, memorystate1, memoryreward1)
                    board = [[0, 0, 0] for i in range(3)]
                    step = 0
                    step1 = 0
                    discountedreward = []
                    discountedreward1 = []
                    moves = []
                    moves1 = []
                    disre = []
                    disre1 = []
                    print("seri")
                    input("Enter untuk lanjut...")
                    turn1 = np.random.choice([-1, 1])
                    continue
                if turn1 == -1:
                    display(board, debug1=con)
                    y = int(input("masukan y"))
                    x = int(input("masukan x"))
                    if board[y][x] != 0:
                        continue
                    board[y][x] = -1
                    condition0, condition1 = validate(board)
                    if condition1:
                        display(board, debug1=con, debug2=con1, stat=win, stat1=win1)
                        for i in reversed(range(step)):
                            disre.append(((gamma ** i) * (-100 + step * 5)))
                        for i in range(step):
                            learn(discountedreward[i], moves[i], disre[i], memoryaksi, memorystate, memoryreward)
                        board = [[0, 0, 0] for i in range(3)]
                        step = 0
                        discountedreward = []
                        moves = []
                        disre = []
                        board = [[0, 0, 0] for i in range(3)]
                        print("kamu mwnang")
                        input("Enter untuk lanjut...")
                        turn1 = np.random.choice([-1, 1])
                        continue
                    turn1 = 1
                    continue
                if turn1 == 1:
                    display(board, debug1=con)
                    board_flat = [board[i][j] for i in range(3) for j in range(3)]
                    bot_layer = [1 if x == 1 else 0 for x in board_flat]
                    user_layer = [1 if x == -1 else 0 for x in board_flat]
                    databoard = board_flat.copy()
                    avaible = [i for i, st in enumerate(board_flat) if st == 0]
                    if len(avaible) == 0:
                        display(board, debug1=con, debug2=con1, stat=win, stat1=win1)
                        for i in reversed(range(step)):
                            disre.append((gamma ** i) * 0)
                        for i in range(step):
                            learn(discountedreward[i], moves[i], disre[i], memoryaksi, memorystate, memoryreward)
                        board = [[0, 0, 0] for i in range(3)]
                        step = 0
                        discountedreward = []
                        moves = []
                        disre = []
                        input("Enter untuk lanjut...")
                        turn = np.random.choice([-1, 1])
                        continue
                    move, con = get_action(databoard, avaible, memoryaksi, memorystate, memoryreward, player=1) 
                    y = move // 3
                    x = move % 3
                    board[y][x] = 1
                    discountedreward.append(databoard)
                    moves.append(move)
                    step += 1
                    condition0, condition1 = validate(board)
                    if condition0:
                        display(board, debug1=con)
                        for i in reversed(range(step)):
                            disre.append(((gamma ** i) * (100 - step * 5)))
                        for i in range(step):
                            learn(discountedreward[i], moves[i], disre[i], memoryaksi, memorystate, memoryreward)
                        board = [[0, 0, 0] for i in range(3)]
                        step = 0
                        discountedreward = []
                        moves = []
                        disre = []
                        board = [[0, 0, 0] for i in range(3)]
                        print("bot 1 menang")
                        input("Enter untuk lanjut...")
                        turn1 = np.random.choice([-1, 1])
                        continue
                    turn1 = -1
                    continue
            except KeyboardInterrupt:
                game = True
                matc += 1
                break
            except ValueError:
                continue
            except IndexError:
                continue
    display(board, debug1=con, debug2=con1, stat=win, stat1=win1)
    condition0, condition1 = validate(board)
    seri = True
    for i in range(len(board)):
       for j in range(len(board[i])):
          if board[i][j] == 0:
            seri = False
    if seri and not condition0 and not condition1:
       display(board, debug1=con, debug2=con1, stat=win, stat1=win1)
       for i in reversed(range(step)):
          disre.append((gamma ** i) * 0)
       for i in reversed(range(step1)):
          disre1.append((gamma ** i) * 0)
       for i in range(step):
          learn(discountedreward[i], moves[i], disre[i], memoryaksi, memorystate, memoryreward)
       for i in range(step1):
          learn(discountedreward1[i], moves1[i], disre1[i], memoryaksi1, memorystate1, memoryreward1)
       board = [[0, 0, 0] for i in range(3)]
       step = 0
       step1 = 0
       discountedreward = []
       discountedreward1 = []
       moves = []
       moves1 = []
       disre = []
       disre1 = []
       seri += 1
    #    print("seri")
    #    input("Enter untuk lanjut...")
       turn = np.random.choice([-1, 1])
       continue

    if turn == -1:
        display(board, debug1=con, debug2=con1, stat=win, stat1=win1)
        board_flat = [board[i][j] for i in range(3) for j in range(3)]
        databoard = board_flat.copy()
        avaible = [i for i, st in enumerate(board_flat) if st == 0]
        if len(avaible) == 0:
            display(board, debug1=con, debug2=con1, stat=win, stat1=win1)
            for i in reversed(range(step)):
                disre.append((gamma ** i) * 0)
            for i in reversed(range(step1)):
                disre1.append((gamma ** i) * 0)
            for i in range(step):
                learn(discountedreward[i], moves[i], disre[i], memoryaksi, memorystate, memoryreward)
            for i in range(step1):
                learn(discountedreward1[i], moves1[i], disre1[i], memoryaksi1, memorystate1, memoryreward1)
            board = [[0, 0, 0] for i in range(3)]
            step = 0
            step1 = 0
            discountedreward = []
            discountedreward1 = []
            moves = []
            moves1 = []
            disre = []
            disre1 = []
            seri += 1
            # print("seri")
            # input("Enter untuk lanjut...")
            turn = np.random.choice([-1, 1])
            continue
        move, con1 = get_action(databoard, avaible, memoryaksi1, memorystate1, memoryreward1, player=-1) 
        y = move // 3
        x = move % 3
        board[y][x] = -1
        discountedreward1.append(databoard)
        moves1.append(move)
        step1 += 1
        condition0, condition1 = validate(board)
        if condition1:
            display(board, debug1=con, debug2=con1, stat=win, stat1=win1)
            for i in reversed(range(step)):
                disre.append(((gamma ** i) * (-100 + step * 5)))
            for i in reversed(range(step1)):
                disre1.append(((gamma ** i) * (100 - step1 * 5)))
            for i in range(step):
                learn(discountedreward[i], moves[i], disre[i], memoryaksi, memorystate, memoryreward)
            for i in range(step1):
                learn(discountedreward1[i], moves1[i], disre1[i], memoryaksi1, memorystate1, memoryreward1)
            board = [[0, 0, 0] for i in range(3)]
            step = 0
            step1 = 0
            discountedreward = []
            discountedreward1 = []
            moves = []
            moves1 = []
            disre = []
            disre1 = []
            board = [[0, 0, 0] for i in range(3)]
            # print("bot 2 menang")
            win1 += 1
            matc += 1
            # input("Enter untuk lanjut...")
            turn = np.random.choice([-1, 1])
            continue
        # input("Enter untuk lanjut...")
        turn = 1
        continue

    if turn == 1:
        display(board, debug1=con, debug2=con1, stat=win, stat1=win1)
        board_flat = [board[i][j] for i in range(3) for j in range(3)]
        bot_layer = [1 if x == 1 else 0 for x in board_flat]
        user_layer = [1 if x == -1 else 0 for x in board_flat]
        databoard = board_flat.copy()
        avaible = [i for i, st in enumerate(board_flat) if st == 0]
        if len(avaible) == 0:
            display(board, debug1=con, debug2=con1, stat=win, stat1=win1)
            for i in reversed(range(step)):
                disre.append((gamma ** i) * 0)
            for i in reversed(range(step1)):
                disre1.append((gamma ** i) * 0)
            for i in range(step):
                learn(discountedreward[i], moves[i], disre[i], memoryaksi, memorystate, memoryreward)
            for i in range(step1):
                learn(discountedreward1[i], moves1[i], disre1[i], memoryaksi1, memorystate1, memoryreward1)
            board = [[0, 0, 0] for i in range(3)]
            step = 0
            step1 = 0
            discountedreward = []
            discountedreward1 = []
            moves = []
            moves1 = []
            disre = []
            disre1 = []
            seri += 1
            # input("Enter untuk lanjut...")
            turn = np.random.choice([-1, 1])
            continue
        move, con = get_action(databoard, avaible, memoryaksi, memorystate, memoryreward, player=1) 
        y = move // 3
        x = move % 3
        board[y][x] = 1
        discountedreward.append(databoard)
        moves.append(move)
        step += 1
        condition0, condition1 = validate(board)
        if condition0:
            display(board, debug1=con, debug2=con1, stat=win, stat1=win1)
            for i in reversed(range(step)):
                disre.append(((gamma ** i) * (100 - step * 5)))
            for i in reversed(range(step1)):
                disre1.append(((gamma ** i) * (-100 + step1 * 5)))
            for i in range(step):
                learn(discountedreward[i], moves[i], disre[i], memoryaksi, memorystate, memoryreward)
            for i in range(step1):
                learn(discountedreward1[i], moves1[i], disre1[i], memoryaksi1, memorystate1, memoryreward1)
            board = [[0, 0, 0] for i in range(3)]
            step = 0
            step1 = 0
            discountedreward = []
            discountedreward1 = []
            moves = []
            moves1 = []
            disre = []
            disre1 = []
            board = [[0, 0, 0] for i in range(3)]
            # print("bot 1 menang")
            win += 1
            matc += 1
            # input("Enter untuk lanjut...")
            turn = np.random.choice([-1, 1])
            continue
        # input("Enter untuk lanjut...")
        turn = -1
        continue
  except KeyboardInterrupt:
    break
  except ValueError:
    continue
  except IndexError:
    continue
