# Programmer: Dalton Cole

from tkinter import *
from random import choice, randint
from time import time

class Person:
	def __init__(self, person, walking_speed):
		self.person = person
		self.set_speed(walking_speed)
		self.side = 0 # 0 if on or going to left side, 1 if on or going to right side
		self.time_stamp = None
		self.to_ack = []
		self.acked = 0


	def set_speed(self, walking_speed):
		if walking_speed == 'Slow':
			self.walking_speed = randint(1,10) / 50
		elif walking_speed == 'Medium':
			self.walking_speed = randint(10,25) / 50
		else:
			self.walking_speed = randint(25, 100) / 50
	def set_side(self, side):
		self.side = side


class Bridge:
	def __init__(self, root):
		self.root = root
		self.speed = 'Fast'
		self.algorithm = 'Ricart & Agrawalas'
		self.count = 2
		self.people = []
		self.c_size = 20 #c ircle size
		self.points = ((100, 450), (100, 50), (350, 250), (650, 250), (900, 50), (900, 450)) # 6 points of the triangles

		#p = Canvas(self.root)
		#p.create_polygon([150,75,225,0,300,75,225,150], outline='gray', fill='gray', width=2)
		#p.pack()


		self.make_canvas()
		self.make_menues()
		self.make_bridge()
		self.make_people()
		self.move_people()
		#self.make_canvas()
		#self.make_circle()

	def make_canvas(self):
		self.root.title("Test")
		#self.root.resizable(False, False)
		self.canvas = Canvas(self.root, width = 1000, height = 500, background='white')
		#self.canvas.pack()

	def make_menues(self):
		### Walking Speed ###
		# Make drop Down menu
		default_walking_speed = StringVar(self.root)
		default_walking_speed.set(self.speed)
		walking_speed = OptionMenu(self.root, default_walking_speed, 'Slow', 'Medium', 'Fast')
		walking_speed.grid(row=0, column=0)
		# Make button to confirm drop down menu
		set_walking_speed = lambda: self.set_walking_speed(default_walking_speed.get())
		speed_button = Button(self.root, text='Set Walking Speed', command=set_walking_speed)
		speed_button.grid(row=1, column=0)

		### Make Algorithm Choice ###
		# Make drop down Menu
		default_algorithm = StringVar(self.root)
		default_algorithm.set(self.algorithm)
		algorithm = OptionMenu(self.root, default_algorithm, 'Ricart & Agrawalas', 'Personal')
		algorithm.grid(row=0, column=1)
		# Make button to confirm drop down menu
		set_algorithm = lambda: self.set_algorithm(default_algorithm.get())
		algorithm_button = Button(self.root, text='Set Algorithm', command=set_algorithm)
		algorithm_button.grid(row=1, column=1)

		### Make number of nodes Choice ###
		# Make text field
		default_count = StringVar(self.root)
		default_count.set(self.count)
		count = Entry(self.root, textvariable=default_count)
		count.grid(row=0, column=2)
		# Make button to confirm text field
		set_count = lambda: self.set_count(default_count.get())
		count_button = Button(self.root, text='Set Person Count', command=set_count)
		count_button.grid(row=1, column=2)

	def make_bridge(self):
		self.canvas.grid(row=2,column=0,columnspan=3)
		#self.canvas.create_rectangle(80, 80, 120, 120, fill="blue")
		#self.canvas.create_rectangle(80, 80, 120, 120)
		self.canvas.create_polygon((100, 450, 350, 250, 100, 50), fill='white', outline='black')
		self.canvas.create_polygon((900, 450, 650, 250, 900, 50), fill='white', outline='black')
		self.canvas.create_line((350,250, 650,250))
		#self.canvas.move(triangle, 200,100)
		#self.canvas.move(line, 100,100) # (item, dx, dy) dx is offset from current position

	def make_people(self):
		self.colors = ['white', 'black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']

		for i in range(self.count):
			sp = choice(self.points) # Starting point
			#shape = self.canvas.create_oval((100 - self.c_size, 450 + self.c_size, 100 + self.c_size, 450 - self.c_size), fill=choice(self.colors))
			#shape = self.canvas.create_oval((900 - self.c_size, 50 + self.c_size, 900 + self.c_size, 50 - self.c_size), fill=choice(self.colors))
			#shape = self.canvas.create_oval((650 - self.c_size, 250 + self.c_size, 650 + self.c_size, 250 - self.c_size), fill=choice(self.colors))
			shape = self.canvas.create_oval((sp[0] - self.c_size, sp[1] + self.c_size, sp[0] + self.c_size, sp[1] - self.c_size), fill=self.random_color())
			self.people.append(Person(shape, self.speed))

	def move_people(self):
		try:
			for i in self.people:
				coords = self.canvas.coords(i.person)
				if i.time_stamp != None:
					#print(i.time_stamp)
					pass
				#print(coords)

				### 1-2 ###
				# On top of right triangle, go South East
				if(coords[0] == 100 - self.c_size and coords[1] == 50 - self.c_size):
					self.canvas.move(i.person, 1 * i.walking_speed, .8 * i.walking_speed)

				### 2-3 ###
				# Cross bridge going east
				elif(coords[0] == 350 - self.c_size and coords[1] == 250 - self.c_size and i.side == 1):
					self.cross_bridge(i)

				### 3-4 ###
				# Just crossed bridge going east, go North East
				elif(coords[0] == 650 - self.c_size and coords[1] == 250 - self.c_size and i.side == 1):
					self.canvas.move(i.person, (1 * i.walking_speed), (-.8 * i.walking_speed))
					i.time_stamp = None # Reset Time stamp

				### 4-5 ###
				# Move down on straight triangle
				elif(coords[0] == 900 - self.c_size and coords[1] == 50 - self.c_size):
					self.canvas.move(i.person, 0, i.walking_speed)

				### 5-6 ###
				# On bottom of left triangle, go North West
				elif(coords[0] == 900 - self.c_size and coords[1] == 450 - self.c_size):
					self.canvas.move(i.person, -(1 * i.walking_speed), (-.8 * i.walking_speed))

				### 6-7 ###
				# Cross bridge going west
				elif(coords[0] == 650 - self.c_size and coords[1] == 250 - self.c_size and i.side == 0):
					self.cross_bridge(i)

				### 7-8 ###
				# Just crossed bridge going west, go South West
				elif(coords[0] == 350 - self.c_size and coords[1] == 250 - self.c_size and i.side == 0):
					self.canvas.move(i.person, (-1 * i.walking_speed), (.8 * i.walking_speed))
					i.time_stamp = None # Reset Time stamp

				### 8-1 ###
				# Move up straight away triangle
				elif(coords[0] == 100 - self.c_size and coords[1] == 450):
					self.canvas.move(i.person, 0, -i.walking_speed)

				### 1 ###
				# Move up on straight away triangle
				elif(coords[0] == 100 - self.c_size and coords[1] < 450):
					# Go full distance if far away from (100, 50)
					if(coords[1] - i.walking_speed >= 50 - self.c_size):
						self.canvas.move(i.person, 0, - i.walking_speed)
					# Go parital distance if close to (100, 50)
					else:
						self.canvas.move(i.person, 0, - (coords[1] - (50 - self.c_size)))

				### 2 ###
				# Head towards left side of bridge
				elif(coords[0] > 100 - self.c_size and coords[0] < 350 - self.c_size and coords[1] < 250 - self.c_size):
					# Go ful distance if far away from (350,250):
					if(coords[1] + i.walking_speed <= 250 - self.c_size):
						self.canvas.move(i.person, 1 * i.walking_speed, .8 * i.walking_speed)
					else:
						self.canvas.move(i.person, ((350 - self.c_size) - coords[0]), ((250 - self.c_size) - coords[1]))
						i.set_side(1)
				
				### 3 ###
				### 7 ###
				# Move across bride
				elif(coords[0] > 350 - self.c_size and coords[0] < 650 - self.c_size and coords[1] == 250 - self.c_size):
					# Going East
					if(i.side == 1):
						# Go full distance if far away from (100, 50)
						if(coords[0] + i.walking_speed <= 650 - self.c_size):
							self.canvas.move(i.person, i.walking_speed, 0)
						# Go parital distance if close to (100, 50)
						else:
							self.canvas.move(i.person, (650 - self.c_size - coords[0]), 0)
					else:
						# Go full distance if far away from (100, 50)
						if(coords[0] - i.walking_speed >= 350 - self.c_size):
							self.canvas.move(i.person, -i.walking_speed, 0)
						# Go parital distance if close to (100, 50)
						else:
							self.canvas.move(i.person, -(coords[0] - (350 - self.c_size)), 0)

				### 4 ###
				# Head towards top right corner
				elif(coords[0] > 650 - self.c_size and coords[0] < 900 - self.c_size and coords[1] < 250 - self.c_size):
					# Go ful distance if far away from (900, 50):
					if(coords[1] - i.walking_speed >= 50 - self.c_size):
						self.canvas.move(i.person, (1 * i.walking_speed), (-.8 * i.walking_speed))
					else:
						self.canvas.move(i.person, (900 - self.c_size - coords[0]), -(coords[1] - (50 - self.c_size)))

				### 5 ###
				# Move down on straight away triangle
				elif(coords[0] == 900 - self.c_size and coords[1] > 50 - self.c_size):
					# Go full distance if far away from (900, 50)
					if(coords[1] + i.walking_speed <= 450 - self.c_size):
						self.canvas.move(i.person, 0, i.walking_speed)
					# Go parital distance if close to (900, 50)
					else:
						self.canvas.move(i.person, 0, ((450 - self.c_size) - coords[1]))

				### 6 ###
				# Head towards right side of bridge
				elif(coords[0] > 650 - self.c_size and coords[0] < 900 - self.c_size and coords[1] > 250 - self.c_size):
					# Go ful distance if far away from (650,250):
					if(coords[0] - i.walking_speed >= 650 - self.c_size):
						self.canvas.move(i.person, (-1 * i.walking_speed), (-.8 * i.walking_speed))
					else:
						self.canvas.move(i.person, -(coords[0] - (650 - self.c_size)), -(coords[1] - (250 - self.c_size)))
						i.set_side(0)

				### 8 ###
				# Head towards bottom left corner
				elif(coords[0] > 100 - self.c_size and coords[0] < 350 - self.c_size and coords[1] > 250 - self.c_size):
					# Go ful distance if far away from (350,250):
					if(coords[1] + i.walking_speed <= 450 - self.c_size):
						self.canvas.move(i.person, (-1 * i.walking_speed), (.8 * i.walking_speed))
					else:
						self.canvas.move(i.person, ((100 - self.c_size) - coords[0]), ((450 - self.c_size) - coords[1]))
				else:
					pass
				
		except Exception as e: print(e)

		self.root.after(10, self.move_people)

	def cross_bridge(self, person):
		if(self.algorithm == 'Ricart & Agrawalas'):
			if(self.bridge_single_person(person)):
				print('yep')
				if(person.side == 1):
					self.canvas.move(person.person, person.walking_speed, 0)
				else:
					self.canvas.move(person.person, -person.walking_speed, 0)
		else:
			if(self.bridge_multiple_people(person)):
				if(person.side == 1):
					self.canvas.move(person.person, person.walking_speed, 0)
				else:
					self.canvas.move(person.person, -person.walking_speed, 0)

	def bridge_single_person(self, person):
		# Set time stamp
		if person.time_stamp == None:
			person.time_stamp = time()

		# Check each process's time stamp #
		for i in self.people:
			# If no time stamp, recieve ack
			if i.time_stamp == None:
				person.acked += 1
			# If your time stamp is lower, you recieve ach
			elif i.time_stamp > person.time_stamp:
				person.acked += 1

		print(person.acked)

		if(person.acked == int(self.count) - 1):
			person.acked = 0
			return True

		person.acked = 0
		return False

	def bridge_multiple_people(self, person):
		pass

	def set_walking_speed(self, walking_speed):
		self.walking_speed = walking_speed

		for i in self.people:
			i.set_speed(self.walking_speed)

		print(self.walking_speed)

	def set_algorithm(self, algorithm):
		self.algorithm = algorithm
		print(self.algorithm)

	def set_count(self, count):
		self.count = count

		while(int(self.count) > len(self.people)):
			sp = choice(self.points) # start point
			shape = self.canvas.create_oval((sp[0] - self.c_size, sp[1] + self.c_size, sp[0] + self.c_size, sp[1] - self.c_size), fill=self.random_color())
			self.people.append(Person(shape, self.speed))
		while(int(self.count) < len(self.people)):
			shape = choice(self.people)
			self.people.remove(shape)
			self.canvas.delete(shape.person)

		print(self.count)

	def random_color(self):
		hex_colors = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
		return '#' + choice(hex_colors) + choice(hex_colors) + choice(hex_colors) + choice(hex_colors) + choice(hex_colors) + choice(hex_colors)

root = Tk()
ex = Bridge(root)

print("Entering GUI")
root.mainloop()