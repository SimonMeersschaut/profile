import json
import tkinter as tk
from glob import glob
from typing import Collection

COLORS = ['b', 'g', 'r', 'c', 'm', 'y', 'k', (0.1, 0.2, 0.5)]

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        self.title = 'Rutherford Backscattering material and component analasis'
        self.data = arrange(get_data())
        self.min, self.max = (min(self.data[0][1:]), max(self.data[0][1:]))
        self.begin_line = self.min
        self.end_line = self.max
        self.elementen = [channel[0] for channel in self.data if len(channel) > 0]
        self.low_limit, self.high_limit  = (self.min, self.max)

        self.pack()
        self.create_widgets()
        

    def create_widgets(self):
      self.checkboxes = []
      self.stringvars = []
      index = 0
      #self.render_elements = [str_var.get() for str_var in self.stringvars]
      #print(self.render_elements)
      for name in self.elementen[1:]:
        var = tk.IntVar()
        self.stringvars.append(var)
        #print(self.stringvars)
        checkbox = tk.Checkbutton(self, width=2, height=2, variable=var)
        checkbox.select()
        self.checkboxes.append(checkbox)
        self.render_elements = [str_var.get() for str_var in self.stringvars]
      for checkbox, name in zip(self.checkboxes, self.elementen[1:]):
        tk.Label(self, text=name).grid(column=0, row=index)
        checkbox.grid(column=1, row=index)
        checkbox["command"] = self.update
        index += 1

      self.calc_vars = []
      calc_index = 0
      for name in self.elementen[1:]:
        var = tk.IntVar()
        var.trace("w", self.update)
        self.calc_vars.append(var)

        checkbox = tk.Checkbutton(self, width=2, height=2, variable=var)
        checkbox.select()
        checkbox.grid(column=2, row=calc_index)
        calc_index += 1
        
      self.low_stringvar = tk.StringVar()
      
      self.high_stringvar = tk.StringVar()
      
      self.lower_entry = tk.Entry(self, textvariable=self.low_stringvar)
      self.lower_entry.insert(tk.END, self.min)
      index += 1
      self.lower_entry.grid(column=0, row=index)
      self.higher_entry = tk.Entry(self, textvariable=self.high_stringvar)
      self.higher_entry.insert(tk.END, self.max)
      self.low_stringvar.trace("w", self.update)
      self.high_stringvar.trace("w", self.update)
      index += 1
      
      self.higher_entry.grid(column=0, row=index)
      index += 1

      self.low_line_stringvar = tk.StringVar()
      
      self.high_line_stringvar = tk.StringVar()
      
      self.lower_line_entry = tk.Entry(self, textvariable=self.low_line_stringvar)
      self.lower_line_entry.insert(tk.END, self.min)
      index += 1
      self.lower_line_entry.grid(column=0, row=index)
      self.higher_line_entry = tk.Entry(self, textvariable=self.high_line_stringvar)
      self.higher_line_entry.insert(tk.END, self.max)
      self.low_line_stringvar.trace("w", self.update)
      self.high_line_stringvar.trace("w", self.update)
      index += 1
      
      self.higher_line_entry.grid(column=0, row=index)
      index += 1

      self.update_button = tk.Button(self)
      self.update_button["text"] = "Update"
      self.update_button["command"] = self.update
      self.update_button.grid(column=0, row=index)

        #self.quit = tk.Button(self, text="QUIT", fg="red",
        #                      command=self.master.destroy)
        #self.quit.pack(side="bottom")

    def update(self, *args, **kwargs):
        print("hi there, everyone!")
        self.render_elements = [str_var.get() for str_var in self.stringvars]
        self.calc_elements = [str_var.get() for str_var in self.calc_vars]
        try:
          self.low_limit = float(self.low_stringvar.get())
          self.high_limit = float(self.high_stringvar.get())
        except ValueError:

          return None  
        main_plot(self.render_elements, (self.low_line_stringvar.get(), self.high_line_stringvar.get()), self.calc_elements)


def get_data():
  files = [file for file in glob('*.txt') if 'depthprofile' in file]

  with open(files[0], 'r') as f:
    text = f.read()
  data = [[number for number in line.split(' ') if number != ''] for line in text.split('\n')]
  compressed_data = []
  for channel in data:
    temp_data = []
    for index, number in enumerate(channel):
      if number != channel[0] or index == 0:
        try:
          number = float(number)
        except ValueError:
          #print(number)
          pass
        temp_data.append(number)
    compressed_data.append(temp_data)
  return compressed_data

def arrange(data):
  lines = [[] for _ in range(len(data))]
  for channel in data:
    for index, number in enumerate(channel):
      lines[index].append(number)
  return lines

def calc(data, lines, v_line1, v_line2):
  x = data[0][1:]
  y = data[1][1:]
  gems = []
  for line, plot in zip(data[1:], lines):
    this_line = []
    if plot == 1:
      for x_value, value in zip(x, line):
        if v_line1 < float(x_value) < v_line2:
          this_line.append(value)
    try:
      gem = sum(this_line)/len(this_line)
      gems.append(gem)
    except ZeroDivisionError:
      gems.append(0)
  print(gems)
  return gems



def plot(data, lines, v_line1, v_line2):
  #input((app.low_limit, app.high_limit))
  import matplotlib.pyplot as plt

  fig = plt.figure(1)	#identifies the figure
  fig.clf()
  plt.title(app.title, fontsize='16')	#title
  x = data[0][1:]
  y = data[1][1:]
  
  for line, plot, color in zip(data[1:], lines, COLORS):
    cropped_line_x = []
    cropped_line_y = []
    if plot == 1:
      if line != []:
        for x_value, y in zip(x, line[1:]):
          if app.low_limit < x_value < app.high_limit:
            cropped_line_x.append(x_value)
            cropped_line_y.append(y)
    
        plt.plot(cropped_line_x, cropped_line_y, color=color)
  plt.vlines([v_line1, v_line2], 0, 1, color="black")
  #plt.vlines(, 0, 1, color="black")
  plt.show()

def main_plot(lines, vertical_lines, calc_lines):
  v_1, v_2 = vertical_lines
  v_1, v_2 = (float(v_1), float(v_2))
  data = get_data()
  arranged = arrange(data)
  calc(arranged, calc_lines, v_1, v_2)
  #with open('file.txt', 'a+') as f:
  #  for i in arranged[:2]:
  #    f.write(f'{i}')#{}  {i[1]}'')
  #  #f.write(json.dumps(arranged[0:2]))
  plot(arranged, lines, v_1, v_2)

if __name__ == '__main__':
  root = tk.Tk()
  app = Application(master=root)
  app.mainloop()