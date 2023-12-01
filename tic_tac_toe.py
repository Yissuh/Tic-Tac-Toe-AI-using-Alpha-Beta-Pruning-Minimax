import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMessageBox, QComboBox, QLabel

class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()

        self.current_player = "Player 1"
        self.game_board = [["" for _ in range(3)] for _ in range(3)]
        self.game_mode = "Against Computer"

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

        self.show()

    def select_game_mode(self):
        self.reset_game()
        self.game_mode = self.game_mode_combo.currentText()

        if self.game_mode == "Against Computer" and self.current_player == "Player 2":
            self.computer_move()

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
                else:
                    winner_message = "Player 1 Wins" if winner == "X" else "Player 2 Wins"
                QMessageBox.information(self, "Tic Tac Toe", f"{winner_message}!")
                self.reset_game()
            elif all(all(cell != "" for cell in row) for row in self.game_board):
                QMessageBox.information(self, "Tic Tac Toe", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"
                self.turn_label.setText(f"Current Turn: {self.current_player}")
                if self.game_mode == "Against Computer" and self.current_player == "Player 2":
                    self.computer_move()

    def reset_game(self):
        self.current_player = "Player 1"
        self.game_board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setText("")
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
        _, best_move = self.minimax(0, float('-inf'), float('inf'), True)
        if best_move:
            row, col = best_move
            self.on_click(row, col)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tictactoe = TicTacToe()
    sys.exit(app.exec_())