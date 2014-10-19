# generate points

class Gibbs_Sampler():

  def init(self, mu, hyp_pi,var):
    pass


  def generate(self,num_points, mu, var,pi,num_clusters = 2):
    # num_points is a list
    assert type(num_points) == list , "num_points is not a list"
    if len(num_points) < num_clusters:
      num_points = num_points+[num_points[-1] for _ in range(num_clusters - len(num_points))]
    if not num_points:
      num_points = [100 for _ in range(num_clusters)]
      assert len(mu) == len(num_points), "mu is not of same length as num_points"

    pi = np.random.dirichilet([1]*sum(num_points))


    #distribution is gaussian
    points = [np.random.multivariate_normal(mu[x], var, i) for x,i in enumerate(num_points)]

    return points
