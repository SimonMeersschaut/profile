from glob import glob
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
          print(number)
        temp_data.append(number)
    compressed_data.append(temp_data)
  return compressed_data

def limit_data(data, lower_limit, higher_limit):
  limited_data = []
  legend = []
  for channel in data:
    try:
      print(channel)
      if len(channel) > 0:
        if lower_limit < channel[0] < higher_limit:
          limited_data.append(channel)
    except TypeError: 
      legend = channel
  lines = [[] for _ in range(len(limited_data[0]))]
  for channel in limited_data:
    for index, number in enumerate(channel):
      lines[index].append(number)
  return lines, legend

def plot(data):
  import matplotlib.pyplot as plt
  fig = plt.figure(1)	#identifies the figure 
  plt.title("Y vs X", fontsize='16')	#title
  print(data)
  x = [channel[0] for channel in data][0]
  y = [channel[0:] for channel in data]
  print(x,y)
  plt.plot(x, y)
  plt.show()

if __name__ == '__main__':
  data = get_data()
  lower_limit, higher_limit = (0, 1000)
  print(data)
  limited_data = limit_data(data, lower_limit, higher_limit)
  plot(limited_data)
