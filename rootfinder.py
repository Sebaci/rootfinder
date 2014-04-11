import math

# this class computes computes complex roots of polynomials
class Rootfinder(object):
    def __init__(self, coef):
      i = 0
      while coef[i] == 0: i += 1
      self.coef = coef[i:]
      self.deg = len(self.coef)-1
      self.roots = []
      
      self.uStart = []
      self.vStart = []
      for i in range(1, 41):
        self.uStart.append(float(i)/10.0)
        self.vStart.append(float(i)/10.0)
        self.uStart.append(float(-i)/10.0)
        self.vStart.append(float(-i)/10.0)
      self.uInd, self.vInd = 0, 0
        
    def findRoots(self):
      self.roots = []
      coefA = self.coef[::-1]
      coefB = [0] * len(coefA)
      
      uList = []
      vList = []
      
      # max number of iterations
      m = 10000
      eps = 0.0000000000000000000000001
      
      n = self.deg
      while n > 1:
          # initial values
          u, v = self.uStart[self.uInd], self.vStart[self.vInd]
      
          for j in range(0, m):
            
              b1 = coefA[n]
              c1 = 0.0
              c0 = b1;
              
              b0 = coefA[n-1] + u*b1;
              coefB[n] = b1;
              coefB[n-1] = b0;
              
              for k in reversed(range(0, n-1)):
                  bt = coefA[k] + u*b0 + v*b1
                  b1 = b0
                  b0 = bt
                  coefB[k] = bt
                  ct = b1 + u*c0 + v*c1
                  c2 = c1
                  c1 = c0
                  c0 = ct
              
              jacob = c0*c2 - c1*c1
              if jacob == 0:
                  size = len(self.uStart)
                  if self.vInd < size-1: self.vInd += 1
                  elif self.uInd < size-1:
                    self.uInd += 1
                    self.vInd = 0
                  else: return
                  
                  self.findRoots()
                  return
              
              u = u + (c1*b1 - c2*b0) / jacob
              v = v + (c1*b0 - c0*b1) / jacob
              #u = u + c1/jacob*b1 - c2/jacob*b0
              #v = v + c1/jacob*b0 - c0/jacob*b1
              
              # check if b1, b0 are small enough
              if abs(b0) <= eps and abs(b1) <= eps: break
          
          for k in range(0, n-1): coefA[k] = coefB[k+2]
          
          n -= 2
          uList.append(u)
          vList.append(v)
      
      # roots
      
      for k in range(0, len(uList)):
          p = uList[k]
          i = p*p + 4*vList[k]
          
          if i < 0:
              i = math.sqrt(-i)
              self.roots.append(complex(p/2, i/2))
              self.roots.append(complex(p/2, -i/2))
          else:
              i = math.sqrt(i)
              self.roots.append(complex((p+i)/2, 0))
              self.roots.append(complex((p-i)/2, 0))
              
      if self.deg % 2 == 1:
          z = -coefA[0]/coefA[1]
          self.roots.append(complex(z, 0))

