# References:
# https://www.tutorialspoint.com/python3/python_gui_programming.htm
# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# https://stackoverflow.com/questions/34029223/basic-tkinter-countdown-timer
# https://www.speedtypingonline.com/typing-equations

import requests
from tkinter import *
from tkinter import messagebox

class GlobalTestState:
	def __init__(self):
		# initialize global settings
		self.finished_test = False
		self.seconds_elapsed = 0
		self.test_words_list = []
		self.typed_words_list = []
		self.typed_characters = 0
		self.searched_keyword = ""
		self.text_block = ""

class TypingTest(Tk, GlobalTestState):
	def __init__(self):
		Tk.__init__(self)
		
		# set tkinter frame size to 900x1100
		self.canvas = Canvas(self, height=900, width=1100)
		self.canvas.pack()
		self.frame = None
		self.show_frame(HomeScreen)
	
	def show_frame(self, screen_name):
		frame_to_show = screen_name(self)
		if self.frame:
			self.frame.destroy()
		self.frame = frame_to_show
		self.frame.place(relwidth=1.0, relheight=1.0)

class HomeScreen(Frame, GlobalTestState):
	def __init__(self, master):
		Frame.__init__(self, master)

		keyword = StringVar()

		home_label = Label(self, text="Typing Test", font=("Arial", 33))
		home_label.place(relx=0.5, rely=0.1, anchor="n")

		search_keyword = Entry(self, textvariable=keyword)
		search_keyword.place(relx=0.5, rely=0.45, anchor="n")

		help_message = Label(self, text="Search using a keyword on a topic you want to type about for the typing test", font=("Arial", 13))
		help_message.place(relx=0.5, rely=0.4, anchor="n")

		def errorMessage():
			error_message = messagebox.showerror("Error", "You did not enter a keyword, or entered an invalid keyword. Try again.")
			
		def get_keyword():
			if keyword.get():
				url = "https://daniel-yu.herokuapp.com/get_data/" + keyword.get()
				response = requests.get(url=url)
				data = response.json()

				if data["content"] != "Other reasons this message may be displayed:":
					GlobalTestState.text_block = data["content"]
					GlobalTestState.searched_keyword = keyword.get()
					master.show_frame(TestScreen)

				else:
					GlobalTestState.searched_keyword = ""
					GlobalTestState.text_block = ""
					errorMessage()
					
			else:
				GlobalTestState.searched_keyword = ""
				GlobalTestState.text_block = ""
				errorMessage()

		go_button = Button(self, text="Go", command=get_keyword)
		go_button.place(relx=0.5, rely=0.53, anchor="n")

class TestScreen(Frame, GlobalTestState):
	def __init__(self, master):
		Frame.__init__(self, master)
		
		# reset global test state for every test
		GlobalTestState.finished_test = False
		GlobalTestState.seconds_elapsed = 0
		GlobalTestState.typed_characters = 0
		GlobalTestState.test_words_list = []
		GlobalTestState.typed_words_list = []
		
		test_label = Label(self, text=GlobalTestState.searched_keyword, font=("Arial", 25))
		test_label.place(relx=0.5, rely=0.1, anchor="n")

		timer_label = Label(self)
		timer_label.place(relx=0.8, rely=0.1, anchor="n")

		def seconds_timer(start_time=0):
			if GlobalTestState.finished_test is False:
				GlobalTestState.seconds_elapsed += 1
				timer_label["text"] = "seconds elapsed: " + str(start_time)
				self.after(1000, seconds_timer, start_time+1)
			
		seconds_timer()

		test_text = Text(self, font=("Arial", 15), wrap=WORD)
		test_text.tag_configure("left", justify="left")

		test_text.insert("end", GlobalTestState.text_block, "left")
		test_text.configure(state="disabled")
		test_text.config(highlightbackground="#0096fc")
		test_text.place(relx=0.03, rely=0.5, anchor="w", width=500, height=600)

		test_field = Text(self, font=("Arial", 15), wrap=WORD)
		test_field.tag_configure("left", justify="left")
		test_field.config(highlightbackground="#0096fc")
		test_field.place(relx=0.97, rely=0.5, anchor="e", width=500, height=600)

		test_button = Button(self, text="Restart", command=lambda: master.show_frame(HomeScreen))
		test_button.place(relx=0.5, rely=0.85, anchor="n")

		def getTypedChars():
			typed_content = test_field.get("1.0", "end")
			GlobalTestState.typed_characters = len(typed_content)
			GlobalTestState.typed_words_list = typed_content.split()
			
			test_content = test_text.get("1.0", "end")
			GlobalTestState.test_words_list = test_content.split()

		done_button = Button(self, text="Done", command=lambda: [getTypedChars(), master.show_frame(ResultScreen)])
		done_button.place(relx=0.5, rely=0.88, anchor="n")

class ResultScreen(Frame, GlobalTestState):
	def __init__(self, master):
		Frame.__init__(self, master)

		# reset global test state for every test
		GlobalTestState.finished_test = True
		GlobalTestState.searched_keyword = ""
		GlobalTestState.text_block = ""

		result_label = Label(self, text="Score:", font=("Arial", 25))
		result_label.place(relx=0.5, rely=0.3, anchor="n")
		
		net_wpm = 0
		if GlobalTestState.typed_characters != 1:
			errors = 0
			i = j = 0
			while i < len(GlobalTestState.test_words_list) and j < len(GlobalTestState.typed_words_list):
				if GlobalTestState.test_words_list[i] != GlobalTestState.typed_words_list[j]:
					errors += 1
				i += 1
				j += 1

			while i < len(GlobalTestState.test_words_list):
				errors += 1
				i += 1
			
			net_wpm = ((GlobalTestState.typed_characters / 5) - errors) / (GlobalTestState.seconds_elapsed / 60)
			if net_wpm < 0:
				net_wpm = 0
			
			# print(net_wpm)

		score_label = Label(self, text=str(round(net_wpm))+" WPM", font=("Arial", 25))
		score_label.place(relx=0.5, rely=0.4, anchor="n")

		wpm_label = Label(self, text="WPM is calculated by taking into account all typed entries, uncorrected errors, and time taken. Learn more at: https://www.speedtypingonline.com/typing-equations")
		wpm_label.place(relx=0.5, rely=0.44, anchor="n")

		retry_button = Button(self, text="Retry", command=lambda: master.show_frame(HomeScreen))
		retry_button.place(relx=0.5, rely=0.48, anchor="n")

if __name__ == "__main__":
	app = TypingTest()
	app.mainloop()
