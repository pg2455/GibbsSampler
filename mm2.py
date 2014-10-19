import numpy as np
from flask import Flask
from flask import Request
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math

class Gibbs():

  def __init__(self):
    self.num_clust = 10
    self.num_points = 100
    self.data = 0
    self.sigma = 2
    self.lam = 10
    #self.mu defined in self.generate()

  def generate(self):
    num_clust = 10
    lam = 10 # covriance of clusters
    num_points = 100
    sigma = 2 # covariance in points

    cov_clust = np.matrix([[pow(lam,2),0],[0,pow(lam,2)]])
    cov_points = np.matrix([[pow(sigma,2),0],[0,pow(sigma,2)]])

    #pi= np.random.dirichlet([1]*num_clust)
    pi = [0.1]*10
    self.mu = np.random.multivariate_normal((0,0), cov_clust, num_clust)

    mix_assignments = np.random.multinomial(1,pi, size=num_points)
    points = [0]*num_points
    for i in range(num_points):
      clust = np.where(mix_assignments[i] == 1)[0][0]
      points[i] = (np.random.multivariate_normal(self.mu[clust], cov_points,1), clust)


    self.data = points
    #return points
    self.mu = [np.array([i]) for i in self.mu]
    #self.plot(self.data,self.mu)
    #plt.show()

  # get data as if it is observed without clusters
  def getData(self,data):
    return [(point,) for point,_ in data]

  #draw mixture assignments ?check for lam in 3rd line?
  def drawAssignments(self, data,mu):
    z_assignment= []
    for (point,cluster) in data:
      # assuming equally probable cluster assingment prior
      z_dist = [np.exp(-0.5*pow(np.linalg.norm(point - mu_k),2)) for mu_k in mu]
      z_dist = list(z_dist/sum(z_dist))
      z_assignment.append((point,z_dist.index(max(z_dist))))

    return z_assignment

  #draw mxiture probabilities : mu= nk/sigma2/n/sigma2+ 1/lambda2 * mean(xk)
  def drawDistribution(self, data):
    mu,sigma = [1]*self.num_clust, [1]*self.num_clust
    for k in range(self.num_clust):
      mu_simulated = [i[0] for i in data if i[1] == k] #scope for improvement
      x_bar_k = np.mean(mu_simulated, axis =0)
      n_k = len(mu_simulated)
      num = n_k*pow(self.sigma,-2)
      denom = num + pow(self.lam,-2)
      mu_k = x_bar_k *num /(num+denom)
      sigma_k = 1/(n_k*pow(self.sigma,-2)  + pow(self.lam,-2))
      mu[k], sigma[k] = [mu_k,np.array([[0.0,0.0]])][np.isnan(mu_k).any()] ,math.sqrt(sigma_k)

    return mu,sigma

  def sampler(self):
    data,log_likelihood_old = self.data, 1
    mu = np.random.multivariate_normal((0,0),np.matrix([[100,0],[0,100]]),size= self.num_clust)

    plt.hold(True)
    plt.figure(1)
    plt.subplot(121)
    self.plot(self.data,self.mu)

    for i in range(1000):
      data = self.drawAssignments(data,mu)
      mu,sigma = self.drawDistribution(data)

      log_likelihood_new = self.getLikelihood(data,mu,sigma)
      if math.fabs(log_likelihood_old -log_likelihood_new) < 1e-200:
        print log_likelihood_new, log_likelihood_old
        break
      else:
        log_likelihood_old= log_likelihood_new


      if i%100 == 0:
        print "\nsampling ... \n"
        plt.subplot(122)
        self.plot(data,mu)
        plt.show()

  def getLikelihood(self,data,mu,sigma):
    log = 0
    sigma = np.array(sigma)
    for datum in data:
      point = datum[0] # array of 2 dimension
      diff = np.array([i[0] for i in point - mu ])
      normalized_diff = np.dot(diff, diff.T).diagonal()
      normalized_diff = normalized_diff/((pow(sigma,2))*2)
      prob_point_in_diff_clusters = np.exp(-normalized_diff)/(math.sqrt(2.0*np.pi)*sigma)
      total_prob = (1.0/self.num_clust)*sum(prob_point_in_diff_clusters)
      log = log + math.log(total_prob)

    return log


  def plot(self, data,mu):
    colors= cm.rainbow(np.array(range(0,self.num_clust*25,25)))
    #plot points
    for datum in data:
      x,y,cluster_color = datum[0][0][0], datum[0][0][1], colors[datum[1]] # this 0 is because it is in matrix format
      plt.scatter(x,y,c=cluster_color, s= 20)

    #plot centers
    for k,mu_k in enumerate(mu):
      x,y = mu_k[0][0],mu_k[0][1]
      print x,y,k
      plt.scatter(x,y,c=colors[k], s = 100.0)

  def demo(self):
    self.generate()
    self.sampler()

string = '''
app=Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def display_message():
  f.generate()
  if f.sampler():
    return "There it is\n"
  else:
    return "Something is wrong...!!\n"
if __name__ == '__main__':
  f= Gibbs()
  app.debug = True
  app.run(host='0.0.0.0', port =8888)
'''
