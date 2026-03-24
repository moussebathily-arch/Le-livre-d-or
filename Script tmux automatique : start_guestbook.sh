#!/bin/bash

SESSION="guestbook"

# Crée une nouvelle session détachée
tmux new-session -d -s $SESSION -n editor

# Panneau 1 : Éditeur (Left)
tmux send-keys -t $SESSION "vim app.py" C-m

# Split vertical pour panneau serveur (Right)
tmux split-window -h -t $SESSION
tmux send-keys -t $SESSION:0.1 "python app.py" C-m

# Split horizontal pour panneau base de données (Bottom Right)
tmux split-window -v -t $SESSION:0.1
tmux send-keys -t $SESSION:0.2 "psql -U quiz_user -d quizdb" C-m

# Ajuster la taille des panneaux (optionnel)
tmux select-layout -t $SESSION tiled

# Rattacher à la session
tmux attach-session -t $SESSION
