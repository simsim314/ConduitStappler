import golly as g 
from sets import Set

zeroGld = g.parse("3C$2.C$.C!")
gld = g.parse("3B$B3A$.A3B$2.A2B$3.2B!", -1, -1)
validationgld = g.parse("$2.4B$.5B$.3A2B$3BAB$2BA$2B!", -3, -3)

glds = [gld, g.transform(gld, 0, 0, -1, 0, 0, 1),  g.transform(gld, 0, 0, 1, 0, 0, -1), g.transform(gld, 0, 0, -1, 0, 0, -1)]

def ValidatePresence (pat, xin, yin):	
	for i in xrange(2, len(pat), 3):
		x = pat[i - 2]
		y = pat[i - 1]
		state = pat[i]
		
		if g.getcell(xin + x, yin + y) != state:
			return False
	
	return True

def Locate(pat):
	
	result = [] 
	
	rect = g.getrect()
	cells = g.getcells(rect)
	
	for i in xrange(2, len(cells), 3):
		x = cells[i - 2]
		y = cells[i - 1]
				
		if ValidatePresence(pat, x, y):
			result.append((x, y))
	
	return result 	
	

def ValidateMovedPresence (pat, xin, yin):	
	for i in xrange(2, len(pat), 3):
		x = pat[i - 2]
		y = pat[i - 1]
		state = pat[i]
		realstate = g.getcell(xin + x, yin + y) 
		
		if state == 0 or state == 2:
			if realstate == 1 or realstate == 3 or realstate == 5:
				g.show(str((xin + x, yin + y)))
				return False
		if state == 1 or state == 3 or state == 5:		
			if realstate == 0 or realstate == 2 or realstate == 4:
				g.show(str((xin + x, yin + y, state, realstate)))
				return False
		
	return True

def Remove(pat, xin, yin):

	for i in xrange(2, len(pat), 3):
		x = pat[i - 2]
		y = pat[i - 1]
		g.setcell(xin + x, yin + y, 2) 
		
def FindGliders():
	return Locate(zeroGld)
	
def FindAdjescent(x, y):
	data = Set()
	data.add((x, y, g.getcell(x, y)))
	
	setSize = -1
	
	while setSize != len(data):
		setSize = len(data)
		data1 = data.copy()
		for s in data1:
			x, y, state = s 
			
			for i in xrange(-1, 2):
				for j in xrange(-1, 2):
					if state > 0:
						data.add((x + i, y + j, g.getcell(x + i, y + j)))
					else:
						if g.getcell(x + i, y + j) > 0:
							data.add((x + i, y + j, g.getcell(x + i, y + j)))
		

	return data
	
def PlaceConduit(data):
	for s in data:
		x, y, state = s 
		g.setcell(x, y, state)

def IterateToInput(x, y):
	
	for i in xrange(1, 1000):
		g.run(4)
		if not ValidateMovedPresence(validationgld, x + i + 2, y - i):
			i -= 1
			return (x + i + 2, y - i, int(g.getgen()) - 4)
		
def FindOutputs(inx, iny, ingen):
	result = []
	
	cells = []
	
	while g.getcells(g.getrect()) != cells:
		cells = g.getcells(g.getrect()) 
		g.run(1)
		
		for i in xrange(len(glds)):
			xyList = Locate(glds[i])
		
			for xy in xyList:
				x, y = xy
				result.append((x - inx, y - iny, i, int(g.getgen()) - ingen))
				Remove(glds[i], x, y)
				
	return result 
		
class Conduit:

	def __init__(self, outputs, dataset, inputgen, stabilizationgen):
		self.outputs = outputs    
		self.dataset = dataset
		self.inputgen = inputgen
		self.stabilizationgen = stabilizationgen
	
	def DState(self, instate, outstate):
		if instate == 0:
			if outstate == 0:
				return (-1, 1, 1)
			if outstate == 1:
				return (-1, 1, 0)
			if outstate == 2:
				return (-1, 1, 3)
			if outstate == 3:
				return (-1, 1, 2)
		
		if instate == 1:
			return (1, 1, outstate)
		
		if instate == 2:
			return (-1, -1, 3 - outstate)
		
		if instate == 3:
			if outstate == 0:
				return (1, -1, 2)
			if outstate == 1:
				return (1, -1, 3)
			if outstate == 2:
				return (1, -1, 0)
			if outstate == 3:
				return (1, -1, 1)
		
	def ReturnGliders(self, x, y, state, gen):
		result = []
		
		for x1, y1, i1, gen1 in self.outputs:
			mx, my, mstate = self.DState(state, i1)
			result.append((x + mx * x1, y + my * y1, mstate, gen + gen1))

		return result
		
gliders = FindGliders()
x, y, = gliders[0]
data = FindAdjescent(x, y)
g.new("")
PlaceConduit(data)
inx, iny, ingen= IterateToInput(x, y)
outputs = FindOutputs(inx, iny, ingen)

con = Conduit(outputs, data, ingen, int(g.getgen()) - ingen)

g.show(str(con.ReturnGliders(0, 0, 0, 0)))

#g.show(str(FindAdjescent(x, y)))
#def ReadConduits():
	