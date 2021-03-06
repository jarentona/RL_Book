import numpy as np
import matplotlib.pyplot as plt
from grid_world import standard_grid, negative_grid
import time

GAMMA = 0.9
ALPHA = 0.1
ALL_POSSIBLE_ACTIONS = ('R', 'U', 'D', 'L')
def print_values(V, g):
  time.sleep(1)
  for j in reversed(range(g.height)):

    print ("'---------------------------------------")
   
    for i in range(g.width):
      v = V.get((i,j), 0)
      if v >= 0:
          print( "| ",'{:06.2f}'.format(v), end=" ")  

      else:
         print( "| ",'{:06.2f}'.format(v), end=" ") 

    print( "| ")
  print ("'---------------------------------------")
  print ("")
  print ("")



def print_policy(P, g):
  time.sleep(2)
  for j in reversed(range(g.height)):
    print ("-----------------------------")
    for i in range(g.width):
      a = P.get((i,j), ' ')
      print( "| ",'{:3s}'.format(a),end=" ") 
    print( "| ")
  print ("-----------------------------")
  print ("")
  print ("")

def max_dict(d):
  max_key = None
  max_val = float('-inf')
  for k, v in d.items():
    if v > max_val:
      max_val = v
      max_key = k
  return max_key, max_val

def random_action(a, eps=0.1):
  p = np.random.random()
  if p < (1 - eps):
    return a
  else:
    return np.random.choice(ALL_POSSIBLE_ACTIONS)

if __name__ == '__main__':
    grid = standard_grid()
    print_values(grid.rewards, grid)
    Q = {}
    states = grid.all_states()
    for s in states:
        Q[s] = {}
        for a in ALL_POSSIBLE_ACTIONS:
            Q[s][a] = 0
    update_counts = {}
    update_counts_sa = {}
    for s in states:
        update_counts_sa[s] = {}
        for a in ALL_POSSIBLE_ACTIONS:
            update_counts_sa[s][a] = 1.0
    t = 1.0
    deltas = []
    for it in range(5000):
        if it % 100 == 0:
            t += 1e-2
        s = (3, 0) 
        grid.set_state(s)
        a = np.random.choice(ALL_POSSIBLE_ACTIONS)
        biggest_change = 0
        while not grid.game_over():
            r = grid.move(a)
            s2 = grid.current_state()
            a2 = max_dict(Q[s2])[0]
            a2 = random_action(a2, eps=1) 
            alpha = 0.1
            update_counts_sa[s][a] += 0.005
            old_qsa = Q[s][a]
            Q[s][a] = Q[s][a] + alpha*(r + GAMMA*Q[s2][a2] - Q[s][a])

            biggest_change = max(biggest_change, np.abs(old_qsa - Q[s][a]))
            update_counts[s] = update_counts.get(s,0) + 1
            s = s2
            a = a2
        deltas.append(biggest_change)

    plt.plot(deltas)
    plt.show()

    policy = {}
    V = {}
    for s in grid.actions.keys():
        a, max_q = max_dict(Q[s])
        policy[s] = a
        V[s] = max_q
    total =sum(update_counts.values())
    for k, v in update_counts.items():
        update_counts[k] = float(v) / total
    print ("values:")
    print_values(V, grid)
    print ("policy:")
    print_policy(policy, grid)

