# https://www.tutorialspoint.com/python3/python_gui_programming.htm
# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# https://stackoverflow.com/questions/34029223/basic-tkinter-countdown-timer

from tkinter import *
from tkinter import messagebox

class GlobalTestState:
		finished_test = False
		seconds_elapsed = 0
		typed_characters = 0

class TypingTest(Tk, GlobalTestState):
	def __init__(self):
		Tk.__init__(self)
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
		home_label = Label(self, text="Typing Test", font=("Arial", 33))
		home_label.place(relx=0.5, rely=0.1, anchor="n")

		search_keyword = Entry(self)
		search_keyword.place(relx=0.5, rely=0.45, anchor="n")

		# HELP MSGS - replacing '?' buttons for easier ux
		help_message = Label(self, text="Search using a keyword on a topic you want to type about for the typing test", font=("Arial", 13))
		help_message.place(relx=0.5, rely=0.4, anchor="n")

		# POPUP MESSAGE WHEN INVALID KEYWORD SEARCHED
		# def errorMessage():
		# 	error_message = messagebox.showerror("Error!")
		go_button = Button(self, text="Go", command=lambda: master.show_frame(TestScreen)) #command=errorMessage)
		go_button.place(relx=0.5, rely=0.53, anchor="n")

class TestScreen(Frame, GlobalTestState):
	def __init__(self, master):
		Frame.__init__(self, master)
		
		# reset global test state for every test
		GlobalTestState.finished_test = False
		GlobalTestState.seconds_elapsed = 0
		GlobalTestState.typed_characters = 0
		
		test_label = Label(self, text="Lorem Ipsum", font=("Arial", 25))
		test_label.place(relx=0.5, rely=0.1, anchor="n")

		timer_label = Label(self)
		timer_label.place(relx=0.8, rely=0.1, anchor="n")

		# TIMER STARTS RIGHT AWAY
		def seconds_timer(start_time=0):
			if GlobalTestState.finished_test is False:
				GlobalTestState.seconds_elapsed += 1
				timer_label["text"] = "seconds elapsed: " + str(start_time)
				self.after(1000, seconds_timer, start_time+1)
			
		seconds_timer()

		# WEB SCRAPER - to be replaced by text fetched using scraper using user entered keyword
		test_text = Text(self, font=("Arial", 15))
		test_text.tag_configure("left", justify="left")

		# LINE BREAKS -maybe figure out line breaks for each given text by figuring out size of the width and chars that can go into one line in the future.
		test_text.insert("end", "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", "left")
		test_text.configure(state="disabled")
		test_text.config(highlightbackground="#0096fc")
		test_text.place(relx=0.03, rely=0.5, anchor="w", width=500, height=600)

		test_field = Text(self, font=("Arial", 15))
		test_field.tag_configure("left", justify="left")
		test_field.config(highlightbackground="#0096fc")
		test_field.place(relx=0.97, rely=0.5, anchor="e", width=500, height=600)

		test_button = Button(self, text="Restart", command=lambda: master.show_frame(HomeScreen))
		test_button.place(relx=0.5, rely=0.85, anchor="n")

		def getTypedChars():
			typed_content = test_field.get("1.0", "end")
			print(len(typed_content))
			GlobalTestState.typed_characters = len(typed_content)

		done_button = Button(self, text="Done", command=lambda: [getTypedChars(), master.show_frame(ResultScreen)])
		done_button.place(relx=0.5, rely=0.88, anchor="n")

class ResultScreen(Frame, GlobalTestState):
	def __init__(self, master):
		Frame.__init__(self, master)

		GlobalTestState.finished_test = True

		result_label = Label(self, text="Score:", font=("Arial", 25))
		result_label.place(relx=0.5, rely=0.3, anchor="n")

		# COLOR CODED - should account for correct/wrong words?
		# ACCURATE WPM - calculation methods
		wpm = 0
		if GlobalTestState.typed_characters != 1:
			wpm_speed = (GlobalTestState.typed_characters / 5) / ((GlobalTestState.seconds_elapsed) / 60)
			wpm_rounded = round(wpm_speed, 0)
			wpm = wpm_rounded

		score_label = Label(self, text=str(wpm)+" WPM", font=("Arial", 25))
		score_label.place(relx=0.5, rely=0.4, anchor="n")

		retry_button = Button(self, text="Retry", command=lambda: master.show_frame(HomeScreen))
		retry_button.place(relx=0.5, rely=0.48, anchor="n")

if __name__ == "__main__":
	app = TypingTest()
	app.mainloop()
