# 2048 game in python with tk as a desktop application
# made by omar sumon
# imports libraries and frameworks
import tkinter as tk
import colors as c
import random

# game class (OOP(object-oriented-programming))
class Game(tk.Frame):
	# initilises game
	def __init__(self):
		tk.Frame.__init__(self)
		self.grid()
		self.master.title("2048 Game")

		self.main_grid = tk.Frame(
			self, bg=c.GRID_COLOR, bd=3, width=600, height=600
		)
		self.main_grid.grid(pady=(100, 0))
		# callback functions
		self.make_gui()
		self.start_game()

		# key bindings
		self.master.bind("<Left>", self.left)
		self.master.bind("<Right>", self.right)
		self.master.bind("<Up>", self.up)
		self.master.bind("<Down>", self.down)

		# keeps window running
		self.mainloop()

	# makes game window

	def make_gui(self):
		# make grid
		self.cells = []
		for i in range(4):
			row = []
			for j in range(4):
				cell_frame = tk.Frame(
					self.main_grid,
					bg=c.EMPTY_CELLCOLOR,
					width=150,
					height=150
				)
				cell_frame.grid(row=i, column=j, padx=5, pady=5)
				cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELLCOLOR)
				cell_number.grid(row=i, column=j)
				cell_data = {"frame": cell_frame, "number": cell_number}
				row.append(cell_data)
			self.cells.append(row)

		# score header
		score_frame = tk.Frame(self)
		score_frame.place(relx=0.5, y=45, anchor="center")
		tk.Label(score_frame, text="Score", font=c.SCORE_label_FONT).grid(row=0)
		self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_font)
		self.score_label.grid(row=1)

	# starts game

	def start_game(self):
		# create matrix of zeroes
		self.matrix = [[0] * 4 for _ in range(4)] 

		# fill 2 random cells
		row = random.randint(0, 3)
		col = random.randint(0, 3)
		self.matrix[row][col]= 2
		self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
		self.cells[row][col]["number"].configure(
			bg=c.CELL_COLORS[2],
			fg=c.CELL_NUM_COLORS[2],
			font=c.CELL_NUM_FONTS[2],
			text="2"
		)
		while(self.matrix[row][col] != 0):
			row = random.randint(0, 3)
			col = random.randint(0, 3)
		self.matrix[row][col]= 2
		self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
		self.cells[row][col]["number"].configure(
			bg=c.CELL_COLORS[2],
			fg=c.CELL_NUM_COLORS[2],
			font=c.CELL_NUM_FONTS[2],
			text="2"
		)


		self.score = 0


	# stacks numbers

	def stack(self):
		new_matrix = [[0] * 4 for _ in range(4)]
		for i in range(4):
			fill_position = 0
			for j in range(4):
				if self.matrix[i][j] != 0:
					new_matrix[i][fill_position] = self.matrix[i][j]
					fill_position += 1
		self.matrix = new_matrix

	# combine function

	def combine(self):
		for i in range(4):
			for j in range(4):
				if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
				 	self.matrix[i][j] *= 2
				 	self.matrix[i][j + 1] = 0
				 	self.score += self.matrix[i][j]


	# Reverse function

	def reverse(self):
		new_matrix = []
		for i in range(4):
			new_matrix.append([])
			for j in range(4):
				new_matrix[i].append(self.matrix[i][3 -j])
		self.matrix = new_matrix

	# transpose function

	def transpose(self):
		new_matrix = [[0] * 4 for _ in range(4)]
		for i in range(4):
			for j in range(4):
				new_matrix[i][j] = self.matrix[j][i]
		self.matrix = new_matrix


	# adds tiles

	def add_new_tile(self):
			row = random.randint(0, 3)
			col = random.randint(0, 3)
			while(self.matrix[row][col] != 0):
				row = random.randint(0, 3)
				col = random.randint(0, 3)
			self.matrix[row][col]= random.choice([2, 4])

	# updates the game (updates the frames to give ilusion of motion)

	def update_game(self):
			for i in range(4):
				for j in range(4):
					cell_value = self.matrix[i][j]
					if cell_value == 0:
						self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELLCOLOR)
						self.cells[i][j]["number"].configure(bg=c.EMPTY_CELLCOLOR, text="")
					else:
						self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])
						self.cells[i][j]["number"].configure(bg=c.CELL_COLORS[cell_value], fg=c.CELL_NUM_COLORS[cell_value], font=c.CELL_NUM_FONTS[cell_value], text=str(cell_value))
			self.score_label.configure(text=self.score)
			self.update_idletasks()		


	# Arrow press Functions

	def left(self, event):
		self.stack()
		self.combine()
		self.stack()
		self.add_new_tile()
		self.update_game()
		self.game_over()


	def right(self, event):
		self.reverse()
		self.stack()
		self.combine()
		self.stack()
		self.reverse()
		self.add_new_tile()
		self.update_game()
		self.game_over()


	def up(self, event):
		self.transpose()
		self.stack()
		self.combine()
		self.transpose()
		self.add_new_tile()
		self.update_game()
		self.game_over()


	def down(self, event):
		self.transpose()
		self.reverse()
		self.stack()
		self.combine()
		self.stack()
		self.reverse()
		self.transpose()
		self.add_new_tile()
		self.update_game()
		self.game_over()

	# checks if any moves are left

	def horisontal_move_exists(self):
		for i in range(4):
			for j in range(4):
				if self.matrix[i][j] == self.matrix[i][j + 1]:
					return True
		return False

	def vertical_move_exists(self):
		for i in range(4):
			for j in range(4):
				if self.matrix[i][j] == self.matrix[i][j + 1]:
					return True
		return False



	# checks if game is over

	def game_over(self):
		if any(2048 in row for row in self.matrix):
			game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
			game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
			rk.Label(
				game_over_frame,
				text="You Win!",
				bg=c.winner_bg,
				fg=c.LOSER_FONT_COLOR,
				font=c.LOSE_FONT
			).pack()
		elif not any(0 in row for row in self.matrix) and not self.horisontal_move_exists() and not self.vertical_move_exists():
			game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
			game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
			rk.Label(
				game_over_frame,
				text="Game Over, You Lost",
				bg=c.LOSER_bg,
				fg=c.LOSER_FONT_COLOR,
				font=c.LOSE_FONT
			).pack()

# main function

def main():
	# calls the game functions
	Game()


# checks if running

if __name__ == '__main__':

	# calls back the main function to run the code

	main()