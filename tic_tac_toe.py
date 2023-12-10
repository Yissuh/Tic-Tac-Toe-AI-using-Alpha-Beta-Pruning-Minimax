import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMessageBox, QComboBox, QLabel

class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
    
        self.current_player = "Player 1"
        self.game_board = [["" for _ in range(3)] for _ in range(3)]
        self.game_mode = "Against Computer"
        self.highlighted_button = None


        # Initialize scoreboard variables
        self.player_1_wins = 0
        self.player_2_wins = 0
        self.draws = 0

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Tic Tac Toe')

        layout = QGridLayout()

        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = QPushButton('', self)
                button.setStyleSheet("font-size: 30px;")
                button.clicked.connect(lambda _, row=i, col=j: self.on_click(row, col))
                layout.addWidget(button, i, j)
                row.append(button)
            self.buttons.append(row)

        self.setLayout(layout)


        # Adding a ComboBox for selecting game mode
        self.game_mode_combo = QComboBox(self)
        self.game_mode_combo.addItem("Against Computer")
        self.game_mode_combo.addItem("Two Players")
        self.game_mode_combo.currentIndexChanged.connect(self.select_game_mode)
        layout.addWidget(self.game_mode_combo, 3, 0, 1, 3)

        # Label to display current player's turn
        self.turn_label = QLabel(f"Current Turn: {self.current_player}", self)
        layout.addWidget(self.turn_label, 4, 0, 1, 3)

        # Start Game button
        self.start_game_button = QPushButton("Computer First Turn", self)
        self.start_game_button.clicked.connect(self.computer_first_turn)
        layout.addWidget(self.start_game_button, 5, 0, 1, 3)

        # Reset Game button
        self.reset_button = QPushButton("Reset Game", self)
        self.reset_button.clicked.connect(self.reset_game)
        layout.addWidget(self.reset_button, 6, 0, 1, 3)

        self.best_move_button = QPushButton("Best Move", self)
        self.best_move_button.clicked.connect(self.highlight_best_move)
        layout.addWidget(self.best_move_button, 7, 0, 1, 3)  

        self.setFixedSize(self.sizeHint())
        self.show()

        # Scoreboard labels
        self.scoreboard_label = QLabel(self)
        layout.addWidget(self.scoreboard_label, 8, 0, 1, 3)
        self.update_scoreboard_label()

    def highlight_best_move(self):
            if self.game_mode == "Against Computer" and self.current_player == "Player 1":
                _, best_move = self.minimax(0, float('-inf'), float('inf'), False)  # Calculate best move for 'X'
                if best_move:
                    row, col = best_move
                    button = self.buttons[row][col]
                    if self.highlighted_button:  # Clear previously highlighted button
                        self.highlighted_button.setStyleSheet("font-size: 30px;")
                    button.setStyleSheet("background-color: yellow; font-size: 30px;")
                    self.highlighted_button = button  # Update the highlighted button

    def select_game_mode(self):
        previous_game_mode = self.game_mode
        self.game_mode = self.game_mode_combo.currentText()
        if previous_game_mode != self.game_mode:
            self.reset_scoreboard()
            self.reset_game()

        if self.game_mode == "Two Players":
            self.start_game_button.setEnabled(False)

    def reset_scoreboard(self):
        self.player_1_wins = 0
        self.player_2_wins = 0
        self.draws = 0
        self.update_scoreboard_label()

    def computer_first_turn(self):
        if self.game_mode == "Against Computer" and self.current_player == "Player 1":
            self.current_player = "Player 2"  # Update the current player
            self.turn_label.setText(f"Current Turn: {self.current_player}")  # Update the UI
            self.computer_move()

        self.start_game_button.setEnabled(False)


    def check_winner(self):
        for i in range(3):
            if self.game_board[i][0] == self.game_board[i][1] == self.game_board[i][2] != "":
                return self.game_board[i][0]
            if self.game_board[0][i] == self.game_board[1][i] == self.game_board[2][i] != "":
                return self.game_board[0][i]
        if self.game_board[0][0] == self.game_board[1][1] == self.game_board[2][2] != "":
            return self.game_board[0][0]
        if self.game_board[0][2] == self.game_board[1][1] == self.game_board[2][0] != "":
            return self.game_board[0][2]
        return None
    
    def update_scoreboard_label(self):
        # Update the scoreboard text
        scoreboard_text = ""
        if self.game_mode == "Against Computer":
            scoreboard_text = f"Player Wins: {self.player_1_wins} | Computer Wins: {self.player_2_wins} | Draws: {self.draws}"
        else:
            scoreboard_text = f"X Player Wins: {self.player_1_wins} | O Player Wins: {self.player_2_wins} | Draws: {self.draws}"
        self.scoreboard_label.setText(scoreboard_text)

    def on_click(self, row, col):
        if self.game_board[row][col] == "" and not self.check_winner():
            self.game_board[row][col] = "X" if self.current_player == "Player 1" else "O"
            button = self.buttons[row][col]

        # Set text and color based on the symbol
            symbol = self.game_board[row][col]
            button.setText(symbol)
            if symbol == "O":
                button.setStyleSheet("color: red; font-size: 30px;")
            else:
                button.setStyleSheet("color: black; font-size: 30px;")
            winner = self.check_winner()
            if winner:
                if winner == "O" and self.game_mode == "Against Computer":
                    winner_message = "Computer Wins"
                    self.player_2_wins += 1
                else:
                    if winner == "X":
                        winner_message = "Player 1 Wins"
                        self.player_1_wins += 1
                    else:
                        winner_message = "Player 2 Wins"
                        self.player_2_wins += 1
                self.update_scoreboard_label()
                QMessageBox.information(self, "Tic Tac Toe", f"{winner_message}!")
                self.reset_game()
            elif all(all(cell != "" for cell in row) for row in self.game_board):
                QMessageBox.information(self, "Tic Tac Toe", "It's a tie!")
                self.draws += 1
                self.update_scoreboard_label()
                self.reset_game()
            else:
                self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"
                self.turn_label.setText(f"Current Turn: {self.current_player}")
                if self.game_mode == "Against Computer" and self.current_player == "Player 2":
                    self.start_game_button.setEnabled(False)
                    self.computer_move()

                if self.highlighted_button:  # Clear highlighted button on a new move
                    self.highlighted_button.setStyleSheet("font-size: 30px;")
                    self.highlighted_button = None  # Reset highlighted button

    def reset_game(self):
        self.game_board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                buttons = self.buttons[i][j]
                self.buttons[i][j].setText("")
                buttons.setStyleSheet("font-size: 30px;")

        if self.game_mode == "Against Computer":
            self.start_game_button.setEnabled(True)
            # Player starts first in 'Against Computer' mode
            self.current_player = "Player 1"
        else:
            self.start_game_button.setEnabled(False)
            # Randomize the start between players in other modes
            self.current_player = random.choice(["Player 1", "Player 2"])

        self.turn_label.setText(f"Current Turn: {self.current_player}")


    def minimax(self, depth, alpha, beta, maximizing_player):
        winner = self.check_winner()
        if winner == "X":
            return -10 + depth, None
        elif winner == "O":
            return 10 - depth, None
        elif winner == None and all(all(cell != "" for cell in row) for row in self.game_board):
            return 0, None
        
    
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for i in range(3):
                for j in range(3):
                    if self.game_board[i][j] == "":
                        self.game_board[i][j] = "O"
                        eval, _ = self.minimax(depth + 1, alpha, beta, False)
                        self.game_board[i][j] = ""
                        if eval > max_eval:
                            max_eval = eval
                            best_move = (i, j)
                        elif eval == max_eval:
                         alpha = max(alpha, eval)
                        if beta <= alpha:
                            break  # Beta cut-off
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for i in range(3):
                for j in range(3):
                    if self.game_board[i][j] == "":
                        self.game_board[i][j] = "X"
                        eval, _ = self.minimax(depth + 1, alpha, beta, True)
                        self.game_board[i][j] = ""
                        if eval < min_eval:
                            min_eval = eval
                            best_move = (i, j)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break  # Alpha cut-off
            return min_eval, best_move

    def computer_move(self):
        if all(all(cell == "" for cell in row) for row in self.game_board):
            # If the board is empty, choose a random corner or center position
            corners_and_center = [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)]
            row, col = random.choice(corners_and_center)
        else:
            _, best_move = self.minimax(0, float('-inf'), float('inf'), True)
            if best_move:
                row, col = best_move
            else:
                return  # No valid moves

        if self.highlighted_button:
            self.highlighted_button.setStyleSheet("font-size: 30px;")
            self.highlighted_button = None

        self.on_click(row, col)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tictactoe = TicTacToe()
    sys.exit(app.exec_())
